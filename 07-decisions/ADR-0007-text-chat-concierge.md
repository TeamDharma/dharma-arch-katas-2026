# ADR-0007: Text chat concierge in the visitor app

## Status

**Superseded by [ADR-0016](ADR-0016-voice-first-concierge.md)**

## Context

*Recorded as originally written, on the second working session, before the
decision was reversed. We have left it intact rather than editing it, because
the reasoning was sound given what we knew and the reversal is more useful to a
reader than a tidy history.*

Visitors need wayfinding, queue times, opening hours and exhibit information.
The estate has no way to deliver any of it beyond static signage.

A text chat interface in a visitor web app is the obvious answer. It is the
cheapest to build, the easiest to evaluate because the input is already text,
the easiest to translate, and every team member has built one.

Alternatives briefly considered and set aside: voice, which we thought would be
harder to evaluate and noisier in a park environment; and a purely static
information site, which cannot answer open ended questions.

## Decision

Deliver the visitor concierge as a text chat interface in a mobile web app.

## Consequences

+ Cheapest path to a working capability.
+ Text in, text out, which makes the golden set and the adversarial suite
  straightforward.
+ Translation is a solved problem on text.
− Requires the visitor to stop, take out a phone, and read.
− Accessibility for visually impaired visitors requires a separate mechanism.

## Why this was superseded

Two problems surfaced once we had written the visitor personas.

**People in a park have their hands full.** Often literally, with children,
pushchairs, food and bags. An interface requiring a visitor to stop walking and
look at a screen is one most of them will not use, which makes its measured
quality irrelevant.

**We had assumed voice was harder to assure, and had it backwards.** Speech
recognition does add an error stage, but that stage is measurable and
injectable. We now test the pipeline end to end at a 10 percent word error rate
(FF-23). The assurance is not harder, it is more honest, because a text-only
evaluation was never measuring what a visitor would actually experience.

We had also been designing around voice experience the team already had,
rather than with it.

See [ADR-0016](ADR-0016-voice-first-concierge.md).
