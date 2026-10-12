<p align="center"><img src="assets/dharma.png" alt="Team Dharma logo" width="220"></p>

# Von Digitalis Estates: an AI architecture that can be held to account

**Team Dharma** | O'Reilly Architectural Katas 2026: AI-Assisted Software Architecture

The 72nd Countess Von Digitalis has inherited an estate with forty 18th century
rides, over two hundred animals, patchy WiFi, and three years to triple her
visitor numbers or sell the carnivorous plants. This repository is our proposal
for how to build the system she needs.

## Our position

Every team in this kata will put AI into the solution. The interesting question
is not whether AI can do these jobs. It is whether anyone can tell when it
stops doing them properly.

So our architecture is built around a claim we are willing to be tested on:
**every AI capability in this system has a defined way to prove it is working,
a threshold at which it is considered broken, and something deterministic to
fall back to when it breaks.** Nothing goes in that we cannot verify. Where we
could not verify something, we did not use AI for it, and we wrote down why.

That shapes three things you will see throughout:

- **A deterministic floor.** The estate can sell a ticket, admit a visitor, and
  keep its legally required animal records with every model provider offline.
  AI sits above that floor, never inside it.
- **Assurance as architecture.** Evaluation, drift detection, and fallback are
  components in the diagrams with owners and budgets, not a paragraph about
  testing at the end.
- **A cost ceiling.** AI inference is capped at EUR 0.10 per scanned admission. The
  Countess's problem is profitability, so a feature that costs more than it
  earns is a feature we removed.

**Where we bet.** The first judging criterion is innovative use of AI, and
our AI is deliberately conventional: a concierge, anomaly detection,
forecasting, condition monitoring, translation. There is nothing agentic in it
and no tool use over estate systems. That is a choice rather than an oversight,
and [04-ai-scenarios/README.md](04-ai-scenarios/README.md) says what an agentic
capability would have to show before it earned a place here. The bet is that a
judge asking "does it work, and how would you know" will value the answer more
than a judge asking "is it novel" will miss the novelty.

## How to read this

**If you have five minutes**

1. This page
2. [Solution strategy](03-architecture/3_0-solution-strategy.md), which is the
   whole architecture in one document
3. [AI assurance strategy](05-ai-assurance/), which is the part we think is
   different from other submissions

**If you have twenty minutes**

Add [the problem as we read it](01-problem/1_0-problem-statement.md),
[our assumptions](01-problem/1_3-assumptions-and-constraints.md), the
[AI scenarios](04-ai-scenarios/), and
[ADR-0001](07-decisions/ADR-0001-jurisdiction-and-regulatory-baseline.md) for a
sense of how we argue.

**If you are reading the whole thing**

Start at `01-problem/` and walk the numbered folders in order. They are
numbered in the order the decisions were actually made.

## Where the brief's deliverables are

| Deliverable | Where |
|---|---|
| Overview narrative of how AI solves the estate's problems | This page, then [3_0-solution-strategy.md](03-architecture/3_0-solution-strategy.md) |
| Comprehensive views | [03-architecture/](03-architecture/): context, containers, domain model, connectivity with a partition sequence, deployment, reference technology choices |
| Targeted view for each use of AI | One per folder in [04-ai-scenarios/](04-ai-scenarios/), each with an inline key |
| ADRs for the AI implementations, with trade-offs | [07-decisions/](07-decisions/), sixteen, each with the options weighed, consequences and a verification method |
| Implementation details (optional) | [code/](code/), a runnable evaluation harness |
| Five minute video (semifinalists only) | [video/Kata_Submission.mp4](video/Kata_Submission.mp4) |

Every diagram is inline Mermaid, so GitHub renders it in place. PNG exports of
all fifteen are in [assets/diagrams/](assets/diagrams/) for reading offline.

## Where the judging criteria are answered

| Criterion | Where |
|---|---|
| Innovative use of AI | [04-ai-scenarios/](04-ai-scenarios/) |
| Suitability given the constraints | [01-problem/1_3-assumptions-and-constraints.md](01-problem/1_3-assumptions-and-constraints.md), [06-economics/](06-economics/) |
| Appropriate levels of detail | [03-architecture/](03-architecture/), [diagram legend](03-architecture/3_10-diagram-legend.md) |
| Dealing with uncertainty in AI technology | [08-risks-and-uncertainty/](08-risks-and-uncertainty/), [claim confidence](02-requirements/2_6-claim-confidence.md) |
| Architectural characteristics of additions matching | [02-requirements/2_3-architecture-characteristics.md](02-requirements/2_3-architecture-characteristics.md) |
| Validation and verification of AI results | [05-ai-assurance/](05-ai-assurance/) |

