# Fitness functions

An architecture characteristic that nothing checks is a preference. This file
turns each of the seven characteristics in
[2_3-architecture-characteristics.md](2_3-architecture-characteristics.md) into
something automated, with a number attached and a stated consequence when the
number is missed.

Two rules we held ourselves to. Every characteristic has at least one fitness
function, and every fitness function has an owner, a frequency, and a defined
failure action. A check that nobody acts on is theater.

## Platform fitness functions

| ID | Characteristic | Check | Threshold | Frequency | On failure |
|---|---|---|---|---|---|
| FF-01 | Availability | Synthetic admission transaction against each zone turnstile | 99.95% success during opening hours | Every 60s per zone | Page on-call, zone falls back to offline credential validation |
| FF-02 | Availability | Revenue path smoke test with all cloud dependencies stubbed out | 100% pass | Every deploy | Block release |
| FF-03 | Partition tolerance | Automated network partition of one zone in staging, assert declared degraded behavior | All Tier 0 and Tier 1 capabilities behave as documented | Nightly | Block release |
| FF-04 | Partition tolerance | Degraded mode matrix completeness check | Zero blank cells | Every commit touching the matrix | Build fails |
| FF-05 | Partition tolerance | Reconciliation correctness after a simulated four hour outage | Zero lost admissions, zero duplicate charges | Weekly | Block release |
| FF-06 | Operability | Count of distinct systems requiring routine human operation | 6 or fewer | Monthly review | Architecture review before adding the seventh |
| FF-07 | Operability | Scheduled operational hours per week in steady state | Under 6 hours | Monthly | Automate or remove the offending system |
| FF-08 | Operability | Alert volume reaching a human | Under 20 per week, under 2 out of hours | Weekly | Tune or delete the alert. An ignored alert counts as a failure |
| FF-09 | Auditability | For a sampled regulated record, reconstruct every change with actor, timestamp and evidence | 100% reconstructable | Weekly sample of 20 | Treat as a compliance incident |
| FF-10 | Auditability | Retention policy conformance, fiscal versus behavioral data | Zero behavioral records past their lifecycle, zero fiscal records deleted early | Monthly | Block, escalate to DPO |
| FF-11 | Affordability | Metered spend per **scanned admission**, metered locally at the gateway, evaluated on every call | Monthly projection above EUR 0.08, rolling 24 hour above EUR 0.09, or month to date above EUR 0.095 | Every call | Degrade unprotected Tier 2, then hard stop. Accessibility continues on local cached content at zero marginal cost |
| FF-12 | Affordability | Cost regression on any prompt or model change | No change increases cost per interaction by more than 15% without an ADR | Every PR touching a prompt | Block merge |
| FF-13 | Evolvability | Provider substitution rehearsal for one capability, chosen at random | Completed in under 2 days, excluding re-embedding | Quarterly | Raise as a risk, fix the seam |
| FF-14 | Evolvability | No direct model provider SDK imported outside the model gateway | Zero violations | Every commit | Build fails |

**The six systems FF-06 counts.** A system is anything with its own upgrade
cycle, its own credentials and its own way of failing that a person has to
watch. On that rule the count is:

| # | System | Instances |
|---|---|---|
| 1 | Zone Node fleet: broker, edge runtime, local store, sync agent, local concierge, zone ops view | Ten, plus the gate standby, one software image |
| 2 | Field device fleet: sensors, counters, turnstiles, point of sale units | About 400, batteries and calibration |
| 3 | Bought ticketing and point of sale platform, and our integration with it | Vendor operated, integration ours |
| 4 | Cloud application runtime: gateway, assurance plane, experience orchestration, forecasting, ops console, register | One managed runtime |
| 5 | Managed data platform: event backbone and lakehouse | One managed offering |
| 6 | Managed identity for staff | One |

The count is six only because the cloud is one managed runtime and the data
platform is one managed offering. The day either is self hosted, or a second
broker appears between cloud containers, it is seven, and FF-06 exists to make
that a review rather than a drift.

FF-14 is the cheapest high value check in the list. It is a static import rule,
it takes minutes to write, and it is what actually keeps the evolvability
promise honest over three years. Architectural intent that is not enforced
decays quietly.

## AI fitness functions

Every check in this section serves **Testability**, the fourth characteristic in
[2_3](2_3-architecture-characteristics.md). It is the only characteristic with
no dedicated platform level check, because the entire block below is its check:
testability for this architecture means being able to demonstrate that
model-backed components behave, and that is what these do.

They sit alongside the platform checks and are graded by tier. Tier decides
how hard the bar is, following the model in the characteristics document.

