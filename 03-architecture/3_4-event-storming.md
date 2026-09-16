# Event storming

*The domain expressed as things that happen, which is how the estate's own staff
describe it.*

Condensed from the session output. We kept the events, the commands that cause
them, and the questions that came up, because the questions turned out to be
more valuable than the tidy parts.

## Notation

| Convention here | Meaning |
|---|---|
| **Event** | Something that happened, past tense |
| *Command* | Something someone or something asked for |
| **[!]** | A hotspot. Where the design is contested, or where we found we did not know |

## Ticketing and access

*Purchase ticket* → **Ticket Purchased** → **Credential Issued** → **Fiscal
Record Written**

*Present credential at gate* → **Credential Verified** → **Admission Recorded**

*Request refund* → **Ticket Refunded** → **Revocation Issued** → **[!]
Revocation Distributed** eventually, per zone

**[!] Hotspot.** The gap between Revocation Issued and Revocation Distributed is
a real window in which a refunded ticket admits someone. We accepted it, priced
it as low value, and measured it. Resolved in
[ADR-0004](../07-decisions/ADR-0004-offline-verifiable-ticket-credentials.md).

**[!] Hotspot.** "What is a family?" took longer than anything else in the
session. We landed on a defined group size with at least one adult, deliberately
not a claim about relationships, because verifying relationships creates a data
protection obligation for no operational benefit.

## Animal care

*Feed animals* → **Feeding Recorded** → **Feed Consumption Measured**

**Reading Taken** → **Threshold Breached** *or* **Anomaly Detected** →
**Welfare Concern Raised**

*Inspect animal* → **Observation Made by keeper** → **[!] Register Entry
Written**

**Welfare Concern Raised** → *dismiss* → **Concern Dismissed with reason**

**[!] Hotspot.** The step from Observation Made to Register Entry Written is
where the whole architecture's position on AI lives. A model can cause a
Welfare Concern. Only a qualified human produces an Observation, and only an
Observation becomes a Register Entry. This is the anti-corruption layer in
[3_3](3_3-domain-model.md), and it started as an argument about whether a
confident model should be allowed to write directly.

**[!] Hotspot.** "What if the sensor is broken?" A flat reading looks exactly
like a healthy enclosure, and a model trained on real data will agree with it.
This produced the sensor liveness check, which deliberately does not consult the
model.

## Estate operations

**Ride Cycle Completed** → **Condition Signature Recorded** → **Maintenance
Prioritised**

*Schedule statutory inspection* → **Inspection Completed by accredited body** →
**Inspection Recorded**

**[!] Hotspot.** Somebody asked whether condition data could reduce inspection
frequency. No. It is a legal process performed by an accredited body, and our
output is never evidence within it. This became FR-503.

## Visitor experience

*Ask question* → **Intent Classified** → **Answered Locally** *or* **Escalated**
*or* **Routed to Curated Content**

**[!] Hotspot.** "What happens when someone asks if the snake is dangerous?"
This one question changed the design. We could not make a generated answer
reliable enough for a question whose wrong answer puts a child near a venomous
animal, so that class of question was removed from the model's reach entirely
rather than made safer. It is now the safety router in
[ADR-0016](../07-decisions/ADR-0016-voice-first-concierge.md) and scenario QS-05.

## Insight

**Boundary Crossed** → **Zone Count Updated** → **Occupancy Published**

**Occupancy Published** + **Weather Received** + **Holiday Calendar Loaded** →
**Demand Forecast Produced** → **Staffing Suggestion Produced** → *manager
assigns* → **Shift Assigned**

**[!] Hotspot.** The step from Staffing Suggestion Produced to Shift Assigned is
a human on purpose, and it is where BetrVG and the EU AI Act both apply. See
[ADR-0009](../07-decisions/ADR-0009-aggregate-only-staff-analytics.md).

## What the hotspots have in common

Five of the six are the same shape: **a point where something automated wants to
become something authoritative.**

Revocation wanting to be instant. A model wanting to write a register entry.
Condition data wanting to count as inspection. A generated answer wanting to
cover a safety question. A staffing suggestion wanting to be an assignment.

In every case the answer was to keep the boundary and make the crossing explicit
and human. That pattern was not designed up front. It emerged from the session,
and recognizing it is what produced the tier model in
[2_3](../02-requirements/2_3-architecture-characteristics.md).
