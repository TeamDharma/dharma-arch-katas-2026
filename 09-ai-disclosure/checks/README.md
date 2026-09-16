# Automated checks

Three runnable check suites, nineteen checks. No dependencies except where
noted, and no claim about who ran them, because nothing here needs a person.

Automated review is the only kind this team had time for. It is narrower than a
practitioner reading the assurance section, and it is honest about what it
covers.

## Run everything

```bash
python3 09-ai-disclosure/checks/check-docs.py
python3 09-ai-disclosure/checks/check-architecture.py
python3 code/eval/run_evals.py
```

All three exit non-zero on failure. Standard library only.

## 1. Documentation checks

`check-docs.py`, five checks.

| Check | Catches |
|---|---|
| em-dashes | A style rule we set and would otherwise break |
| unexpected non-ASCII | Stray characters, against a short allowlist of German and our own notation |
| broken relative links | Files that moved, and references to files deleted |
| diagram keys | A diagram without an inline key, which the brief explicitly asks for |
| requirement counts | Prose claiming 48 requirements when the table contains a different number |

The last one is the useful one. A document that counts itself in prose drifts
from its own table the moment anyone edits it, and nobody rereads a summary
paragraph after adding a row. This check exists because exactly that happened.

## 2. Architecture consistency checks

`check-architecture.py`, seven checks. This is the one worth reading, because it
tests the claims this submission actually makes.

| Check | The claim it tests |
|---|---|
| Fitness function references | Every `FF-nn` cited anywhere is defined in `2_4`. Thirty one defined, three added after the adversarial review and one after the flow-tracing pass |
| Requirement verification | Every one of the 48 requirements names a verification method. No requirement is a wish |
| ADR references | Every `ADR-nnnn` referenced exists as a file |
| Scenario completeness | **Every AI capability states its tier, fallback and verification.** Our stated rule, made mechanical |
| Degraded mode matrix | No blank cells across 17 capabilities and 6 failure conditions. This is FF-04 |
| Characteristic coverage | Every one of the 7 characteristics has at least one fitness function |
| Headline number consistency | The AI ceiling, the capital budget and the visitor figures do not contradict each other, and neither superseded figures nor the phrases superseded when ADR-0014 moved accessibility to a reserved floor linger |

### What it found

Running it for the first time surfaced two real inconsistencies:

**`NFR-32` still carried a superseded operating cost.** It said under EUR 600,000
per year at target scale. The bottom up cost model had revised that to EUR
975,000 at target and EUR 495,000 today, and the NFR had not followed.

**Testability had no fitness function naming it.** It is the fourth ranked
architecture characteristic and every AI check serves it, but none said so, so
a reader tracing characteristics to checks would have found a gap. Now stated
explicitly.

Neither would have been caught by reading. Both are the kind of drift that
happens when seventy documents are written quickly, and both are exactly what a
consistency check is for.

## 3. Evaluation harness

[`../../code/`](../../code/), seven fitness functions against recorded fixtures.
Offline, no credentials. See its own README.

## Diagram rendering

`check-diagrams.sh` extracts every Mermaid block and renders it, then asserts
the legend rule.

**Needs a dependency**, unlike everything else here: `@mermaid-js/mermaid-cli`
and a headless Chrome. The script preflights both and exits with a distinct
code if either is missing, and it finds whatever Chrome puppeteer has installed
rather than hardcoding a path. It caught a diagram with an invalid empty link
label that read as correct.

Pass a second argument to also write the rendered PNGs somewhere. That is how
[`assets/diagrams/`](../../assets/diagrams/) is produced:

```bash
09-ai-disclosure/checks/check-diagrams.sh . assets/diagrams
```

## What automated checking does not cover

It cannot tell us whether 0.2 is the right drift threshold for piranha
enclosures, whether a 2 percent false negative rate is achievable with
non-invasive sensing, or whether EUR 40 of yield per visitor is realistic.

Those need a practitioner, and we did not have one available inside the kata
window. They are listed, sorted by how much we doubt them, in
[2_6-claim-confidence.md](../../02-requirements/2_6-claim-confidence.md).

Knowing the difference between what a script can check and what it cannot is
most of the point.
