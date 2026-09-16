# AI scenarios

*The brief asks for targeted views for each use of AI. This is that set.*

One folder per capability. Every folder follows the same structure, because a
consistent shape lets a reader compare capabilities rather than re-learn a
format eight times.

| Section | What it answers |
|---|---|
| **Purpose** | What problem of the Countess's this solves |
| **Tier and why** | Criticality, and what that permits and forbids |
| **Inputs** | What it consumes, and where that comes from |
| **Approach** | How it works, and the heuristic baseline it must beat |
| **Fallback** | What happens when it is unavailable |
| **Verification** | Golden set, threshold, monitoring, and the failure modes |
| **Diagram** | A targeted view, with a key |

## The set

| Capability | Tier | Depth | Phase |
|---|---|---|---|
| [Ticketing and passes](ticketing-and-passes/) | **0** | Deep | 0 |
| [Visitor experience, the voice concierge](visitor-experience/) | 2 | Deep | 2 |
| [Animal welfare, aquatic](animal-welfare-aquatic/) | 1 | Deep | 1 |
| [Animal welfare, terrestrial](animal-welfare-terrestrial/) | 1 | Standard | 1 |
| [Footfall and staffing](footfall-and-staffing/) | 1 | Deep | 1 and 2 |
| [Piranha population](piranha-population/) | 1 | Standard | 2 |
| [Predictive maintenance](predictive-maintenance/) | 1 | Standard | 2 |
| [Accessibility and translation](accessibility-and-translation/) | 2 | Standard | 2 |

## Why ticketing is in this list

It contains no AI at all, and it is the most important entry here.

The brief asks how AI could solve the Countess's problems. Part of our answer is
that for the capability the estate cannot operate without, the right amount of
AI is none. Including the scenario makes that a decision with reasoning rather
than an omission, and it is where the deterministic floor stops being a slogan.

## What we deliberately did not build

Nothing here is agentic. No capability plans, calls tools against estate
systems, or acts without a person between it and the consequence. The brief's
own example diagram shows an agent booking through MCP, and we read that as an
invitation, so declining it needs a reason.

The reason is the tier model. An agent that acts on estate systems would be
Tier 0 or Tier 1 by consequence, and we could not give it the three things
every capability here must have: a heuristic baseline it must beat, a golden
set that covers what it might do, and a fallback that is not "undo what it
did". With no historical data and a two to three person operations team, an
agent has nothing to be measured against and nobody to catch it.

Where one would earn a place, and when: a read only assistant on the
operations console that answers keeper and manager questions by calling typed,
read only queries over the register, the telemetry and the forecasts. Tier 1,
tools with no write path, every call logged through the gateway, a golden set
of operational questions, and the same override measurement as every other
Tier 1 capability. It is a phase 3 candidate, after the assurance plane has a
year of evidence. It is not in this repository because a capability without a
tier, a fallback and a verification does not appear here.

## The rule every entry obeys

**Tier, fallback, verification. All three, or it does not appear in this
repository.** A capability that cannot answer all three has not been designed,
it has been imagined.