| ID | Capability | Check | Threshold | Frequency | On failure |
|---|---|---|---|---|---|
| FF-20 | All AI capabilities | Every capability has a golden dataset, a threshold, and a CI evaluation run | 100%, no exceptions | Every commit | Build fails. A capability without an eval cannot ship |
| FF-21 | Voice concierge | Answer correctness against golden set of 300 visitor questions | 95% correct, 0% confidently wrong on safety topics | Every prompt or model change | Block release |
| FF-22 | Voice concierge | Adversarial suite: prompt injection, jailbreak, off-topic coercion | 0 successful policy violations out of 200 attempts | Every release, and weekly in production shadow | Block release, fall back to static content |
| FF-23 | Voice concierge | Speech recognition error injection, compounded with model response | Correctness holds above 90% at 10% word error rate | Weekly | Investigate the two stage pipeline, not just the model |
| FF-24 | Animal welfare, aquatic | False negative rate on withheld historical incidents | Under 2%. False negatives cost an animal, false positives cost a vet visit | Weekly | Lower the alert threshold. We accept more false positives here by design |
| FF-25 | Animal welfare, terrestrial | Same, with per-species breakdown | Under 2% overall, no species above 5% | Weekly | Species specific retraining or fall back to schedule based inspection |
| FF-26 | Piranha population | Output is a tagged type: every `Estimate` carries an interval, every non-estimate is an explicit `MeasurementUnavailable` with a reason | 100% of outputs are one or the other. A bare number fails | Every run | Build fails. This one is non-negotiable |
| FF-27 | Piranha population | Interval width | Under 15% of the estimate, else trigger physical verification | Daily | Manual count, and log the discrepancy against the model |
| FF-28 | Demand forecasting | Accuracy versus the heuristic baseline | Model must beat baseline by 10% MAPE or the baseline stays in service | Weekly | Revert to heuristic. The baseline is never deleted |
| FF-29 | Staff deployment | Output contains no individual level staff data | Zero personally identifying fields, verified by schema assertion | Every commit and every run | Build fails. This is a works council commitment, not a preference |
| FF-30 | All Tier 1 capabilities | Human override rate and override reasons are logged and reviewed | Override rate above 20% triggers a model review | Monthly | Investigate. A high override rate means the model is not earning its place |
| FF-31 | All AI capabilities | Input distribution drift against the training window | Population stability index under 0.2 | Daily | Alert, shadow evaluate, consider reverting to baseline |
| FF-32 | All AI capabilities | Output sampling reviewed by a human. **Tier 2:** 50 per capability per week, by the technical team. **Tier 1:** 20 per capability per week, by the domain owner who already reviews its alerts, inside the override process, plus an independent 5 per capability per month by the technical team, so the people acting on an output are not the only people reviewing it. **Tier 3:** 10 per month, by estate management | Every sample reviewed and scored | Weekly | Any systematic problem opens an incident |
| FF-33 | Piranha population | **Prediction interval coverage** against independent physical counts. One sided lower Wilson bound, temporal holdout, strata across every conditioning dimension | Minimum 120 paired observations, 30 per stratum. **Lower bound must exceed 0.90** against a nominal 0.95 | Per calibration cycle | Below the sample minimum the capability is labelled provisional. Below the bound it recalibrates or reverts to physical counts |
| FF-34 | Piranha population | Refusal rate outside calibrated conditions | 100% of out of distribution observations return "measurement unavailable" rather than an interval | Per run | Build fails |
| FF-35 | Accessibility and translation | Reserved floor intact after the guard has degraded everything else, **and local content still serving after the hard stop** | Floor never consumed. Accessibility never dark | Staging exercise, per release, under four adverse scenarios | Block release |
| FF-36 | Voice concierge | **Safety routing recall.** Every question in the safety golden set, and a paraphrase set written to defeat a keyword list, must end at curated content by either the classifier or the lexical net. Classifier-only misses are counted | 100 percent routed. The classifier-only miss count is reported, and a rise in it triggers classifier retraining | Every prompt, model or classifier change, and weekly | Block release. A safety question reaching generation is the failure the router exists to prevent |

## Three of these deserve explanation

**FF-24 and FF-25 set an asymmetric bar on purpose.** A false negative on a sick
animal costs an animal, and the brief says animal illness is the expensive
outcome. A false positive costs a veterinary visit. Those are not equivalent,
so we tune toward over-alerting and we say so rather than optimizing a symmetric
accuracy number that hides the trade.

**FF-33 is a non-inferiority test, not a difference test.** An earlier version
asked whether a confidence bound contained 0.95, which a badly under-covering
model passes whenever the sample is small enough to make the bound wide. That
rewards weak evidence. It now asks whether the lower bound clears a stated
minimum acceptable coverage of 0.90, which is a question small samples cannot
answer by accident.

**FF-33 exists because FF-26 was not enough.** FF-26 checks that an interval is
present. Adversarial review pointed out that a structurally valid but badly
calibrated interval passes it, which is correct and was a real gap. FF-33
measures whether nominal 95 percent intervals actually contain the truth 95
percent of the time. A check on the shape of an output is not a check on its
honesty.

**FF-36 exists because the safety router is a model.** Safety questions are
kept from generation by a router, the router is a classifier, and a classifier
misses paraphrases. So the router has a second, non-statistical signal beside it, and
a fitness function that measures how often the classifier alone would have
failed. The number to watch is not the pass rate, which must be total. It is
the count the second signal caught.

**FF-26 forbids a bare number.** Counting jumping piranhas in murky water is not
reliably solvable with a camera. Any system that reports "247 piranhas" is
lying with more confidence than the evidence supports. Reporting an interval,
and alerting on trend rather than absolute value, is the honest design and it
makes the failure mode visible instead of silent.

**FF-28 keeps the baseline alive permanently.** The heuristic is how we solve
cold start with no historical data, and it is also the fallback for every
subsequent failure. Deleting it once the model works would remove the thing
that makes the model safe to deploy.

## What we did not write fitness functions for

We have no automated check for whether the architecture is understandable, and
we could not think of an honest one. The diagram legend, the reading paths in
the README, and this document are our attempt, but the only real test is
whether a reader who has never met us can follow it. We are aware that is
exactly what the judges are about to do.
