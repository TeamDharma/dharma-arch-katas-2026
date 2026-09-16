# Production monitoring and drift

*Offline evaluation tells you about the inputs you thought of. This page is
about the rest.*

## What we watch

Four signals per capability, all of them cheap, none of them optional.

| Signal | What it catches | Frequency | Threshold |
|---|---|---|---|
| **Input drift** | The world moved. New species, new enclosure, new visitor demographics, a season nobody trained on | Daily | Population stability index above 0.2 (FF-31) |
| **Output sampling** | Systematic wrongness that no automated score noticed | Weekly. 50 per Tier 2 capability by the technical team, 20 per Tier 1 capability by the human already in its loop plus an independent 5 a month by the technical team, 10 a month for Tier 3 | Any systematic pattern opens an incident (FF-32) |
| **Human override rate** | The model is not earning its place, and nobody said so | Monthly | Above 20 percent triggers model review (FF-30) |
| **Cost per capability** | Silent economic failure | Hourly | Guard at EUR 0.08 per scanned admission, ceiling EUR 0.10 (FF-11) |

## Drift, specifically

Drift is the failure mode that has no error message. Nothing throws, nothing
alerts, the dashboard is green, and the answers get slowly worse.

We watch three kinds, because they have different causes and different fixes.

**Input drift.** The distribution of what arrives changes. A new enclosure
opens, an animal is rehoused, an unusually wet summer changes visitor patterns.
Detected by comparing live input distributions against the training window.

**Concept drift.** The inputs look the same but the correct answer has changed.
A species ages and its normal activity band shifts. The old thresholds are now
wrong for an animal that is perfectly healthy. Detected only through outcome
comparison, which is why keeper override rate matters so much for welfare.

**Provider drift.** The one people forget. A provider updates a model behind a
stable name and behavior changes with no deployment on our side. Detected by
running the golden set on a schedule rather than only on our own changes, so a
score shift with no commit of ours points straight at the provider.

Provider drift is the reason our golden sets run **weekly regardless of
whether anything changed**, which is not free but is the only way to see a
change we did not make.

## What happens automatically

| Observation | Automatic response |
|---|---|
| Drift index above threshold | Shadow evaluation starts, alert raised |
| Shadow evaluation below acceptance threshold | Capability reverts to heuristic baseline |
| Golden set score drops with no deployment on our side | Pin to last known good model version, alert |
| Cost guard reached | Tier 2 capabilities degrade in a defined order |
| Override rate above 20 percent | Model review scheduled, capability keeps running |
| Adversarial attempt succeeds in production | Attempt added to corpus, capability reverts to curated content pending fix |

Reversion is automatic in four of six cases. That is deliberate: a two to three
person team cannot be the mechanism by which a degraded model is taken out of
service at two in the morning.

## Observability for the AI parts

The model gateway is the instrumentation point, which is why everything routes
through it. For every call it records: capability, model version, prompt
version, input and output, token counts, cost, latency, cache hit, and the
evaluation score where one applies.

That record serves three purposes at once, which is why it is worth its storage
cost: it is the evaluation corpus, the cost ledger, and the audit trail the AI
Act expects a deployer to keep. See
[5_7-ai-act-obligations.md](5_7-ai-act-obligations.md).

## Retention of model logs

Model inputs and outputs can contain personal data, particularly for the
concierge. They are kept for 90 days for evaluation and incident investigation,
then aggregated and the raw records deleted, except where a record forms part of
a regulated decision trail, in which case it follows the animal register's
retention.

This is a deliberate tension with wanting a large evaluation corpus. We resolved
it toward minimization, because the alternative is retaining visitor speech
indefinitely on the argument that it might be useful, which is exactly the
argument GDPR exists to refuse.

## The alert budget

Everything above produces alerts, and alerts are where good monitoring goes to
die. FF-08 caps them at under 20 per week and under 2 out of hours.

That cap is binding, not aspirational. If a new capability's monitoring would
breach it, either the monitoring is tuned or the capability does not ship. An
alert nobody reads is worse than no alert, because it produces the appearance of
coverage.

Outside opening hours, only Tier 0 and animal welfare page a human. Everything
else waits until morning, because nothing else in this system gets worse for
waiting eight hours, and a team of three needs to sleep.
