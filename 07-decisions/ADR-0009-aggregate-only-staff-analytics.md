# ADR-0009: Aggregate only staff analytics

## Status

Accepted

## Context

The Countess asked to know where to deploy staff. The natural design collects
staff location and activity, measures productivity per person and per zone, and
optimizes assignment.

That design is unlawful to operate in Germany without works council agreement,
and it may be high risk under the EU AI Act.

Under BetrVG section 87(1)(6), a works council holds co-determination over any
technical system **capable** of monitoring employee performance. Capability is
the trigger, not intent, so a system that could produce per-person figures needs
agreement whether or not anyone looks. Separately, Annex III of the AI Act
classifies AI used for task allocation based on individual behaviour or traits
in employment as high risk, bringing conformity assessment and a quality
management system.

Alternatives considered:

- **Individual tracking with works council agreement negotiated.** Possible in
  principle. It makes a legal negotiation a precondition for a feature, hands
  the works council a permanent veto over changes, and likely lands the
  capability in the high risk category.
- **Individual tracking with the data locked down.** Does not help. Capability
  is the trigger, not access control.
- **Aggregate zone demand only, human assigns.**

## Decision

Staff deployment consumes **zone occupancy counts only** and produces a **zone
level staffing suggestion**. No individual staff identifier exists in any
analytics schema. A human assigns individuals to places.

## Consequences

+ Stays clear of both BetrVG co-determination on monitoring and AI Act Annex III
  high risk classification. Two regulatory regimes, one design.
+ The works agreement conversation becomes straightforward rather than adversarial,
  because there is nothing to concede.
+ The capability is simpler, cheaper and needs less data.
+ It is also the better design on its merits. Zone demand is what a manager
  needs; per-person productivity would have been a distraction.
− **We cannot measure individual performance**, which some managers will
  eventually ask for. The answer is no, and this ADR is where that answer lives.
− Without individual data we cannot account for skills, so a suggestion of "three
  more people in the aquatic house" does not know who is qualified to be there.
  The manager supplies that knowledge.
− Advice quality depends on managers actually using it, and we have no lever to
  make them.

## Verification

FF-29 asserts at schema level that staff deployment output contains zero
personally identifying fields, on every commit and every run, and **fails the
build** otherwise.

That is what turns this from a policy into an architecture. A works council
asking whether the system can monitor individuals gets an answer from build
history rather than from a design document, which is scenario QS-10 in
[2_5](../02-requirements/2_5-quality-scenarios.md).

Working time compliance is checked by rules outside the model, because rest
periods are law and not a judgment call. And FF-30 watches override rate, where
a rate near zero is investigated rather than celebrated: total compliance would
mean the human is rubber stamping, and human judgment is the legal basis for
keeping this out of the high risk category.
