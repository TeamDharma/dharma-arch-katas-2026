#!/usr/bin/env python3
"""Internal consistency checks over the architecture document set.

This repository claims that every requirement traces to a verification method,
that every AI capability declares a tier, a fallback and a verification, and
that the degraded mode matrix has no gaps. Those are checkable claims, so they
are checked here rather than asserted.

Standard library only.

Usage:
    python3 09-ai-disclosure/checks/check-architecture.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
REQ = ROOT / "02-requirements"
ARCH = ROOT / "03-architecture"
SCEN = ROOT / "04-ai-scenarios"
ADR = ROOT / "07-decisions"


def read(p):
    return p.read_text()


def md_files():
    return [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]


# --- 1. Every fitness function cited anywhere actually exists ---------------

def defined_ffs():
    text = read(REQ / "2_4-fitness-functions.md")
    return set(re.findall(r"\|\s*(FF-\d+)\s*\|", text))


def check_ff_references():
    defined = defined_ffs()
    missing = {}
    for p in md_files():
        if p.name == "2_4-fitness-functions.md":
            continue
        for ff in set(re.findall(r"\bFF-\d+\b", read(p))):
            if ff not in defined:
                missing.setdefault(ff, []).append(str(p.relative_to(ROOT)))
    hits = [f"{ff} cited in {', '.join(sorted(files))} but not defined in 2_4"
            for ff, files in sorted(missing.items())]
    return f"fitness function references ({len(defined)} defined)", hits


# --- 2. Every requirement names a verification method -----------------------

def check_requirement_verification():
    text = read(REQ / "2_1-functional-requirements.md")
    hits = []
    count = 0
    for row in re.findall(r"^\| (FR-\d+) \|.*$", text, re.M):
        pass
    for line in text.splitlines():
        m = re.match(r"^\| (FR-\d+) \|", line)
        if not m:
            continue
        count += 1
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not cells[4]:
            hits.append(f"{m.group(1)} has no verification method")
    return f"requirement verification ({count} requirements)", hits


# --- 3. Every ADR referenced exists ----------------------------------------

def check_adr_references():
    existing = {p.name.split("-")[0] + "-" + p.name.split("-")[1]
                for p in ADR.glob("ADR-*.md")}
    hits = []
    for p in md_files():
        for adr in set(re.findall(r"\bADR-\d{4}\b", read(p))):
            if adr not in existing:
                hits.append(f"{adr} referenced in {p.relative_to(ROOT)} but no such file")
    return f"ADR references ({len(existing)} ADRs)", sorted(set(hits))


# --- 4. Every AI scenario declares tier, fallback and verification ----------

def check_scenario_completeness():
    """The repository's own stated rule: tier, fallback, verification, or it
    does not appear. This makes that rule mechanical."""
    hits = []
    folders = [d for d in SCEN.iterdir() if d.is_dir()]
    for d in sorted(folders):
        readme = d / "README.md"
        if not readme.exists():
            hits.append(f"{d.name} has no README.md")
            continue
        text = read(readme).lower()
        for required in ("tier", "fallback", "verification"):
            if required not in text:
                hits.append(f"{d.name} does not state its {required}")
    return f"scenario completeness ({len(folders)} capabilities)", hits


# --- 5. Degraded mode matrix has no empty cells ----------------------------

def check_degraded_matrix():
    """FF-04 fails the build on a blank cell. This is that check."""
    text = read(ARCH / "3_8-degraded-mode-matrix.md")
    rows, hits = 0, []
    for line in text.splitlines():
        if not line.startswith("| ") or "---" in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 8:          # capability, tier, C1..C6
            continue
        if cells[0] in ("Capability", "Code"):
            continue
        rows += 1
        for i, c in enumerate(cells):
            if not c:
                hits.append(f"row {cells[0]!r} has an empty cell at column {i + 1}")
    if rows == 0:
        hits.append("no matrix rows parsed, the table shape may have changed")
    return f"degraded mode matrix ({rows} capabilities)", hits


# --- 6. Every characteristic has at least one fitness function -------------

def check_characteristics_covered():
    text = read(REQ / "2_3-architecture-characteristics.md")
    chars = re.findall(r"^### \d+\. (.+)$", text, re.M)
    ff_text = read(REQ / "2_4-fitness-functions.md")
    hits = []
    for c in chars:
        key = c.split()[0].lower().rstrip(",")
        if key not in ff_text.lower():
            hits.append(f"characteristic '{c}' has no fitness function mentioning it")
    return f"characteristic coverage ({len(chars)} characteristics)", hits


# --- 7. Headline numbers are stated consistently --------------------------

def check_number_consistency():
    """A number repeated across seventy documents drifts. These are the ones
    that would be embarrassing to contradict ourselves on."""
    expectations = {
        r"EUR 0\.10 per scanned admission": "AI spend ceiling",
        r"EUR 2\.8 million": "capital budget",
        r"15,000": "visitor target",
        r"5,000": "visitors today",
    }
    contradictions = {
        r"EUR 2\.0 million capital": "old capital figure, superseded",
        r"EUR 600,000 per year": "old flat opex figure, superseded",
        r"EUR 0\.10 per visitor": "ceiling denominated per visitor, superseded by scanned admission in ADR-0014",
        r"translation, last\b": "accessibility in the shutdown queue, superseded by the reserved floor in ADR-0014",
        r"\b[Dd]egrade[sd]? last\b": "accessibility in the shutdown queue, superseded by the reserved floor in ADR-0014",
    }
    hits = []
    for pattern, label in expectations.items():
        found = any(re.search(pattern, read(p)) for p in md_files())
        if not found:
            hits.append(f"{label}: no document states it any more")
    for pattern, label in contradictions.items():
        for p in md_files():
            if "reviews" in p.parts:      # verbatim and quoted review text
                continue
            if re.search(pattern, read(p)):
                hits.append(f"{p.relative_to(ROOT)} still contains {label}")
    return "headline number consistency", hits


CHECKS = [
    check_ff_references,
    check_requirement_verification,
    check_adr_references,
    check_scenario_completeness,
    check_degraded_matrix,
    check_characteristics_covered,
    check_number_consistency,
]


def main():
    print("architecture consistency checks")
    print("-" * 70)
    failed = 0
    for check in CHECKS:
        name, hits = check()
        if hits:
            failed += 1
            print(f"[FAIL] {name}: {len(hits)}")
            for h in hits[:12]:
                print(f"         {h}")
        else:
            print(f"[PASS] {name}")
    print("-" * 70)
    print("architecture is internally consistent" if not failed
          else f"{failed} check(s) failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
