# Cost model

*Bottom up, with the arithmetic shown. The interesting result is that it did not
agree with our top down estimate.*

## What happened when we costed it properly

[A3](../01-problem/1_3-assumptions-and-constraints.md) originally assumed
**EUR 2.0 million capex**, derived top down as 3 to 4 percent of annual revenue,
which is a normal ratio for a platform at this scale.

The bottom up build came to **EUR 2.8 million**. We have revised the assumption
rather than trimming the estimate to fit, and the gap is worth understanding: the
top down ratio is drawn from businesses that already have infrastructure.
This estate has none. There is no network, no point of sale, no sensing, and no
data. A greenfield estate pays for things an established one already owns.

## Capital, 18 months

| Line | Amount | Basis |
|---|---|---|
| Build team | EUR 1,400,000 | 11 people for 18 months at EUR 85,000 fully loaded. 8 engineers, 1 architect, product and design |
| Zone Nodes | EUR 132,000 | 11 nodes at EUR 12,000: ten zones plus a warm standby at the gate. Compute, weatherproof enclosure, power, installation |
| Sensing | EUR 220,000 | 20 aquatic enclosures at 3,500; 35 terrestrial at 1,500; 40 counters at 800; 40 rides at 1,200; environmental |
| **Connectivity** | **EUR 250,000** | **Placeholder. The largest uncertainty in this model.** See [ADR-0013](../07-decisions/ADR-0013-connectivity-backhaul.md) |
| Turnstiles and point of sale | EUR 155,000 | 12 lanes at 9,000, 15 point of sale units at 3,000 |
| Ticketing platform | EUR 180,000 | License and implementation. Bought, see [ADR-0012](../07-decisions/ADR-0012-buy-ticketing-build-the-ai.md) |
| Cloud, tooling, licenses during build | EUR 80,000 | |
| **Subtotal** | **EUR 2,417,000** | |
| Contingency at 15 percent | EUR 363,000 | |
| **Total** | **EUR 2,780,000** | Round to **EUR 2.8 million** |

That is 3.7 percent of the revenue the estate will take across those 18 months,
which is at the high end of normal and defensible for a greenfield build.

## Operating cost, and why it is not flat

Operating cost scales with visitors, because inference scales with visitors.
Quoting a single annual figure would hide the thing that matters.

| Line | At 5,000/day today | At 15,000/day target |
|---|---|---|
| Cloud infrastructure | EUR 120,000 | EUR 240,000 |
| Connectivity | EUR 60,000 | EUR 60,000 |
| Ticketing platform license | EUR 90,000 | EUR 140,000 |
| **AI inference** | **EUR 125,000** | **EUR 375,000** |
| Support, maintenance, hardware replacement | EUR 100,000 | EUR 160,000 |
| **Total** | **EUR 495,000** | **EUR 975,000** |

Inference at target: 3.75 million visitors at the EUR 0.10 ceiling is EUR
375,000. At today's 1.25 million visitors it is EUR 125,000.

**AI is the largest single operating line at target scale.** That is the entire
justification for treating the ceiling as a design constraint rather than as a
monthly report. See
[6_2](6_2-ai-spend-ceiling.md) and
[ADR-0014](../07-decisions/ADR-0014-ai-spend-ceiling-and-budget-guard.md).

## Against revenue

| | Today | Target |
|---|---|---|
| Visitors per year | 1.25 million | 3.75 million |
| Revenue at EUR 40 yield | EUR 50 million | EUR 150 million |
| Platform operating cost | EUR 495,000 | EUR 975,000 |
| **Cost as percent of revenue** | **0.99 percent** | **0.65 percent** |

The ratio improves with scale because most of the platform is fixed. That is the
economic argument for the whole build: the estate pays roughly one percent of
revenue now and less than that later.

## What this model is soft on

Three things, stated rather than buried.

**Connectivity is a placeholder.** EUR 250,000 is a working figure pending a site
survey. It could plausibly be half or double that, and it is the single line most
likely to move the total.

**Yield per visitor is assumed, not measured.** EUR 40 covering admission, food,
beverage and retail is our figure, not the Countess's. The estate has no
instrumentation, so nobody currently knows the real number. Phase 1 exists partly
to find out, and if it is materially different, both the budget and the AI
ceiling move with it.

**Team cost assumes a blended European rate.** A different delivery model
changes the largest line in the capital table by a lot.

## The number we would defend hardest

Not the total. The **EUR 0.10 per scanned admission AI ceiling**, because it is the only
line that is simultaneously the largest operating cost, entirely outside our
control, and capable of changing by an order of magnitude on somebody else's
pricing decision.

Everything else in this model is an estimate that will be wrong by some
percentage. That one is an estimate that can be wrong by a multiple, which is
why it has a runtime guard attached rather than a review meeting.
