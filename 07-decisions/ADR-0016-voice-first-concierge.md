# ADR-0016: Voice first visitor concierge

## Status

Accepted. Supersedes [ADR-0007](ADR-0007-text-chat-concierge.md).

## Context

ADR-0007 chose a text chat interface. Writing the visitor personas changed our
minds.

A visitor in an amusement park is walking, carrying things, and frequently
managing children. An interface that requires stopping and reading a screen
will be used by a minority, and a capability used by a minority is not worth its
assurance cost.

Voice also carries two cases text does not. Visually impaired visitors cannot
use a text interface without a separate accessibility mechanism, and hands-free
operation matters most to exactly the visitors who are most burdened.

The objection we had raised against voice, that speech recognition makes
evaluation harder, turned out to be backwards. Recognition error is measurable
and can be injected deliberately, so an end to end evaluation at a realistic
word error rate tells us what a visitor actually experiences. Our text-only
evaluation would have been cleaner and less truthful.

Alternatives reconsidered:

- **Text only.** ADR-0007. Rejected above.
- **Voice only.** Rejected. A noisy queue, a hearing impaired visitor, and
  anyone who simply prefers to read all need a text path.
- **Voice first with a text path.** Both interfaces over one pipeline.

## Decision

Deliver the concierge as **voice first with an equivalent text path**, sharing
one intent classification and response pipeline.

Common intents resolve on the Zone Node. Safety classified topics are answered
from curated content, never generated. Open ended queries escalate to the cloud.

## Consequences

+ Usable while walking and carrying a child, which is the actual context.
+ The accessibility case and the multilingual case are served by the same
  capability rather than by three.
+ Local intent handling keeps most traffic off paid inference, which is most of
  how we stay under the cost ceiling.
+ Voice is a stack the team has shipped before, so the reversal adds less
  delivery risk than a new one would.
− Speech recognition adds an error stage that compounds with model error, and
  must be evaluated end to end.
− A noisy park is a hostile acoustic environment. Recognition quality will be
  worse than in a quiet demo and we should expect that in the numbers.
− Accented and non-native German and English will recognize worse, which is a
  fairness problem in a capability partly justified by serving international
  visitors. We monitor per language quality and disable a language rather than
  serve it badly.
− Voice interfaces are harder to make discoverable. Visitors have to know it
  exists.

## Verification

FF-21 scores answer correctness against a golden set of 300 visitor questions,
requiring 95 percent correct and zero confidently wrong on safety topics.

FF-23 is the one specific to this decision: correctness must hold above 90
percent when speech recognition error is injected at a 10 percent word error
rate. Evaluating the language model on clean text would tell us almost nothing
about a visitor in a queue next to a rollercoaster.

FF-22 requires zero policy violations across 200 adversarial attempts per
release, because a public voice endpoint at a family attraction is a target.
