# The animal register as master data

*The most legally significant data in the system, and the reason AI is advisory
throughout the welfare capabilities.*

## What it is

Under BNatSchG section 42, transposing the EU Zoos Directive, a licensed
collection must maintain up to date records of the animals it holds. TierSchG
imposes welfare duties. Wildlife trade regulation requires provenance and
movement documentation for regulated species.

Together these make the register a **statutory record**, inspected by an
authority, and evidence in a licensing decision.

## What it contains

| Element | Detail |
|---|---|
| Identity | Per animal, with marking or identification as required for the species |
| Provenance | Origin, acquisition, permits, CITES documentation where applicable |
| Location | Current enclosure, and movement history |
| Health | Observations, treatments, veterinary decisions |
| Feeding | Recorded feeding events |
| Disposition | Transfer, death, with cause where determined |

## The rule

**No model output is ever written to the register.**

AI produces advisory alerts. A keeper or veterinarian decides. **Their decision
is the record**, and the model's contribution is recorded as supporting
evidence alongside it.

This is [ADR-0010](../07-decisions/ADR-0010-animal-register-as-system-of-record.md)
and it is Tier 0 in the criticality model.

## What an entry looks like

An entry records who observed, when, what, and on what basis. Where AI was
involved, the entry carries the model version, its inputs, its confidence, and
the fact that a named human confirmed it, so that an inspector can distinguish
between what a person saw and what a system suggested.

The distinction is the entire point. A regulator asking "who determined this
animal was unwell" must get the name of a qualified person, not a model version.

## Why it is structurally protected, not just policy

Three separate mechanisms, because a rule this important should not rest on one.

**Container topology.** The animal register has no path to the model gateway in
the [container view](3_2-container-view.md). Introducing one would change the
architecture visibly rather than adding a line of code.

**Bounded context separation.** Animal Care and Compliance and Records are
different contexts with an anti-corruption layer between them, and the word
"observation" means different things on either side. See
[3_3](3_3-domain-model.md). A concern cannot become an entry by passing through
a mapper.

**Append only with full reconstruction.** FF-09 samples entries weekly and
requires actor, timestamp and evidence for every change, for the full retention
period.

## Availability

The register is Tier 0, so it has to work when things do not.

| Condition | Behavior |
|---|---|
| Cloud link down | Entries are taken by the zone ops view on the keeper's tablet, queued on the Zone Node, reconciled on reconnect |
| Zone Node down | Paper fallback, keyed in later. **This is the statutory path anyway** |
| Model provider down | No effect. Models never write here |

The paper fallback is not a joke. Zoos kept these records on paper for decades
and the regime still contemplates it. An architecture that made the statutory
record dependent on our software being available would have made the estate's
licence dependent on our uptime, which would be an unreasonable thing to do to
the Countess.

## Notifiable disease

A special path, and the one with the sharpest boundary.

Welfare monitoring may flag indicators consistent with a notifiable disease. It
raises a concern. **A veterinarian confirms and reports to the Veterinäramt.**

The system never notifies an authority. A false positive notification is not a
degraded feature, it is a regulatory event with consequences for the estate, and
the professional judgment of a veterinarian is the control the regime is built
around.

## What this costs

Every welfare finding waits for a human, including at three in the morning, and
keeper time has to be budgeted for. Some genuinely useful automation is off the
table, such as updating feeding records automatically from weight sensors.

We accepted all of it. The register's integrity is what the estate's licence
rests on, and no efficiency gain is worth putting a machine inference into a
document a regulator will read as a professional observation.
