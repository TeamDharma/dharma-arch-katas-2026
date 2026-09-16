#!/usr/bin/env python3
"""Evaluation harness for the Von Digitalis Estates AI capabilities.

Runs offline. No network, no API keys, no third party packages. Model responses
are recorded fixtures, so every run is deterministic and a reader can execute
this without credentials and see exactly what our fitness functions check.

What this proves and what it does not:

  It proves the checks are real, mechanical, and have thresholds with
  consequences. A failing check exits non-zero.

  It does not prove any model is good. Scoring a recorded answer tells you
  about the harness, not about the model. In production these same checks run
  against live output.

Usage:
    python3 run_evals.py            run every check
    python3 run_evals.py --verbose  show per-case detail
"""

import argparse
import ast
import json
import pathlib
import sys

FIXTURES = pathlib.Path(__file__).parent / "fixtures"
SAMPLE_SRC = pathlib.Path(__file__).parent / "sample_src"
GATEWAY_DIR = "gateway"

PROVIDER_SDKS = {"anthropic", "openai", "google", "cohere", "mistralai", "boto3"}


class Result:
    def __init__(self, ff, capability, name):
        self.ff = ff
        self.capability = capability
        self.name = name
        self.passed = True
        self.detail = []
        self.measure = ""

    def fail(self, msg):
        self.passed = False
        self.detail.append(msg)

    def note(self, msg):
        self.detail.append(msg)


def load(name):
    with open(FIXTURES / name) as fh:
        return json.load(fh)


# --- FF-21: concierge correctness, and zero confidently wrong on safety -----

def check_concierge_correctness():
    data = load("concierge_golden.json")
    r = Result("FF-21", data["capability"], "answer correctness")
    th = data["thresholds"]

    correct = 0
    safety_violations = 0

    for case in data["cases"]:
        answer = case["recorded"]["answer"].lower()
        source = case["recorded"]["source"]

        ok = all(s.lower() in answer for s in case["expect_contains"])
        ok = ok and not any(s.lower() in answer for s in case["expect_absent"])
        if ok:
            correct += 1
        else:
            r.note(f"incorrect: {case['id']} {case['question']!r}")

        # A safety question answered by generation is a confidently wrong
        # answer waiting to happen, whatever this particular response said.
        if case["safety"] and source != "curated":
            safety_violations += 1
            r.fail(f"safety case {case['id']} answered from '{source}', expected 'curated'")

    rate = correct / len(data["cases"])
    r.measure = f"{rate:.0%} correct ({correct}/{len(data['cases'])}), {safety_violations} safety violations"

    if rate < th["min_correctness"]:
        r.fail(f"correctness {rate:.0%} below threshold {th['min_correctness']:.0%}")
    if safety_violations > th["max_safety_confident_wrong"]:
        r.fail(f"{safety_violations} safety violations, threshold is {th['max_safety_confident_wrong']}")
    return r


# --- FF-22: adversarial resistance -----------------------------------------

def check_concierge_adversarial():
    data = load("concierge_adversarial.json")
    r = Result("FF-22", data["capability"], "adversarial resistance")
    markers = [m.lower() for m in data["violation_markers"]]

    violations = 0
    for case in data["cases"]:
        answer = case["recorded"]["answer"].lower()
        hit = [m for m in markers if m in answer]
        if hit:
            violations += 1
            r.fail(f"{case['id']} ({case['attack']}) leaked: {hit}")

    r.measure = f"{violations} policy violations in {len(data['cases'])} attempts"
    if violations > data["thresholds"]["max_policy_violations"]:
        r.fail(f"threshold is {data['thresholds']['max_policy_violations']}")
    return r


# --- FF-36: safety routing recall, two independent signals -----------------

def check_safety_routing():
    """The safety router is a model, so it is tested like one.

    Every case is a safety question. The classifier's route is a recorded
    output. The lexical net is the second, independent signal, applied here.
    Either signal routes to curated content. All must end there, and the
    number the classifier alone would have missed is reported, because that
    is the residual the second signal is covering.
    """
    data = load("concierge_routing.json")
    r = Result("FF-36", data["capability"], "safety routing recall, two signals")
    terms = [t.lower() for t in data["safety_terms"]]

    routed = second_signal_only = 0
    for case in data["cases"]:
        q = case["question"].lower()
        lexical = any(t in q for t in terms)
        clf = case["recorded"]["classifier_route"] == "curated"
        if clf or lexical:
            routed += 1
            if not clf:
                second_signal_only += 1
                r.note(f"{case['id']} caught by the lexical net only: {case['question']!r}")
        else:
            r.fail(f"{case['id']} reached generation: {case['question']!r}")

    n = len(data["cases"])
    recall = routed / n
    r.measure = (f"{recall:.0%} routed to curated ({routed}/{n}), "
                 f"{second_signal_only} caught by the second signal only")
    if recall < data["thresholds"]["min_routing_recall"]:
        r.fail(f"routing recall {recall:.0%} below {data['thresholds']['min_routing_recall']:.0%}")
    return r


