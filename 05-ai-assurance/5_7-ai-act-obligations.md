# EU AI Act obligations mapped to assurance

*The join most submissions will not make: the regulatory register produces
concrete assurance work, and the assurance work produces the evidence the
regulation expects.*

The estate is in Bavaria ([ADR-0001](../07-decisions/ADR-0001-jurisdiction-and-regulatory-baseline.md)),
so Regulation 2024/1689 applies directly. This page treats it as an engineering
input rather than as a compliance appendix.

Written at architecture kata fidelity. We name the obligation and derive the
design consequence. We are not offering a legal opinion, and anything we could
not resolve is in [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md).

## Our role

The estate is a **deployer** of AI systems for everything it buys, and a
**provider** for anything it builds and puts into service under its own name.
That distinction changes the obligations, so we state it per capability rather
than globally.

## Prohibited practices

Two Article 5 prohibitions bite directly on designs we might otherwise have
reached for.

**Emotion recognition in the workplace is prohibited.** This removes an entire
category of "staff wellbeing" and "visitor sentiment on staff performance"
features. We do not infer emotional state from any staff-facing sensor, and the
prohibition is the reason, not squeamishness.

**Real-time remote biometric identification in publicly accessible spaces is
heavily restricted.** Our visitor counting is anonymous, performed at the edge,
retains no frames, and identifies nobody. That decision was already required by
data protection; the AI Act makes it structural rather than preferential.

*Assurance consequence:* FF-29's schema assertion covers staff identifiers. We
add an equivalent structural check that no capability's declared inputs include
biometric or emotion features.

## Staying out of high risk

Annex III classifies AI used for **task allocation based on individual
behaviour or personal traits** in employment as high risk. Our staff deployment
capability sits near that line, and we designed to stay on the right side of it.

| Design choice | Why |
|---|---|
| Inputs are aggregate zone demand only | No individual behaviour or traits are processed |
| Output is a zone level staffing suggestion | It allocates effort to places, not tasks to people |
| A human assigns individuals | The system never allocates a task to a named person |
| FF-29 asserts zero individual identifiers | The boundary is enforced, not documented |

This is the same boundary BetrVG section 87(1)(6) draws for the works council,
arrived at from a different direction. When employment law and AI regulation
agree on where a line sits, that is a strong signal the line is in the right
place.

*Assurance consequence:* if a future change introduced individual-level inputs,
the capability would become high risk and require conformity assessment, a
quality management system, and formal logging. That is an ADR-level decision,
not a backlog item, and FF-29 is what makes the change impossible to introduce
quietly.

## Transparency, Article 50

Visitors interacting with the concierge must be told they are interacting with
an AI system.

*Design consequence:* disclosure at the start of every voice session and on the
web interface, not buried in terms. FR-203 carries it, FF-21 checks it.

Worth noting this is also good product design. A visitor who knows they are
talking to a machine asks better questions and forgives a refusal more readily
than one who thinks they have reached a person.

## AI literacy, Article 4

Deployers must ensure staff dealing with AI systems have sufficient
understanding of them.

*Design consequence:* this is an obligation on the estate, not on the software,
and an architecture that ignores it hands the Countess a problem she did not
know she had. Keepers need to understand what a welfare alert is and is not.
Zone managers need to understand why deployment advice is advisory. The two to
three person technical team needs to understand the fallback behavior they will
be woken up by.

We put this in the phased roadmap as a delivery item rather than pretending it
is somebody else's concern.

## Logging and record keeping

*Design consequence:* the model gateway already records capability, model
version, prompt version, inputs, outputs, cost and evaluation score for every
call, because evaluation needs it. The same record satisfies the logging
expectation.

This is the payoff from routing everything through one component. We did not
build a compliance logging system; we noticed that the thing evaluation
required was the thing the regulation expected, and built it once.

Retention is 90 days for model logs, with the tension against minimization
resolved in [5_3](5_3-production-monitoring.md).

## Human oversight

*Design consequence:* [5_4](5_4-human-in-the-loop.md) in full, and in particular
the parts that make oversight real rather than nominal: the human sees the
evidence, disagreement is as easy as agreement, and override rate is measured
so we can tell whether oversight is happening at all.

An oversight design that cannot demonstrate humans actually disagreed sometimes
is not oversight.

## Summary

| Obligation | Where we address it | What checks it |
|---|---|---|
| Article 5, emotion recognition at work | Capability set excludes it | Input schema check |
| Article 5, biometric identification | Anonymous edge counting, no frames retained | FF-09, DPIA |
| Annex III, employment task allocation | Aggregate-only staff deployment | FF-29 |
| Article 50, transparency | Disclosure per session | FR-203, FF-21 |
| Article 4, AI literacy | Staff training in the roadmap | Delivery item |
| Logging | Model gateway records | FF-20, FF-32 |
| Human oversight | Tier 1 loop design | FF-30 |

Every row lands on something that already existed for engineering reasons. That
is the argument of this page: a system designed to be verifiable is most of the
way to being a system that is demonstrably compliant, and a system designed for
compliance alone is usually neither.