The fifth criterion needs a word of explanation. This is greenfield, confirmed
by the organizers, so there is no existing architecture for the additions to
match. We read the criterion as internal consistency instead: we define the
core platform's characteristics first, then show that each AI addition conforms
to them, or say plainly where it does not and why we accepted that.

## Repository map

| Folder | Contents |
|---|---|
| `01-problem/` | The brief as we read it, assumptions, regulatory context |
| `02-requirements/` | Functional, non functional, characteristics, fitness functions, quality scenarios, claim confidence |
| `03-architecture/` | Context, containers, domain model, connectivity, degraded mode, data, reference technology choices |
| `04-ai-scenarios/` | One folder per AI capability, with its own targeted view |
| `05-ai-assurance/` | Evaluation, golden datasets, drift, human in the loop, fallbacks |
| `06-economics/` | Cost model, AI spend ceiling, build versus buy, business case |
| `07-decisions/` | Architecture decision records |
| `08-risks-and-uncertainty/` | Model provider risk, exit strategy, risk register, roadmap |
| `09-ai-disclosure/` | How we used AI to produce this, including where it was wrong |
| `10-security/` | Threat model, AI specific threats, incident scenarios |
| `code/` | A runnable evaluation harness for the claims in `05-ai-assurance/` |
| `assets/` | PNG exports of every diagram, team logo |

## Run the checks yourself

The assurance claims in this repository are testable, so we made them testable.

```bash
python3 code/eval/run_evals.py
```

```bash
python3 09-ai-disclosure/checks/check-docs.py
python3 09-ai-disclosure/checks/check-architecture.py
```

Nineteen checks across three suites. No network, no API keys, no third party
packages, all exit non-zero on failure.

The architecture suite tests the claims this repository makes about itself:
that every requirement names a verification method, that every AI capability
declares a tier, a fallback and a verification, that the degraded mode matrix
has no gaps, and that our headline numbers do not contradict each other. It
found two real inconsistencies the first time it ran, both described in
[`09-ai-disclosure/checks/`](09-ai-disclosure/checks/).

## If you work in arc42

We numbered the folders around the judging criteria rather than around a
template, but the arc42 sections are all present. This is where they live.

| arc42 section | Here |
|---|---|
| 1. Introduction and goals | [`01-problem/`](01-problem/), [`02-requirements/2_1`](02-requirements/2_1-functional-requirements.md) |
| 2. Constraints | [`01-problem/1_3`](01-problem/1_3-assumptions-and-constraints.md), [`1_4`](01-problem/1_4-regulatory-context.md) |
| 3. Context and scope | [`03-architecture/3_1`](03-architecture/) |
| 4. Solution strategy | [`03-architecture/3_0`](03-architecture/3_0-solution-strategy.md) |
| 5. Building block view | [`03-architecture/3_2`](03-architecture/) |
| 6. Runtime view | [`04-ai-scenarios/`](04-ai-scenarios/), and the partition and reconciliation sequence in [`3_5`](03-architecture/3_5-connectivity-and-edge.md) |
| 7. Deployment view | [`03-architecture/3_6`](03-architecture/) |
| 8. Cross-cutting concepts | [`05-ai-assurance/`](05-ai-assurance/), [`10-security/`](10-security/), [`3_11`](03-architecture/3_11-data-architecture.md) to [`3_13`](03-architecture/3_13-animal-register.md) |
| 9. Architecture decisions | [`07-decisions/`](07-decisions/) |
| 10. Quality requirements | [`02-requirements/2_3`](02-requirements/2_3-architecture-characteristics.md), [`2_4`](02-requirements/2_4-fitness-functions.md) |
| 11. Risks and technical debt | [`08-risks-and-uncertainty/`](08-risks-and-uncertainty/) |
| 12. Glossary | [`GLOSSARY.md`](GLOSSARY.md) |

## Also worth reading

- [TODO.md](TODO.md): what is done and what is left
- [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md): what we could not settle
- [TEAM.md](TEAM.md): who we are, and why the team is called Dharma

## Source material

The organizers' brief is not reproduced here. Our reading of it is restated in
our own words in
[`01-problem/1_0-problem-statement.md`](01-problem/1_0-problem-statement.md).

## A note on scope

The four of us had other professional commitments through the kata window and
could not spend much time on this together. What is here was drafted by an AI
assistant working under our direction, kept in check by scripts that do not
share its assumptions, and shaped by the discussions and reviews we could fit
in between. [09-ai-disclosure/](09-ai-disclosure/) says exactly how that went,
including where the assistant was wrong and we had to override it.

We went deep on the parts we believe decide whether this system is
trustworthy, and [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) is honest about the
parts we left thin. We would rather show you a sharp edge and an admitted gap
than a uniform surface.
