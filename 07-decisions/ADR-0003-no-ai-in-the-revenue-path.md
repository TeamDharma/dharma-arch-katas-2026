# ADR-0003: No AI in the revenue path

## Status

Accepted

## Context

This kata asks how AI can solve the Countess's problems, and the honest answer
includes a boundary.

Ticketing, admission, payment, fiscal records and the statutory animal register
share three properties. They are what the estate cannot operate without, their
failures are legal or financial rather than degraded, and they are exactly the
places where a plausible-but-wrong output causes the most damage.

We identified three tempting applications of AI in this path and evaluated each.

**Dynamic pricing driven by a demand model.** Attractive, common in the
industry, and genuinely capable of increasing yield. But price is a contractual
term. PAngV requires total price transparency, AGG constrains segmentation, and
a pricing error is a legal and reputational event rather than a degraded
feature. A rules based seasonal and day-of-week pricing table captures most of
the available yield with none of the exposure, and a human can explain it.

**Fraud detection on purchase.** Card fraud is the payment provider's problem
and they have vastly more signal than we do. Adding our own model creates a
false positive path that refuses a real family at a gate, which is a worse
outcome than the fraud it prevents at our volume.

**Conversational ticket purchase.** A checkout that occasionally misunderstands
is a checkout that occasionally sells the wrong product to someone who
discovers it at the gate. The form works, and it is accessible, auditable and
translatable.

## Decision

**No model output may appear in the revenue path or in any statutory record.**
This is Tier 0 in the criticality model: ticketing, admission, payment, fiscal
records, and the animal register.

AI sits above this floor and never inside it. Every AI capability in the system
degrades to something in Tier 0 or to curated content.

## Consequences

+ The estate sells tickets and admits visitors with every model provider dark,
  which is the single strongest availability property in the architecture.
+ The floor gives every other capability a defined thing to fall back to, which
  is what makes graceful degradation possible rather than aspirational.
+ Regulatory exposure in the fiscal and zoo licensing regimes is bounded to
  deterministic code we can reason about.
+ It simplifies the assurance story enormously. Tier 0 needs conventional
  testing, not evaluation harnesses.
− **We leave yield on the table.** A demand-driven pricing model would probably
  earn more than a seasonal table. We chose a smaller, explicable number.
− A visitor cannot buy a ticket by talking to the concierge, which is a genuinely
  nice experience we are declining.
− In an AI competition, submitting a decision to not use AI carries a risk of
  being read as a lack of ambition rather than as a judgment.

## Verification

FF-02 runs the revenue path smoke test with every cloud dependency stubbed out
and requires a 100 percent pass on every deploy. The container view shows that
no Tier 0 container has any path to the model gateway, and that is a structural
property rather than a convention.

A future change that introduced a model into this path would have to modify the
container topology to do it, which makes the boundary visible in review rather
than discoverable in production.
