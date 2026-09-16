# Business case

*Does this platform get the Countess to 15,000 visitors a day, and does it pay
for itself on the way?*

## The honest answer first

**A platform does not grow visitor numbers. It removes the reasons people do not
come back, and it tells the estate where to spend money on the things that do.**

Tripling attendance in three years is a marketing, pricing, programming and
capital investment problem. Software contributes in three specific ways, and we
would rather name them precisely than claim the platform delivers the target.

## Where the platform actually contributes

**It replaces three unknowns with numbers.** The estate currently cannot say
which zones are popular, what a visitor is worth, or whether anyone comes back.
Three of six baselines in [1_1](../01-problem/1_1-business-goals-and-challenges.md)
are "unknown". Every investment decision the Countess makes for the next three
years is currently a guess, and phase 1 ends that. Whether anyone comes back is
answered by the ticketing platform, which computes repeat purchase rates by
cohort on a hashed purchaser identifier, and by season pass scans. Both are
aggregates. That is a coarser answer than journey analytics would give, and it
is the one the privacy position in ADR-0008 permits.

**It reduces the cost of animal care.** The brief says illness is the expensive
outcome. Earlier detection means cheaper intervention, and the welfare system is
tuned toward over-alerting precisely because the error costs are asymmetric.

**It removes friction that suppresses return visits.** Shorter queues through
better staff deployment, wayfinding that works, and an estate usable by visitors
with a disability or without German. These are not growth levers in the
marketing sense. They are the removal of reasons not to return.

## What it costs and what it must return

| | Today | Target |
|---|---|---|
| Revenue at EUR 40 yield | EUR 50 million | EUR 150 million |
| Platform operating cost | EUR 495,000 | EUR 975,000 |
| As percent of revenue | 0.99 percent | 0.65 percent |
| Capital, 18 months | EUR 2.8 million | |

**Break-even on the capital requires the platform to add roughly EUR 1.9 million
of annual value once running**, against EUR 975,000 of operating cost, to repay
EUR 2.8 million within three years.

## Is that plausible?

Three routes, with the arithmetic.

| Route | Mechanism | Annual value |
|---|---|---|
| Staff deployment | 5 percent efficiency on an estate payroll we assume near EUR 6 million | EUR 300,000 |
| Animal health | Earlier detection reducing veterinary and replacement cost | EUR 150,000 to 400,000, poorly bounded |
| **Yield per visitor** | **EUR 1 more per visitor from better wayfinding, shorter queues and accessible food and retail** | **EUR 1.25 million today, EUR 3.75 million at target** |

The third row carries the case, and it is also the one we are least able to
evidence. One euro per visitor is a small number that sounds achievable, and we
cannot prove it because nobody has ever measured yield at this estate.

So the honest position is: the business case rests on a yield improvement we
believe is conservative and cannot currently demonstrate. **Phase 1 exists to
make that number knowable.** If it turns out to be wrong, the Countess finds out
in month twelve having spent a fraction of the capital, not in year three.

## The failure condition, priced

If the estate misses the growth target, the family sells the carnivorous plant
collection. The platform does not prevent that on its own.

What it does is make the difference between missing the target while knowing why
and missing it while guessing. An estate that can see which zones are
underperforming, what a visitor is worth, and whether returning visitors are
increasing can correct course. The current estate cannot.

That is a modest claim, and we think it is the true one.

## What we are not claiming

**Not a recommendation engine that increases spend.** Phase 3 at the earliest,
and we have not modeled revenue from it.

**Not dynamic pricing yield.** Deliberately declined in
[ADR-0003](../07-decisions/ADR-0003-no-ai-in-the-revenue-path.md). It would
probably earn more than the seasonal table. We chose a smaller explicable
number.

**Not headcount reduction.** Better staff deployment means staff in the right
place, not fewer of them. An architecture proposal that quietly assumes
redundancies is making a business decision it was not asked to make, and would
also make the works council conversation considerably harder.
