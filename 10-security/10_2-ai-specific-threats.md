# AI specific threats

*The concierge is a public endpoint, at a family attraction, with the estate's
name on it. That makes it a target in a way the rest of the system is not.*

## Prompt injection

The main event. A visitor types or says something engineered to make the
concierge behave off policy, then screenshots the result.

The motive is usually not theft. It is amusement, and the harm is reputational:
a family attraction's assistant saying something obscene, offensive, or
dangerously wrong, circulating on social media.

| Control | Detail |
|---|---|
| Scope constraint | The concierge answers about the estate. Off-scope requests are refused by design, not by instruction |
| Safety topic routing | Questions about dangerous animals are routed to curated content by two independent signals, an intent classifier and a lexical net, with an output filter behind generation. Router recall is measured by FF-36 ([ADR-0016](../07-decisions/ADR-0016-voice-first-concierge.md)) |
| Input classification | Before generation, not as part of the prompt |
| Output filtering | After generation, before speech synthesis |
| Adversarial suite | 200 attempts per release, zero tolerance (FF-22) |
| Corpus growth | **Every real attempt observed in production is added to the suite** |
| Automatic fallback | A successful violation in production reverts the capability to curated content pending fix |

The last two matter most. An adversarial suite frozen at launch tests last
year's attacks, and visitors are inventive in ways we are not.

## Indirect prompt injection

The subtler version: hostile instructions arrive not from the visitor but from
content the model reads.

Our exposure is narrow because the concierge's retrieval corpus is estate
authored. But it is not zero, because we ingest weather and school holiday
calendars from third parties, and translation processes text we did not write.

**Control:** external content is treated as data and never concatenated into an
instruction position. The weather feed supplies numbers into a template, not
prose into a prompt.

## Data poisoning

Welfare models learn from the estate's own data, so an attacker who can
influence sensor readings could in principle teach a model that an abnormal
state is normal.

Realistically this requires physical access to an enclosure, at which point the
attacker has easier ways to harm an animal. We note it, control it lightly
through sensor liveness and bounds checking, and do not over-engineer against it.

The more plausible variant is accidental: an enclosure is rearranged, the model
learns the new normal, and a genuine problem later looks unremarkable. That is
handled as a re-baselining event rather than as a security control.

## Model extraction and cost attacks

**Extraction** is not a meaningful threat. Our models are not proprietary and
their value is in the estate's data and thresholds, not in weights.

**Cost attack** is real and cheap to attempt. A script hammering the open ended
concierge path could burn through the inference budget deliberately.

| Control | Detail |
|---|---|
| Rate limiting per session and per source | Standard |
| Local intent handling | Most traffic never reaches paid inference anyway |
| Budget guard | Degrades before the ceiling, so an attack produces reduced service rather than an unbounded bill (FF-11) |

The budget guard was built for provider price rises. It turns out to be the
control that makes a cost attack survivable, which is the second time in this
architecture that a decision made for one reason covered a different risk.

## Output handling

Model output is **untrusted data**, everywhere, without exception.

It is never executed, never used to construct a query, never written to a
statutory record, and never used to authorize anything. This is why
[ADR-0010](../07-decisions/ADR-0010-animal-register-as-system-of-record.md)
requires a human between a welfare alert and the register, and it is why the
container view shows no path from the model gateway to any Tier 0 container.

## Privacy specific to AI

| Concern | Control |
|---|---|
| Visitor speech is personal data | Model logs retained 90 days, then aggregated and raw records deleted |
| Children's voices | Same retention, no identification, no voice biometrics, ever |
| Model logs as an evaluation corpus | Directly in tension with minimization. Resolved toward minimization, stated in [5_3](../05-ai-assurance/5_3-production-monitoring.md) |
| Provider processing of visitor input | Data processing terms and location are a procurement requirement, not an afterthought |

## The threat we cannot fully control

A visitor asks the concierge something about an animal, gets a wrong answer, and
acts on it.

We removed the highest consequence version architecturally: safety topics never
reach generation. What remains is the long tail, where a plausible wrong answer
about opening times or facilities is merely annoying, and where the boundary
between annoying and harmful is not always obvious in advance.

Our position is that the two routing signals cover what we could enumerate and
what we could paraphrase, the output filter and the weekly sample of generated
turns catch some of what both missed, and the residual is real. Claiming otherwise would be the kind
of overconfidence this whole submission argues against.
