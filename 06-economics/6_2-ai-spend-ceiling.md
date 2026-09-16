# The AI spend ceiling

*Why EUR 0.10 per scanned admission, what it buys, and what enforces it.*

## Why a ceiling exists at all

The Countess's problem is profitability, and the brief's failure condition is
financial. An AI feature costing more than it earns is a step toward selling the
plant collection.

At target scale, inference is the **largest single operating line** in
[6_1](6_1-cost-model.md). Treating it as something to review monthly would mean
discovering a problem after a quarter of it had already been spent.

## Where the number comes from

| Step | Value | Status |
|---|---|---|
| Yield per visitor | EUR 40 | Assumed, measured in phase 1 |
| Share of yield spent on metered inference | 0.25 percent | **A policy choice**, ours. The check below is what makes it defensible |
| **Ceiling per scanned admission** | **EUR 0.10** | 40 x 0.0025 |
| Scanned admissions per year at target | 3.75 million | Derived from the brief |
| Annual inference budget | EUR 375,000 | Derived |
| As a share of platform operating cost | 38 percent | A consequence, not an input. Read the other way, from share to ceiling, the table would be circular |

We chose a share that is **generous enough to be achievable**, which is the
point. A ceiling nobody can hit is theater, and a ceiling that forces
capabilities to be cancelled before launch is a budget decision disguised as an
architecture.

## Does it fit?

A worked check on the capability that dominates spend.

Assume a visitor has one concierge interaction of three turns. Each turn is
roughly 2,000 tokens in and 500 out.

| Routing | Cost per scanned admission | Within ceiling? |
|---|---|---|
| Every turn to a frontier model | ~EUR 0.04 | Yes, at 40 percent of the ceiling |
| Small model first, escalating on low confidence | ~EUR 0.008 | Yes, comfortably |
| Local intents handled on the Zone Node, only open ended escalates | **~EUR 0.002** | Yes, at 2 percent of the ceiling |

The ceiling is achievable even in the naive case. It becomes comfortable with
the routing decisions we made for other reasons. That headroom is deliberate: it
absorbs a provider price rise without immediately degrading service.

The figures are order-of-magnitude, based on current published pricing, and they
will be wrong within a year. The architecture is built so that being wrong is
survivable.

## How the ceiling shapes design

Four decisions exist mostly because of it.

| Decision | Effect |
|---|---|
| Local intent handling on the Zone Node | Removes most concierge traffic from paid inference entirely |
| Caching common open queries | The same question from 200 visitors costs one inference |
| Small model first, escalate on low confidence | Most queries never reach an expensive model |
| Edge inference for counting and welfare | Capital cost rather than per-call operating cost |

The last one is worth noticing. Vision workloads at 15,000 visitors a day would
be ruinous as cloud inference. At the edge they are a hardware purchase that
does not scale with visitors at all.

## The budget guard

A ceiling with no enforcement is a target. The guard meters **locally at the
gateway** from known token counts and published prices, evaluated on every call,
because a billing-driven control would leave an hour of unobserved spend and
could not enforce anything.

| Horizon | Threshold | Action |
|---|---|---|
| Monthly projection | EUR 0.08 | Degrade unprotected Tier 2 |
| Rolling 24 hour | EUR 0.09 | Degrade immediately |
| Month to date | EUR 0.095 | Hard stop, all metered inference ceases |

Every threshold sits below the EUR 0.10 ceiling, which is what makes it a cap
rather than a target. Maximum overshoot is bounded by the in-flight call set,
around EUR 4 absolute, roughly two hundred times smaller than the margin.

**Accessibility and translation hold a reserved floor**, 25 percent of the
ceiling, that the guard cannot consume. At the hard stop they continue on local
cached content at zero marginal cost. The guard degrades only the unprotected
remainder, in this order, fixed in advance:

1. Itinerary suggestions
2. Voice concierge open ended queries, to the curated FAQ
3. Demand forecasting, to the lookup table

An ordering alone would only delay the outcome. A floor does not. It would save the most money to degrade accessibility first,
which is precisely why the protection is decided now rather than by whoever is
looking at a cost overrun in eighteen months.

## What enforces it

| Check | What it does |
|---|---|
| FF-11 | Metered spend per scanned admission, on every call. Guard at 0.08, ceiling at 0.10 |
| FF-12 | Blocks any prompt or model change raising cost per interaction more than 15 percent without an ADR |
| Staging exercise | The degradation order is forced in staging and asserted, because an order never exercised is an order nobody should trust |

FF-12 is the quiet one. A ceiling is rarely broken by a single decision. It is
eroded by a series of individually reasonable changes, each slightly more
expensive than the last, and a per-change threshold is the only thing that
catches that.

## What we would do if the ceiling were wrong

If phase 1 shows yield per visitor is materially below EUR 40, the ceiling comes
down with it and capabilities get cut in the degradation order above. That is a
business decision for the Countess, and the architecture's contribution is that
it can be executed by changing a number rather than by a redesign.