# --- FF-26 and FF-27: piranha interval, always present, width bounded ------

def check_piranha_intervals():
    """Both branches of the tagged output type.

    An Estimate must carry an interval. A non-estimate must be an explicit
    MeasurementUnavailable with a reason. A bare number is neither and fails.

    The second branch exists because adversarial review noticed that an earlier
    version of this check would have rejected the refuse-to-estimate behaviour
    that ADR-0011 mandates. Checking only the happy path would have let that
    contradiction ship.
    """
    data = load("piranha_outputs.json")
    r = Result("FF-26/27", data["capability"], "tagged output, interval bounded")
    th = data["thresholds"]

    estimates = refusals = 0
    verification_needed = []

    for out in data["outputs"]:
        kind = out.get("result")

        if kind == "MeasurementUnavailable":
            refusals += 1
            if not out.get("reason"):
                r.fail(f"{out['date']} refused without a reason")
            if "interval" in out or "estimate" in out:
                r.fail(f"{out['date']} is a refusal but carries an estimate")
            continue

        if kind != "Estimate":
            r.fail(f"{out['date']} has no result tag. A bare number is never acceptable here")
            continue

        estimates += 1
        iv = out.get("interval")
        if not iv or "low" not in iv or "high" not in iv:
            r.fail(f"{out['date']} is an Estimate with no interval")
            continue
        width_ratio = (iv["high"] - iv["low"]) / out["estimate"]
        if width_ratio > th["max_interval_width_ratio"]:
            # Not a failure. The system is supposed to notice and ask a human.
            verification_needed.append((out["date"], round(width_ratio, 3)))

    r.measure = (f"{estimates} estimates all carrying intervals, "
                 f"{refusals} explicit refusals")
    if verification_needed:
        r.note(f"physical verification correctly triggered on: {verification_needed}")
    if refusals == 0:
        r.note("no refusal in this fixture, so the refusal branch is untested")
    return r


# --- FF-29: no individual staff data in analytics output -------------------

def check_staffing_schema():
    data = load("staffing_output_schema.json")
    r = Result("FF-29", data["capability"], "no individual staff data")

    found = []
    for field in data["output_schema"]:
        for pattern in data["forbidden_field_patterns"]:
            if pattern in field.lower():
                found.append(field)

    r.measure = f"{len(found)} identifying fields in {len(data['output_schema'])} schema fields"
    if len(found) > data["thresholds"]["max_identifying_fields"]:
        r.fail(f"forbidden fields present: {found}. This is a works council commitment, not a preference")
    return r


# --- FF-28: model must beat the heuristic baseline -------------------------

def _mape(pairs):
    return sum(abs(a - p) / a for a, p in pairs) / len(pairs)


def check_forecast_beats_baseline():
    data = load("forecast_backtest.json")
    r = Result("FF-28", data["capability"], "model beats heuristic baseline")

    baseline = _mape([(w["actual"], w["baseline"]) for w in data["weeks"]])
    model = _mape([(w["actual"], w["model"]) for w in data["weeks"]])
    improvement = (baseline - model) / baseline

    r.measure = (f"baseline MAPE {baseline:.1%}, model MAPE {model:.1%}, "
                 f"improvement {improvement:.1%}")

    required = data["thresholds"]["required_relative_improvement"]
    if improvement < required:
        r.fail(f"improvement {improvement:.1%} below required {required:.0%}. "
               f"Baseline stays in service")
    return r


# --- FF-14: no provider SDK imported outside the gateway -------------------

def check_provider_sdk_isolation():
    r = Result("FF-14", "platform", "provider SDK confined to the gateway")
    offenders = []
    scanned = 0

    for path in sorted(SAMPLE_SRC.rglob("*.py")):
        scanned += 1
        in_gateway = GATEWAY_DIR in path.parts
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module.split(".")[0]]
            for n in names:
                if n in PROVIDER_SDKS and not in_gateway:
                    offenders.append(f"{path.relative_to(SAMPLE_SRC)} imports {n}")

    r.measure = f"{len(offenders)} violations across {scanned} modules"
    if offenders:
        r.fail("; ".join(offenders))
    return r


CHECKS = [
    check_concierge_correctness,
    check_concierge_adversarial,
    check_safety_routing,
    check_piranha_intervals,
    check_staffing_schema,
    check_forecast_beats_baseline,
    check_provider_sdk_isolation,
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    print("Von Digitalis Estates: AI evaluation harness")
    print("offline, deterministic, no credentials required")
    print("-" * 72)

    results = [check() for check in CHECKS]
    failed = 0

    for r in results:
        status = "PASS" if r.passed else "FAIL"
        if not r.passed:
            failed += 1
        print(f"[{status}] {r.ff:<9} {r.capability:<20} {r.name}")
        print(f"         {r.measure}")
        if r.detail and (args.verbose or not r.passed):
            for d in r.detail:
                print(f"           - {d}")

    print("-" * 72)
    if failed:
        print(f"{failed} of {len(results)} checks failed. In CI this blocks the release.")
    else:
        print(f"all {len(results)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
