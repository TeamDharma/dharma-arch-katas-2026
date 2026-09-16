# ADR-0006: Retain the heuristic baseline permanently

## Status

Accepted

## Context

The estate is greenfield. There is no attendance history, no machine readable
feeding record, no labeled imagery and no visitor interaction data. Every model
we propose starts with nothing to learn from.

Separately, every AI capability needs something to fall back to when a provider
fails, an evaluation threshold is breached, drift is detected, or the cost
ceiling is reached.

We noticed these are the same problem. A rule based implementation built from
domain knowledge solves cold start, and the same implementation is the natural
fallback afterward.

Alternatives considered:

- **Wait for data before shipping anything.** The Countess needs revenue on
  the new system by month six. Not viable.
- **Ship models trained on transferred or synthetic data, no rules layer.**
  Faster to something impressive, and it leaves every capability with nothing
  to degrade to.
- **Rules first, model replaces rules once it demonstrably wins, rules deleted.**
  Solves cold start, leaves the same fallback gap a year later.
- **Rules first, model serves when it wins, rules retained permanently.**

## Decision

Every AI capability ships first as an explicit heuristic baseline built from
domain knowledge and external signals. A model replaces it in service only when
it beats the baseline by a defined margin over a defined window.

**The baseline is never deleted.** It remains the fallback for every failure
mode, and the control against which the model's continued value is measured.

## Consequences

+ Capabilities ship in phase 1 without data, and the estate gets value before it
  gets sophistication, which is the right order for a business that needs
  revenue first.
+ Every graceful degradation in the architecture has somewhere real to degrade
  to.
+ It gives a permanent answer to "is the model worth its cost", because the
  comparison never goes away.
+ Data collected while the baseline serves is what trains the model that
  replaces it.
− **Two implementations of every capability, maintained indefinitely.** For a two
  to three person operations team this is a real and recurring burden, and it is
  the largest ongoing cost of this decision.
− Delivery is slower. Capabilities that could ship as models in phase 1 ship as
  rules instead and the model arrives in phase 2.
− In year two the rules will look like legacy and someone will propose deleting
  them. This ADR exists partly to be found by that person.

## Verification

FF-28 compares model against baseline weekly for demand forecasting, and reverts
automatically when the model loses. Equivalent comparisons exist per capability.

The retention itself is verified structurally: the degraded mode matrix
(FF-04) has no blank cells, and most of those cells name the baseline. If a
baseline were deleted, the matrix would develop a blank and the build would
fail.

That is deliberate. We wanted the consequence of deleting a baseline to be a
failing build rather than a discovery during an outage.
