# Dealing with uncertainty in AI technology

*The kata asks three questions directly. This page answers them.*

> How are you going to deal with the fact that the best models or providers
> today might not be the best tomorrow? How would you handle your model provider
> changing prices on you? What might happen if the provider you used suddenly
> shut down?

## The general answer, and why it is not enough

The usual response is an abstraction layer. We have one
([ADR-0005](../07-decisions/ADR-0005-model-gateway-as-single-seam.md)) and it is
enforced rather than intended, because FF-14 fails the build on any provider SDK
import outside it.

But an abstraction layer only answers the easy half. It makes the code portable
and says nothing about the assets, the costs, or what the estate does during the
substitution. Those are the parts that hurt.

## Question 1: the best model today is not the best tomorrow

**What we do:** capabilities are bound to a capability contract, not to a model.
Prompts are versioned data rather than code. Golden sets are provider
independent. Swapping a model means re-evaluating against the golden set and
switching a route.

**What it costs:** prompts optimized for one model perform differently on
another, so a substitution is not free even when the code is untouched. Expect
some capabilities to need prompt rework, and expect to find that out from the
evaluation rather than from production.

**What we decline:** provider specific features that would sometimes be better.
That is a real capability cost, accepted deliberately.

## Question 2: the provider changes prices

**What we do:** the budget guard degrades Tier 2 capabilities in a fixed order
when rolling spend per scanned admission reaches EUR 0.08, before the EUR 0.10 ceiling is
reached. Degradation is automatic and the order is decided in advance.

**Why it works:** a price rise becomes a predictable service change rather than
an unexpected invoice. QS-12 in
[2_5](../02-requirements/2_5-quality-scenarios.md) exercises exactly this.

**What it costs:** visitors experience reduced service for reasons invisible to
them, and the estate may be running degraded for weeks while a substitution is
evaluated.

## Question 3: the provider shuts down

| Notice | What happens |
|---|---|
| 30 days or more | Substitute in the gateway, re-evaluate, re-embed if needed, canary, switch |
| **None at all** | **Every capability falls to its heuristic baseline automatically. Tier 0 is unaffected. The estate keeps operating.** |

The second row is the important one, and it works because of a decision made for
an entirely different reason. [ADR-0006](../07-decisions/ADR-0006-heuristic-baseline-retained-permanently.md)
keeps a rule based implementation of every capability permanently, originally to
solve cold start with no historical data.

The consequence is that a sudden provider shutdown, which is an outage for most
architectures, is a degradation for this one. The estate sells tickets, admits
visitors, keeps its statutory records, monitors water quality against
thresholds, and answers the twenty most common visitor questions from cache,
with every model provider in the world offline.

## What is not portable, and what it costs

This is the part most answers omit.

| Asset | Why it does not move | Cost |
|---|---|---|
| **Vector embeddings** | Embeddings from one provider are meaningless to another | **Re-embed the entire corpus** before the capability works again |
| Prompt tuning | Optimized per model | Re-evaluate everything, rework some |
| Tool calling semantics | Format and reliability differ | Adapter work in the gateway |
| Fine tuned models | Do not transfer | Retrain. We currently do not fine tune, partly for this reason |

Re-embedding is why NFR-34 says substitution in "two days, **excluding
re-embedding**". A target stated without that exclusion would be a target we
could not meet, and quietly hoping nobody asks is not an architecture.

## The uncertainty we are least protected against

Honesty requires naming it: **a provider silently changing a model behind a
stable name.**

There is no notice, no version change, no deployment on our side, and the
capability's behavior shifts. Nothing throws.

Our only defense is running golden sets **weekly regardless of whether we
changed anything**. A score shift with no commit of ours points at the provider.
That costs money to do and detects the problem days after it starts, which is
the best we can currently do and is not good enough to be comfortable about.

## The bet underneath all of this

We assume model capability keeps improving and prices keep falling, but that
specific providers are unreliable partners over a three year horizon.

So we optimize for **substitutability rather than for extracting the maximum
from any one provider**. That is a deliberate trade: a team willing to bind
tightly to one vendor could build something better today. We think the estate,
run by two or three people with a three year horizon and a plant collection at
stake, is better served by a system that survives its suppliers.

The one place we took the opposite bet is accessibility and translation, where
output quality is a usability floor rather than a gradient. That lock-in is
recorded as a tradeoff rather than hidden.
