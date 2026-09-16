# Risk register

Ordered by our judgment of expected harm. The mitigation column names something
that exists in the architecture, not an intention.

## High

| # | Risk | Consequence | Mitigation | Residual |
|---|---|---|---|---|
| R1 | **Connectivity is worse than assumed** | Reconciliation lag, stale telemetry, cost model wrong by a material amount | Zone authority means correctness does not depend on the link ([ADR-0002](../07-decisions/ADR-0002-zone-based-edge-architecture.md)). FF-03 and FF-05 test partition behaviour independent of the medium | Site survey outstanding. Cost line remains a placeholder |
| R2 | **No historical data means models launch unvalidated against reality** | A capability that scored well offline behaves badly in production | Heuristic baseline serves first and permanently ([ADR-0006](../07-decisions/ADR-0006-heuristic-baseline-retained-permanently.md)). Switchover only on beating the baseline over a defined window | Golden sets at launch are small and will not represent the tail |
| R3 | **Two to three person operations team is a single point of human failure** | One departure or illness leaves the estate without anyone who understands the system | Managed services preferred, FF-06 caps systems at six, FF-07 caps operational hours at six per week, FF-08 caps alerts | Knowledge concentration remains. Documentation is the only real defense and it decays |
| R4 | **Welfare alerts lose keeper trust and get ignored** | The most expensive capability becomes worthless, silently | Override rate measured (FF-30), alert budget enforced, asymmetric thresholds stated openly | A gradual loss of trust is slow to show in a monthly metric |

## Medium

| # | Risk | Consequence | Mitigation | Residual |
|---|---|---|---|---|
| R5 | Vendor cannot support offline gate validation | ADR-0012 reverses, build scope grows by roughly EUR 400,000 and six months | Hard selection criterion stated before procurement, FF-02 tests the property | Discovery happens during procurement, which is late |
| R6 | Counting bias by lighting and gate geometry | The estate invests in the wrong zone, which is the exact mistake we were hired to prevent | Monthly manual calibration per zone, correction applied per zone | Bias is systematic and stable, so it looks like real popularity |
| R7 | Yield per visitor is materially below EUR 40 | Budget and AI ceiling both move, business case weakens | Phase 1 measures it before most capital is spent | Nobody knows the real figure today |
| R8 | Provider silently changes a model behind a stable name | Capability degrades with no signal | Weekly golden set runs regardless of our own changes | Detection is days late and costs money to maintain |
| R9 | Works council agreement is not reached | Staff deployment cannot operate | Designed to have nothing to concede: aggregate only, FF-29 enforced ([ADR-0009](../07-decisions/ADR-0009-aggregate-only-staff-analytics.md)) | Agreement is still a negotiation with humans |
| R10 | Dangerous animal rules in Bavaria differ from our assumption | Incident procedures need rework | Logged as open rather than assumed | Unconfirmed |

## Low, or accepted

| # | Risk | Position |
|---|---|---|
| R11 | Revocation window allows a refunded ticket to be admitted | Accepted. Low fraud value, and the alternative is a live check that fails during outages ([ADR-0004](../07-decisions/ADR-0004-offline-verifiable-ticket-credentials.md)) |
| R12 | Model gateway is a single point of failure | Accepted. Every capability has a baseline, so the blast radius is degradation rather than outage |
| R13 | Zone Node failure removes monitoring for that zone | Accepted and documented in the degraded mode matrix. Redundant power. Only the gate zone admits, and it has a warm standby |
| R14 | Speech recognition performs worse for accented speech | Accepted with monitoring. Per language quality tracked, a failing language is disabled rather than served badly |

## Technical debt we are taking on deliberately

**Two implementations of every capability.** The heuristic baseline plus the
model, maintained indefinitely. This is the largest ongoing cost of
[ADR-0006](../07-decisions/ADR-0006-heuristic-baseline-retained-permanently.md)
and we accepted it with our eyes open.

**A cost model with a placeholder in it.** EUR 250,000 for connectivity, pending
a survey that has not happened.

**Golden sets that are too small at launch.** Three hundred concierge questions
for 15,000 visitors a day will not cover the tail. Covered by a higher sampling
rate and a conservative fallback until month four, not by pretending otherwise.

## The risk we would watch most closely

R4. It produces no error, no exception and no alert of its own. A welfare system
whose alerts are quietly ignored looks identical in every dashboard to one that
is working, and the only signal is override rate, which is why we measure it
monthly and treat a rise as a model problem rather than a compliance problem.
