# ADR-0015: Model provider exit strategy

## Status

Accepted

## Context

The kata asks directly how we deal with the best model or provider today not
being the best tomorrow, with a provider changing prices, and with a provider
shutting down.

Over a three year horizon all three are likely and at least one is close to
certain. The usual answer, "we use an abstraction layer", is not an answer. It
describes an intention without saying what is actually portable.

## Decision

Provider substitution is handled at the **model gateway** (ADR-0005), and we
commit to a specific scope of portability rather than a general claim.

**What is portable**

| Asset | How |
|---|---|
| Capability code | Never imports a provider SDK. FF-14 enforces it |
| Prompts | Versioned, stored as data, evaluated per provider |
| Golden datasets | Provider independent by construction |
| Routing and caching | Gateway concerns, unchanged by substitution |

**What is not portable, and what it costs**

| Asset | Why | Cost to replace |
|---|---|---|
| **Vector embeddings** | Embeddings from one provider are meaningless to another | **Re-embed the entire corpus.** Time and compute proportional to corpus size, and it must complete before the capability works |
| Fine tuned models | Do not transfer | Retrain, if we ever fine tune. We currently do not |
| Prompt tuning | Prompts optimized for one model perform differently on another | Re-evaluate every capability against its golden set, and expect some to need rework |
| Tool calling semantics | Differ in format and reliability | Adapter work in the gateway |

The re-embedding cost is the one most teams miss, and it is why our substitution
target in NFR-34 says "two days, **excluding re-embedding**". Stating the target
without that exclusion would be dishonest.

## Provider shutdown runbook

| Notice | Response |
|---|---|
| **30 days or more** | Substitute in the gateway, re-evaluate against golden sets, re-embed if needed, canary, switch. QS-04 |
| **Sudden, no notice** | Every capability falls to its heuristic baseline automatically. Tier 0 is unaffected. The estate keeps operating while we substitute. QS-03 |

The second row is the reason ADR-0006 keeps the baseline permanently. A sudden
provider shutdown is an outage for most architectures. Here it is a degradation,
and the difference is entirely due to a decision made for a different reason.

## Consequences

+ A provider disappearing overnight does not stop the estate.
+ Costs of substitution are stated concretely rather than waved at, so the
  Countess can make an informed decision about corpus size and embedding
  provider choice.
+ Rehearsing substitution quarterly means the first real one is not the first
  one we have attempted.
− Keeping capabilities provider-neutral means declining provider-specific
  features that would sometimes be better.
− Re-embedding is a real cost we have accepted rather than eliminated. Reducing
  it further would mean self-hosting embeddings, which fails the operability
  constraint.
− We deliberately accept lock in for accessibility and translation. See
  [2_5](../02-requirements/2_5-quality-scenarios.md).

## Verification

FF-13 rehearses a substitution quarterly on a randomly chosen capability and
requires completion within two days excluding re-embedding. A failed rehearsal
means the seam has leaked and the leak gets fixed.

FF-14 asserts zero provider SDK imports outside the gateway on every commit.

Weekly golden set runs happen **regardless of whether we changed anything**,
which is how we detect a provider silently updating a model behind a stable
name. That is the failure mode with no error message, and the only way to see it
is to keep measuring when nothing appears to have happened.
