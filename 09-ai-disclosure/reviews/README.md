# Adversarial review

We had a different model attack our own decisions, and published what it said.

## Why a different model

The architecture was drafted with AI assistance. Asking the same assistant to
review it would share its blind spots, which is the same reason we do not let a
model score its own output in
[5_1](../../05-ai-assurance/5_1-evaluation-strategy.md).

So the review was run in VS Code with GitHub Copilot, against a different model
family, with no context from the drafting session.

## Method

Each prompt was given the relevant files and asked to find weaknesses, not to
summarize. Output is recorded **verbatim**, including the findings we think are
wrong, because publishing only the flattering half would make this worthless.

Each finding gets one of three responses:

| Response | Meaning |
|---|---|
| **Fixed** | It was right, we changed the document |
| **Accepted, not fixed** | It was right, we ran out of time. Now in OPEN-QUESTIONS.md |
| **Rejected** | We think it is wrong, and here is why |

## Findings

See [findings.md](findings.md).

## What this is not

It is not validation by a practitioner. A model reviewing an architecture
catches structural weaknesses, unsupported claims and missing alternatives. It
cannot tell us whether a 2 percent false negative rate is achievable with
non-invasive sensing on a Bavarian estate. Those remain in
[2_6-claim-confidence.md](../../02-requirements/2_6-claim-confidence.md).
