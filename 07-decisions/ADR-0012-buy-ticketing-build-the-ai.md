# ADR-0012: Buy ticketing and point of sale, build the AI

## Status

Accepted

## Context

A2 and A6 in the assumptions set the shape of this decision. The estate will be
run permanently by two to three technical staff who have other jobs. Operability
is our third ranked characteristic and it is the constraint that kills the most
attractive options.

Ticketing, family passes, point of sale with a certified TSE, fiscal record
retention, accessibility conformance and payment integration are all solved
problems with mature commercial products serving attractions of exactly this
size. Building them means building a payments and tax compliance system with a
team of eight, then handing it to a team of two.

The AI capabilities, the zone model and the assurance plane have no off the
shelf equivalent that fits this estate's constraints.

Alternatives considered:

- **Build everything.** Full control, coherent codebase, and it puts the two
  person team on the hook for fiscal compliance changes forever.
- **Buy everything, including an off the shelf park analytics suite.** Minimal
  build, and the analytics products we would buy assume connectivity we do not
  have and would not give us the assurance properties the submission rests on.
- **Buy the commodity, build the differentiator.**

## Decision

**Buy** ticketing, family pass management, point of sale, TSE compliance, and
payment integration from an established attraction platform.

**Build** the Zone Node, the model gateway, the assurance plane, and the AI
capabilities.

Two selection criteria for the bought component, both hard. It must support
**offline validation of credentials at the gate**, and it must support
**delegated issuance at the point of sale**, so that an on-site sale during a
cloud outage produces a credential the gate can verify (ADR-0004). A product
that requires connectivity at the turnstile, or that can only issue credentials
from its cloud, is disqualified regardless of its other merits.

## Consequences

+ Fiscal and tax compliance changes become the vendor's problem, which for a
  two person team is worth a great deal.
+ Phase 0 ships much faster, so the estate has revenue while we build the
  interesting parts.
+ Accessibility conformance for ticketing comes with a product that already has
  to meet it.
+ Engineering effort concentrates on the parts that are actually differentiated.
− **The deterministic floor is now partly a vendor product**, so its availability
  depends on someone else's engineering. Mitigated by the offline validation
  requirement, which means a vendor outage does not stop admission.
− Integration surface, and the usual risk that the vendor's data model resists
  what we need.
− Vendor lock-in on the revenue path, which is the worst place to have it.
− If no product meets both criteria adequately, this decision reverses and
  the build scope grows substantially.

## Verification

FF-02 runs the revenue path smoke test with all cloud dependencies stubbed,
which exercises exactly the offline property the vendor selection depends on. A
product that cannot pass it has not met the criterion.

FF-06 counts distinct systems requiring routine human operation, capped at six.
Buying reduces that count, which is the operability argument made measurable.

The commercial terms are out of scope for this architecture, but the exit
question is not: we hold our own copy of ticket and pass data continuously, so
that changing vendor is a migration rather than a hostage negotiation.
