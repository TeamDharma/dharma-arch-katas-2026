# Architecture characteristics

## Why this document comes before the diagrams

One of the judging criteria asks whether the architectural characteristics of
the AI additions match the existing architecture. The organizers confirmed this
is greenfield, so there is no existing architecture to match. We read the
criterion as internal consistency instead, which means we owe the reader two
things in order: the characteristics the core platform is built to, and then
evidence that each AI addition respects them.

This document is the first half. The conformance table at the end is the
second.

## The seven we are designing for

We cannot have everything. These seven are ranked, and the ranking is the
argument. Each one names how it is measured, because a characteristic without a
measure is a preference.

### 1. Availability of the revenue path

The estate must be able to sell a ticket and admit a visitor at all times
during opening hours. Nothing else matters if the turnstile stops.

*Measured as:* successful admissions divided by attempted admissions, target
99.95 percent during opening hours, including during any cloud outage.

*Why first:* the brief's stated failure condition is financial. Every hour the
gate is down is revenue the Countess does not get back, and a queue of angry
families at a family attraction is also a reputational event.

### 2. Partition tolerance

WiFi coverage is patchy and we are told not to expect that to change. The
system has to keep working when parts of it cannot talk to other parts, and it
has to reconcile cleanly afterward.

*Measured as:* every capability has a declared behavior for a network partition
of up to four hours, and the degraded mode matrix in
`../03-architecture/3_8-degraded-mode-matrix.md` has no blank cells.

*Why second:* it is the constraint most likely to break a naive design, and it
is the one the brief states most plainly.

### 3. Operability

Two to three technical staff will run this permanently, and they will have
other jobs. Anything that needs a platform team to keep alive is out.

*Measured as:* number of distinct systems requiring routine human operation,
and hours per week of scheduled operational work. Budget: under six hours per
week in steady state.

*Why third:* it is the constraint that kills the most attractive options, which
is exactly why it has to be visible rather than implicit. See
[A6](../01-problem/1_3-assumptions-and-constraints.md).

### 4. Testability

We need to be able to demonstrate that every component behaves, including the
ones whose outputs vary between runs. For AI components this means an offline
evaluation path that does not require production traffic.

*Measured as:* proportion of AI capabilities with a golden dataset, a defined
acceptance threshold, and an automated evaluation run in CI. Target: all of
them, with no exceptions carried into production.

*Why fourth:* it is the enabling characteristic for everything we claim about
AI in this submission. It is also the one we are best placed to deliver.

### 5. Auditability

The animal collection sits inside a zoo licensing regime with statutory record
keeping, and the point of sale sits inside a fiscal regime with its own
retention duties. Some of this system is a legal record.

*Measured as:* for any regulated record, the ability to reconstruct who or what
changed it, when, and on what evidence, for the full retention period.

*Why fifth:* it is not negotiable where it applies, but it applies to a bounded
part of the system rather than all of it.

### 6. Affordability

AI inference is capped at EUR 0.10 per scanned admission, and the platform as a whole has
to fit a EUR 600,000 annual operating budget. The Countess's problem is
profitability, so cost is a design constraint and not a report.

*Measured as:* rolling inference spend per scanned admission, with an automated guard
that degrades AI features before the ceiling is breached rather than after.

*Why sixth:* it constrains the solution space hard, but unlike the first five
it fails gracefully. Exceeding it is a business problem, not an outage.

### 7. Evolvability at the model boundary

Models, prices, and providers will change inside the three year horizon, and at
least one provider we might pick today will not exist in the same form by the
end of it. The seams around model calls have to be replaceable without
redesigning what sits behind them.

*Measured as:* time to substitute a model provider for a given capability,
measured by actually doing it in a rehearsal rather than asserting it. Target:
under two days per capability, excluding re-embedding.

*Why seventh:* it matters over years rather than hours, so it loses to the
others when they conflict. It does not lose quietly, though. See
`../08-risks-and-uncertainty/8_1-ai-provider-uncertainty.md`.

## What we deliberately did not optimize for

Naming these is part of the argument. A list of characteristics that excludes
nothing has not been thought about.

**Elasticity.** The estate's load is predictable within a day and a season. It
does not spike without warning, and we can provision against a known peak more
cheaply than we can build for elastic scale.

**Extreme low latency.** Turnstiles need to feel instant, which is a few
hundred milliseconds, not a few. Nothing else in the system is latency bound.

**Multi region availability.** One estate, one location, one timezone. A
regional failover story would cost operability, which we ranked higher.

**Openness of the data platform to third parties.** Interesting in year three,
a distraction in year one, and it carries data protection exposure we do not
need to take on yet.

## Criticality tiers for AI additions

Every AI capability in this architecture is assigned a tier. The tier decides
what the capability is allowed to do, what it must fall back to, and how hard
its assurance has to be.

| Tier | What it means | AI permitted? | Fallback | Assurance |
|---|---|---|---|---|
| **0. Deterministic floor** | Revenue and legal obligation. Ticketing, admission, payment, the statutory animal register, fiscal records. | **No.** No model output may sit in this path. | Not applicable. This layer is the fallback. | Conventional testing to normal standards |
| **1. Advisory** | Model output informs a human who decides. Animal health alerts, staff deployment, maintenance prioritization. | Yes, as a recommendation only | The human decision continues without it | Golden dataset, threshold, false negative cost analysis, human override always available and logged |
| **2. Visitor facing** | Model output reaches a visitor directly. Voice concierge, wayfinding, recommendations, translation. | Yes | Static content and a signposted human | Golden dataset, safety evaluation, adversarial suite, live output sampling |
| **3. Analytical** | Model output informs planning, offline, with no live path. Demand forecasting, cohort analysis. | Yes | Last known good forecast, or heuristics | Backtesting, drift detection, published confidence intervals |

The tier model is how we answer the conformance question. A capability's tier
fixes which characteristics it has to satisfy and which it is excused from. It
also decides where the argument happens: moving a capability up a tier is an
ADR, not an implementation detail.

## Conformance of AI additions to platform characteristics

| Capability | Tier | Must satisfy | Deliberately excused |
|---|---|---|---|
| Ticketing and admission | 0 | Availability, partition tolerance, auditability | Nothing |
| Animal welfare monitoring | 1 | Partition tolerance, auditability, testability | Affordability ceiling applies at zone level, not per animal |
| Piranha population estimation | 1 | Testability, auditability | Availability. A daily estimate may be late without harm |
| Staff deployment support | 1 | Operability, testability | Partition tolerance. Aggregated and advisory, so it may wait |
| Voice concierge | 2 | Affordability, evolvability, testability | Availability. Degrades to static content |
| Accessibility and translation | 2 | Availability, affordability | Evolvability, since we will accept lock in for quality here |
| Predictive maintenance | 1 | Auditability, testability | Affordability. Runs rarely and matters when it does |
| Demand forecasting | 3 | Testability, affordability | Availability, partition tolerance |

Two entries in that table are uncomfortable and worth flagging rather than
hiding. Accepting provider lock in for accessibility is a real trade we made
for output quality, and it is recorded as such. Excusing the piranha estimate
from availability assumes nobody needs the number urgently, which is true right
up until an escape.

## Where these characteristics turn into tests

Each characteristic above has at least one fitness function in
[2_4-fitness-functions.md](2_4-fitness-functions.md), with a threshold and an
automated check. A characteristic that no fitness function covers has not
really been adopted, and we treated any such gap as a defect in this document
rather than an acceptable omission.
