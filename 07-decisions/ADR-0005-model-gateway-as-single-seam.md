# ADR-0005: The model gateway as the single provider seam

## Status

Accepted

## Context

Three separate problems arrived at the same answer.

**Evolvability.** Models, prices and providers will change within the three year
horizon, and at least one provider we might pick today will not exist in the
same form by the end of it. Provider specific code scattered through eight
capabilities makes substitution a rewrite.

**Assurance.** Evaluation needs every model call recorded with its inputs,
outputs, model version, prompt version and score. Instrumenting eight
capabilities separately guarantees inconsistency.

**Cost.** The EUR 0.10 per scanned admission ceiling needs a single place that knows what
has been spent and can act before the ceiling is reached.

Alternatives considered:

- **Direct provider SDK calls per capability.** Fastest to build, and it makes
  all three problems above unsolvable without a later refactor.
- **A thin wrapper library.** Better, but a library is a convention. Nothing
  stops a developer importing the SDK directly, and conventions decay.
- **A gateway component every call passes through, with a structural check
  forbidding provider SDK imports anywhere else.**

## Decision

Every model call in the system routes through a single **model gateway**
component, which handles provider abstraction, routing, caching, budget
accounting and logging.

**No provider SDK may be imported anywhere outside the gateway**, enforced as a
static check on every commit.

## Consequences

+ One component satisfies three architectural characteristics, which is a better
  ratio than three components satisfying one each.
+ Provider substitution becomes a change in one place, making the two day target
  in NFR-34 plausible rather than aspirational.
+ The logging the AI Act expects from a deployer falls out of the logging
  evaluation already required. We built it once.
+ Caching and small-model-first routing are implementable centrally, which is
  most of how we stay under the cost ceiling.
− **It is a sensitivity point and a single point of failure.** Gateway downtime
  takes every AI capability with it. Mitigated by the fact that every capability
  has a heuristic baseline, so the blast radius is degradation rather than
  outage.
− It adds a network hop and some latency to every inference.
− There is a real risk of it becoming a dumping ground. Routing logic,
  capability-specific prompting and business rules will all try to migrate into
  it, and we will have to push back.
− Edge inference on Zone Nodes complicates the picture, since a local model call
  is not a network call. Local inference is registered with the gateway for
  accounting and logging even where the call does not physically transit it.

## Verification

FF-14 asserts zero provider SDK imports outside the gateway on every commit, and
fails the build otherwise. This is the cheapest high value check in the
repository: minutes to write, and it is what keeps the promise honest over three
years.

FF-13 rehearses a provider substitution quarterly for a randomly chosen
capability and requires completion within two days excluding re-embedding. A
rehearsal that fails is the signal that the seam has leaked.
