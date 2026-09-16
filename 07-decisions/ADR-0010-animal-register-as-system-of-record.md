# ADR-0010: The animal register is the system of record, AI is advisory

## Status

Accepted

## Context

The brief asks for animal health monitoring, feeding tracking and population
levels. Read as an operations problem, the natural design has sensors and models
maintaining a live picture of each animal's state.

Once the collection opens to the public it sits inside a licensing regime.
BNatSchG section 42, transposing the EU Zoos Directive, requires up to date
records of the collection. TierSchG section 11 imposes welfare duties, and
TierGesG requires notifiable disease reporting.

The register is therefore a legal record, and the question becomes who is
allowed to write to it.

Alternatives considered:

- **Model writes observations, human reviews later.** Efficient, and it means the
  statutory record contains machine inferences presented as observations. A
  regulator asking who observed an animal was unwell would get an unsatisfying
  answer.
- **Model writes to a separate operational store, register updated in batch.**
  Two sources of truth, which is worse.
- **Model recommends, human confirms, human's decision is the record.**

## Decision

The **animal register is Tier 0**. No model output is written to it.

AI produces advisory alerts. A keeper or veterinarian decides, and **their
decision** is recorded, with the model's contribution recorded as supporting
evidence rather than as an observation.

Notifiable disease indications route to a veterinarian. **The system never
notifies the authority.**

## Consequences

+ The statutory record contains human observations and decisions, which is what
  the regime expects and what a regulator can act on.
+ The audit trail is clean: what the model saw, what it recommended, who decided
  and what they decided.
+ Welfare monitoring can fail completely without putting the estate's licence at
  risk, because the register's integrity does not depend on it.
+ It preserves the veterinarian's professional responsibility rather than
  diluting it.
− **Slower.** Every welfare finding waits for a human, including at three in the
  morning.
− It requires keeper time that the estate must budget for. We have added a
  signal, not a shift pattern, but the signal still costs attention.
− Some genuinely useful automation is off the table, such as automatically
  updating feeding records from weight sensors without confirmation.

## Verification

FF-09 samples regulated records weekly and requires 100 percent
reconstructability: actor, timestamp and evidence for every change, for the full
retention period. NFR-30 requires that any AI-informed entry carries model
version, inputs, confidence and the human confirmation.

The structural check is in the container view: the animal register has no path
to the model gateway. A change introducing one would alter the container
topology and be visible in review.

QS-13 in [2_5](../02-requirements/2_5-quality-scenarios.md) exercises this as a
regulator audit scenario.
