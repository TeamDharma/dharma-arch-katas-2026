# Business goals and challenges

*arc42 section 1. What success looks like for the Countess, in her terms and
then in measurable ones.*

## The goal behind every other goal

The estate must become profitable. The brief states the failure condition
plainly: miss the growth target and the family sells the carnivorous plant
collection, and the fallback is returning to the garden gnome business.

That framing matters architecturally. It means a feature that costs more than it
earns is not a neutral addition, it is a step toward the failure condition. It
is the direct reason AI inference carries a hard ceiling of EUR 0.10 per scanned admission
rather than a budget review.

## Goals, made measurable

| Her goal | Measure | Baseline | Target |
|---|---|---|---|
| Grow visitor numbers | Visitors per day, annual average | 5,000 | 15,000 within three years |
| Make the estate profitable | Yield per visitor, and platform cost per visitor | Unknown, no instrumentation exists | Yield growing faster than cost |
| Know what is popular | Proportion of zones with reliable occupancy data | 0 percent | 100 percent by end of phase 1 |
| Deploy staff well | Proportion of shifts planned against demand rather than habit | 0 percent | Majority by end of phase 2 |
| Healthy and happy animals | Veterinary interventions, and time from onset to detection | Unknown | Detection time falling year on year |
| More returning visitors | Repeat purchase rate by cohort, computed inside the ticketing platform on hashed purchaser identifiers, aggregate only, plus season pass scans | Unknown | Measurable by end of phase 1, improving by phase 3 |

Three of six baselines are "unknown", and that is the most important fact on
this page. The estate cannot currently tell whether it is succeeding. Phase 1 is
mostly about replacing those unknowns with numbers, which is why instrumentation
precedes intelligence in our roadmap.

## The challenges she named

**"We have no real idea what parts of the estates are most popular, so it is
difficult to know where to invest and deploy staff."**

This is a measurement problem before it is an AI problem. Anonymous edge
counting per zone answers most of it without any model at all. Forecasting adds
value only once there is history to forecast from, which is phase 2.

**"Looking after the animals is costly, even more so if they get sick. So we
want healthy and happy animals."**

The economic argument is early detection. The architectural consequence is that
false negatives cost far more than false positives, so welfare monitoring is
tuned to over-alert and we say so explicitly (FF-24, FF-25).

There is a second consequence she did not ask for. Once the collection opens to
the public it sits inside a licensing regime with statutory record keeping, so
the welfare system is partly a compliance system. That is why the animal
register is Tier 0.

**"We want to get more returning visitors too, but are not sure how."**

We are cautious here, because this is where an architecture proposal most easily
drifts into marketing. Our position is that return visits follow from the day
being good: shorter queues, easier wayfinding, an estate that works for a
visitor with a disability or without German. Those are the levers we can build.
A recommendation engine that nudges people back is a phase 3 question and we
have not pretended otherwise.

## What she did not ask for and needs anyway

Sixteen of forty eight functional requirements are regulatory and appear nowhere
in the brief. See [1_4](1_4-regulatory-context.md).

The most consequential is that her stated need to know "where to deploy staff"
runs directly into works council co-determination. Delivered naively, that
feature is not merely risky, it is unlawful to operate without agreement. We
redesigned it to aggregate zone signals before building anything.

This is the gap between a statement of need and a scope, and it is where most of
the cost and nearly all of the risk of this project lives.

## What would make this project fail

Worth naming, since goals without failure conditions are aspirations.

- **AI spend outgrows AI value.** Guarded by the ceiling and the budget guard
- **The system is unrunnable by two or three people.** Guarded by the operability
  ranking and the six hour weekly budget
- **Animal welfare alerts are not trusted and get ignored.** Guarded by measuring
  override rate rather than assuming engagement
- **A regulator stops a headline feature after it is built.** Guarded by doing
  the regulatory register in week one rather than week three
- **The network is worse than we assumed.** Guarded by making degraded operation
  the normal case rather than the exception
