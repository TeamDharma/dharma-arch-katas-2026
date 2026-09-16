# ADR-0014: AI spend ceiling with a runtime budget guard

## Status

Accepted

## Context

The Countess's problem is profitability. The brief's stated failure condition is
financial: miss the target and the family sells the plant collection.

An AI feature that costs more than it earns is therefore not a neutral addition,
it is a step toward the failure condition. Model pricing is also outside our
control and changes without notice.

Most architectures treat inference cost as something to review monthly. At
15,000 visitors a day, a concierge conversation of three turns at around two
thousand tokens each is a recurring bill that can move by an order of magnitude
on somebody else's pricing decision.

Alternatives considered:

- **Monitor and review monthly.** The normal approach. It discovers overspend
  after it has happened and relies on a human to act.
- **Hard per call rate limits.** Predictable, and it fails visitors arbitrarily
  rather than degrading coherently.
- **A ceiling expressed per scanned admission, enforced at runtime by degrading
  capabilities in a predetermined order.**

## Decision

**Metered vendor inference is capped at EUR 0.10 per scanned admission, per
calendar month.** It is a hard cap, and every threshold that acts on it sits
strictly below it. An earlier version of this ADR had a 24 hour threshold of
EUR 0.09 while claiming a EUR 0.10 cap, which is not a cap. Adversarial review
caught it and it was our error, introduced while fixing something else.

### How the number is set

The input is a policy choice. The arithmetic that follows from it is derived,
and the table says which is which. The share of operating cost at the bottom
is a consequence of the ceiling, not a source for it. Read the other way, from
share to ceiling, the table would be circular, and the adversarial review's
finding that the number was invented rests on exactly that reading.

| Input | Value | Status |
|---|---|---|
| Yield per visitor | EUR 40 | Assumed, unmeasured until phase 1, [A2](../01-problem/1_3-assumptions-and-constraints.md) |
| Share of yield the estate will spend on metered inference | **0.25 percent** | **Policy choice.** Set so that the naive routing case in [6_2](../06-economics/6_2-ai-spend-ceiling.md), every turn to a frontier model at about EUR 0.04, fits with two and a half times headroom for a provider price rise |
| **Ceiling per scanned admission** | **EUR 0.10** | 40 x 0.0025 |
| Scanned admissions per year at target | 3.75 million | 15,000/day x 250 operating days |
| Annual inference budget at target | EUR 375,000 | Derived, 0.10 x 3.75 million |
| Share of platform operating cost | 38 percent | A consequence, 375,000 / 975,000. Not an input |
| Degradation threshold | EUR 0.08 | 80 percent of ceiling, leaving 20 percent to absorb reaction time |
| Accessibility reservation | EUR 0.025, 25 percent | Sized below |

The admission forecast is conservative in the right direction: if attendance
falls short, spend per admission rises and the guard acts earlier. If yield
turns out lower, the ceiling moves with it and the routing check in 6_2 says
how much room remains. The 0.25 percent is ours, not the Countess's, and
[2_6](../02-requirements/2_6-claim-confidence.md) files the ceiling as a
conventional default rather than a derivation.

### Metering is local, not billing-driven

The gateway meters in real time from known token counts and published prices.
**Provider billing is reconciliation, not the control input.**

This matters more than it sounds. Waiting on provider billing would leave a
blind window of up to an hour, during which peak-rate spend could run to several
hundred euros before any threshold moved. That gap is larger than the margin
between the guard and the ceiling, so a billing-driven control could not enforce
the cap at all. Local metering reduces the blind window to the set of in-flight
calls.

### Thresholds, all below the ceiling

| Horizon | Threshold | Action |
|---|---|---|
| Month to date, projected to month end by linear extrapolation of the trailing 7 day rate | EUR 0.08 | Degrade unprotected Tier 2, in order |
| Rolling 24 hour | EUR 0.09 | Degrade immediately, regardless of the monthly projection |
| Month to date, actual | **EUR 0.095** | **Hard stop. All metered inference ceases** |

The accounting period is a calendar month, and the reservation replenishes
daily within it.

### What happens at the hard stop

Every metered call stops. The system does not stop.

| Layer | At hard stop |
|---|---|
| Tier 0 deterministic floor | **Unaffected.** No metered inference is in it |
| Unprotected Tier 2 | Already degraded, curated content and static routes |
| **Accessibility and translation** | **Continues on local cached content**: reference translations, recorded audio description, step free routing. Zero marginal cost |
| Tier 1 and 3 | Heuristic baselines, which are not metered |

This resolves a trilemma adversarial review identified: we were claiming a
protected floor, that accessibility sat last in the shutdown queue, and a total cap, and under
unbounded protected demand all three cannot hold.

They can hold once the protected service has a **non-metered terminal mode**.
Accessibility never goes dark. Beyond the budget it is served from content that
was paid for as capital, which is exactly why
[ADR-0006](ADR-0006-heuristic-baseline-retained-permanently.md) keeps every
baseline permanently.

**The denominator is an admission scanned at a turnstile**, not a ticket sold,
not a unique credential, and not estimated footfall. Tickets sold but unused
would flatter the figure. Footfall is an estimate and a budget should not be
denominated in one.

**The scope is metered vendor billing**, not the total cost of a capability.
Edge inference is capital expenditure and sits outside this control, as do
engineering, evaluation, monitoring and baseline maintenance. Those appear in
[6_1](../06-economics/6_1-cost-model.md). This ceiling answers "what are we
spending with model providers", which is the cost that is volatile and outside
our control. It does not answer "does this capability earn its keep".

**Accessibility and translation hold a reserved floor**, not a place at the end
of a shutdown queue.

| Property | Value |
|---|---|
| Reservation | 25 percent of the ceiling, EUR 0.025 per scanned admission |
| Replenishment | Daily |
| Borrowing | Unprotected capabilities may **not** borrow from the reservation. The reservation may borrow from unused unprotected budget |
| If protected demand exceeds the reservation | Extended from unprotected budget, degrading unprotected capabilities further |
| If all budget is exhausted | **Local cached content, zero marginal cost.** Never dark |

**How 25 percent was sized.** Assume 15 percent of visitors need translation or
audio description, at roughly twice the interaction volume of a general visitor,
and at similar cost per interaction. That is 0.15 x 2 = 0.30 of a general
visitor's share, which we round down to 0.25 because a meaningful part of the
demand is served from cached reference content at no marginal cost.

Every input in that line is an estimate, and the visitor mix in particular is
unmeasured until phase 1. It is recorded in
[2_6](../02-requirements/2_6-claim-confidence.md) as a conventional default
rather than a derivation. What is not an estimate is the priority it encodes. The guard degrades only the unprotected remainder, in
this order:

1. Itinerary suggestions
2. Voice concierge, open ended queries, to the curated FAQ
3. Demand forecasting, to the lookup table

An ordering alone would have meant that sustained pressure eventually reaches
accessibility. A floor means it does not.

## Consequences

+ Cost becomes a design input rather than a monthly surprise, and it shapes real
  decisions: local intent handling, caching, and small-model-first routing all
  exist because of this ceiling.
+ A provider price rise degrades service predictably instead of producing an
  unexpected invoice. QS-12 exercises exactly this.
+ The degradation order is decided calmly in advance rather than by whoever is
  looking at a cost overrun, which is why accessibility is protected.
+ It makes metered vendor spend attributable per capability, which is the input
  to a capability economics question this control does not itself answer.
− Visitors may experience reduced service for reasons entirely invisible to them.
− The ceiling is our estimate, not the Countess's budget. If yield per visitor
  is materially different from our assumption, the number moves.
− The guard is a component to build and to operate, and a bug in it could
  degrade capabilities unnecessarily.
− **The control measures one cost category.** Calling it a capability economics
  mechanism would be overreach, and an earlier draft of this ADR came close to
  doing so.
− **Budget consumed in the morning is not available to afternoon visitors.** We
  accept a coarse control over an unfair one: the guard degrades a capability for
  everyone rather than refusing individual visitors, so nobody is denied service
  because of when they arrived. The 24 hour threshold limits how far one day can
  run ahead of the month.
− **The cap binds metered inference, not the estate's experience.** At the hard
  stop the estate still sells tickets, admits visitors, monitors welfare on
  thresholds, answers common questions from cache and serves accessibility from
  local content. What stops is spending money with a model provider.
− The reserved accessibility floor is a fixed allocation, so in an extreme
  overrun it protects accessibility by degrading everything else further than
  an ordering alone would have.

## Verification

FF-11 meters locally at the gateway and evaluates all three thresholds above on
every call, not on a schedule. Spend is known at the moment it is incurred.

**Maximum overshoot, quantified.** At the hard stop, calls already dispatched
cannot be recalled. The bound is:

```
overshoot = max_concurrent_calls x max_cost_per_call
          = 200 x EUR 0.02
          = EUR 4 absolute
```

Across a day at target attendance that is under EUR 0.0003 per admission, which
is why the hard stop sits at EUR 0.095 rather than at EUR 0.10. The margin is
roughly two hundred times the bound.

This is only true because metering is local. Under billing-driven metering the
overshoot would be an hour of unobserved peak spend, which the margin could not
absorb, and the cap would be decorative.

FF-11 is validated against four scenarios in staging: a tenfold provider price
increase, a holiday attendance spike, one language consuming disproportionate
traffic, and sustained abuse of the open ended concierge path. Each must end
with total spend inside the cap and accessibility still serving.

FF-12 blocks any pull request touching a prompt or model that increases cost per
interaction by more than 15 percent without an ADR. That is the check that stops
the ceiling being eroded by a series of individually reasonable changes.

The degradation order is tested by forcing the guard in staging and asserting
the order, because an ordering that has never been exercised is an ordering
nobody should trust. The same exercise asserts that the accessibility floor
holds when every other capability has been degraded.

Adversarial review of this ADR, and our response, is in
[../09-ai-disclosure/reviews/findings.md](../09-ai-disclosure/reviews/findings.md).
