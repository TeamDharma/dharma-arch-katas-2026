# Adversarial review: findings

Model used: GitHub Copilot in VS Code, a different model family from the one
that drafted this repository. That independence is the point. A model reviewing
its own output shares its blind spots, which is the same reason we do not let a
model score its own work in
[5_1](../../05-ai-assurance/5_1-evaluation-strategy.md).

Date: 2026-09-16, the day of submission.

Raw output is recorded as received. Our response follows each finding.

---

## Round 1: trade-off rigor in the ADRs

**Prompt used:**

```
You are a senior architect reviewing these ADRs with an ATAM background.
Find the three weakest arguments. For each: quote the claim, say why it is
weak, and say what a rigorous version would look like. Be specific and do not
be polite. Do not summarize the documents back to me.
```

**Files given:** all sixteen ADRs.

### Raw output

The full response is reproduced in [round-1-raw.md](round-1-raw.md). Summarized
here by finding, with our answer.

### Finding 1: Bavaria is inferred from decorative clues, then preferred because its laws are more interesting

> "'French would be `de`, which rules out France' is simply invalid: a
> German-named owner can own an estate in France. Worse, Germany is selected
> partly because its regulations create more interesting design constraints.
> That reverses the causal direction."

**Response: partly accepted, partly rejected.**

**Accepted.** The France deduction was invalid and we have removed it. A
nobiliary particle indicates the owner's linguistic origin, not where the estate
stands. We also removed the sentence claiming Germany's constraints "do more
architectural work", because that does invert the causality. The honest account
is that Germany and Austria were both defensible, our only substantive reason to
prefer Austria dissolved once we could name a single Bavarian supervisory
authority, and at that point it was a coin toss. ADR-0001 now says so.

**Accepted, and acted on.** The reviewer's best suggestion was to state the
variation points. ADR-0001 now carries a table of what actually changes if the
estate is not in Bavaria. The answer is: a fiscal device, a retention period, a
consent age, and which supervisory authority we name. No part of the
architecture changes. That is a stronger position than the one we had, and we
would not have written it unprompted.

**Rejected.** The proposed remedy, establishing the operating entity and running
a three jurisdiction sensitivity analysis with legal confirmation and deadlines,
assumes a client who can be asked. There is no Countess. The brief states no
location, the organizers confirmed greenfield, and some assumption is
unavoidable. Modelling three jurisdictions in full would consume the submission
to resolve a fictional fact. We think stating the assumption, showing the
variation points, and flagging every regulatory claim as requiring legal
confirmation is the proportionate answer.

### Finding 2: the AI budget numbers are invented and disconnected from business value

> "'Per visitor' is also an unjustified allocation unit... The ADR never defines
> whether 'visitor' means ticket sold, admission scanned, unique credential, or
> estimated footfall."
>
> "It also excludes edge inference because it is capital expenditure, then claims
> to answer whether each capability 'earns its cost.' That claim is false."
>
> "'Accessibility and translation, last' sounds virtuous but is not an
> operational policy."

**Response: accepted, three changes made.**

**The denominator is now defined.** An admission scanned at a turnstile. Not a
ticket sold, which would flatter the figure with no-shows, and not estimated
footfall, because a budget should not be denominated in an estimate.

**The scope claim is corrected.** The ceiling governs metered vendor inference
billing, which is the cost that is volatile and outside our control. It does not
measure capability economics, and the ADR previously came close to claiming it
did. Edge inference, engineering, evaluation and baseline maintenance are in the
cost model, not in this control.

**Accessibility now holds a reserved floor rather than last place in a queue.**
This was the most useful finding in the whole review. An ordering only delays the
outcome: under sustained pressure the queue eventually reaches the thing you
said you would protect. FF-35 asserts the floor survives after everything else
has been degraded.

We also recorded, without solving, the fairness point the reviewer raised: a
seven day rolling window can hide a same day spike, and budget consumed in the
morning is not available to afternoon visitors. Our position is that degrading a
capability for everyone is coarse but fair, whereas refusing individual visitors
is not. A per-day sub-limit would tighten it and we have not designed one.

**Partly rejected.** The reviewer treats "the ceiling is our estimate, not the
Countess's budget" as fatal. There is no Countess to ask. Stating that a number
is ours is honesty, not a defect, and
[2_6-claim-confidence.md](../../02-requirements/2_6-claim-confidence.md) already
sorts every such number by how much we doubt it.

### Finding 3: the piranha confidence interval is statistical theatre

> "Requiring every output to carry an interval verifies serialization, not
> honesty. A structurally valid but catastrophically miscalibrated interval
> passes FF-26."

**Response: accepted almost entirely. This was the best finding.**

It is correct, and it is uncomfortable because this capability is the one we
point at as an example of honest treatment of uncertainty. We were checking the
shape of an output and calling it integrity.

Changes made:

| Weakness | Fix |
|---|---|
| No interval semantics | Now a 95 percent prediction interval for the true population under declared conditions. Width is high minus low as a proportion of the estimate |
| "15 percent" ambiguous | Now stated as width above 0.15 of the estimate |
| No coverage validation | **FF-33 added.** Empirical coverage against independent physical counts must fall between 90 and 98 percent, with subgroup results by turbidity band |
| Trend-only alerting | Now absolute bounds set per enclosure by keepers and a veterinarian, **and** trend break |
| Wider interval outside calibration | **Now refuses to estimate.** FF-34 asserts it. Adopted directly from the reviewer's suggestion, which is better than what we had |
| No estimator named | Repeated observations combined with a calibrated detection probability model |

**Not fixed, and recorded as such.** The reviewer asks that the physical count
trigger be derived from decision loss rather than from a percentage, and that
physical counts carry their own stated error rate with an adjudication procedure
for disagreements. Both are right. Neither was reachable in the time remaining,
and they are now in [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md).

---

## Round 2: re-review after acting on round 1

We handed the revised ADRs back to the same reviewer. It was sharper than the
first pass, and it caught a pattern in how we had made the fixes.

**Raw output:** [round-2-raw.md](round-2-raw.md).

### The pattern worth naming

Three of its findings were the same defect: **we edited the Decision section of
an ADR and left the Consequences or Verification section contradicting it.**

| ADR | Decision said | Stale section still said |
|---|---|---|
| 0014 | "It does not answer whether this capability earns its keep" | "It gives a concrete answer to whether each capability earns its cost" |
| 0014 | Denominator is a scanned admission | Verification measured "spend per visitor" |
| 0011 | Output may be "measurement unavailable" | FF-26 required 100 percent of outputs to carry an interval, which would reject that |
| 0011 | Absolute bounds and trend both matter | "Trend alerting catches the thing that actually matters" |

The third row is the worst of them. We wrote a decision mandating a refusal
behaviour and a fitness function that would have rejected it, in the same
document, in the same edit.

This is the identical failure recorded in [../README.md](../README.md): confident
output never checked against a source. Our architecture consistency checker
catches drift **between** documents and had nothing to say about a document
contradicting itself. That is a real gap in our tooling and we are recording it
rather than quietly patching around it.

### Finding 1: jurisdiction is still not an accepted decision

> "An acknowledged coin toss is not an accepted architecture decision. It is a
> planning assumption. Labeling it 'Accepted' still launders missing stakeholder
> information into certainty."

**Response: accepted.** Status is now **Accepted as a planning assumption**,
with the confirmation condition stated and an owner named.

> "'Nothing in the architecture changes' ... is not demonstrated and is
> contradicted by the table immediately above it."

**Response: accepted, this was an overclaim.** Replaced with a four level
portability table separating configuration from adapter replacement from
physical topology from workflow. Moving to Austria is adapter replacement plus
configuration. Moving outside the EU replaces the entire regulatory basis, and
we say so instead of implying otherwise. The contradicting consequence has been
corrected too.

**Rejected:** costing the elapsed time of a jurisdiction change, and modelling a
non-EU scenario in full. Disproportionate for a fictional estate. We say in the
ADR that we would do it for a real one.

### Finding 2: the spend ceiling numbers are still unjustified

**Accepted, four changes.** The self-contradiction is gone. The denominator is
consistent throughout. The reserved accessibility floor is now specified: 25
percent of the ceiling, daily replenishment, no borrowing out of it, borrowing
into it permitted, and a stated behaviour when protected demand exceeds it. And
FF-11 now runs on three horizons, because a seven day average cannot enforce a
cap and a same day spike could run most of a day before it moved.

We also state the residual: with hourly monitoring and provider billing latency,
spend can exceed the ceiling for up to one reporting interval. The guard sits
below the ceiling to absorb that, and the overshoot is bounded rather than
denied.

**Rejected in our first response, conceded here.** We had answered that EUR
0.10 was derived from the operating budget. That derivation was circular: the
38 percent share of operating cost had itself been computed from the ceiling.
The input is a policy choice, 0.25 percent of assumed yield, checked against
three routing scenarios. ADR-0014 and
[6_2](../../06-economics/6_2-ai-spend-ceiling.md) say so, and
[2_6](../../02-requirements/2_6-claim-confidence.md) files the ceiling as a
conventional default rather than a derivation. What remains true is that nobody
can derive it from a margin the Countess has never stated, because there is no
Countess.

### Finding 3: piranha is credible but the acceptance test is incomplete

**Accepted, three changes.**

The output is now an explicit tagged type, `Estimate | MeasurementUnavailable`,
and the harness tests **both branches**. FF-33 now specifies a minimum sample of
40 paired observations and a binomial confidence bound rather than a raw
percentage range, because nine successes in ten is 90 percent coverage and
proves almost nothing. Subgroups are reported across every conditioning
dimension rather than turbidity alone, with temporal holdout so repeated
observations of one population do not manufacture independence.

**Already open, not newly accepted.** Threshold provenance for 0.15 and the
physical count protocol were both raised in round 1 and are in
[OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md). Round 2 restated them and they
remain open.

**Verdict quoted, because it is the honest score:** "no longer one of the three
weakest arguments in the ADR set. It has moved from statistical theatre to a
plausible design requiring threshold provenance and a real validation
protocol." 

---

## Round 3: the one that failed us

**Raw output:** [round-3-raw.md](round-3-raw.md).

| ADR | Verdict |
|---|---|
| 0001 Jurisdiction | Pass at kata fidelity |
| 0011 Piranha | Conditional pass |
| **0014 Spend ceiling** | **Fail** |

### ADR-0014 failed, and we had made it worse

> "A control that reacts at EUR 0.12 does not cap expenditure at EUR 0.10."

That threshold did not exist before round 2. **We introduced it while fixing
something else**, which is the second time in this review cycle that a repair
created a new defect.

It also identified a trilemma we had not seen: a protected accessibility floor,
accessibility degrading last, and a hard total cap cannot all hold under
unbounded protected demand.

**Response: accepted in full. ADR-0014 was rebuilt rather than patched.**

| Defect | Fix |
|---|---|
| Threshold above the cap | Every threshold now below it: degrade at 0.08, 24 hour at 0.09, **hard stop at 0.095** |
| No derivation | Derivation table from the EUR 975,000 operating budget and the 3.75 million admission forecast |
| 25 percent asserted, not calculated | Arithmetic shown: 15 percent of visitors at roughly twice the interaction volume, rounded down for cached content |
| Period and projection undefined | Calendar month, linear extrapolation of the trailing 7 day rate |
| "Overshoot is bounded" with no bound | 200 concurrent calls at EUR 0.02 max, **EUR 4 absolute**, about 200 times smaller than the margin |
| The trilemma | **A non-metered terminal mode.** At the hard stop accessibility serves from local cached content at zero marginal cost. It is never dark, and the cap still holds |

The terminal mode is the real fix, and it only works because
[ADR-0006](../../07-decisions/ADR-0006-heuristic-baseline-retained-permanently.md)
keeps every baseline permanently, a decision made months of narrative time
earlier for a different reason.

**One further change, not asked for.** Working through the overshoot bound made
it obvious that a billing-driven control cannot enforce this cap at all: an hour
of unobserved peak spend exceeds the entire margin. Metering is now local at the
gateway on every call, with provider billing as reconciliation. The review did
not ask for that. Its question about the overshoot bound forced it.

### ADR-0011: statistics corrected

> "Failure to reject a bad model is not proof that the model is good."

Correct, and our test was exactly that failure. Asking whether a confidence
bound contains 0.95 passes any under-covering model whose sample is small enough
to make the bound wide. It rewarded weak evidence.

Now a **non-inferiority test**: minimum acceptable coverage 0.90 stated
separately from nominal 0.95, one sided lower **Wilson** bound named explicitly
because Wald is unsuitable near 1, minimum 120 paired observations derived from
where the bound crosses 0.90, and 30 per stratum before any stratum verdict.
Terminology fixed to prediction interval throughout.

**And an honest consequence we added ourselves.** 120 physical piranha counts is
more than the operation can cheaply produce. The capability will not reach a
validated state for a year or more, and some strata may never qualify. So it now
runs **provisional** until the sample exists, published as provisional, with the
keeper told the calibration is unproven. The old threshold of 40 would have
produced a confident pass from evidence that could not support it.

### ADR-0001: passed, one clause removed

The surname clause about the UK is gone. A name says nothing about where an
estate stands, and we had left that reasoning in one place after removing it
from another.

We also corrected an overclaim the reviewer flagged in passing: EU obligations
do not simply fall away outside the EU, since GDPR and the AI Act both reach
organizations targeting people inside it. We now say we have not analyzed it
rather than implying it is simple.

### Still open after three rounds

Two items, both raised in round 1 and restated twice:

- The 0.15 interval width trigger is precisely defined and still not derived
  from a keeper's decision.
- Physical counts are treated as ground truth without their own protocol or
  error rate.

Both are in [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md). Three rounds did not
make us able to answer them inside the kata window, and restating them a fourth
time would not either.

---

## Summary

Three findings. Two landed hard, one was half right.

| | Count |
|---|---|
| Fixed | 8 specific changes across ADR-0001, ADR-0011, ADR-0014, plus three new fitness functions |
| Accepted, not fixed | 2, both on piranha calibration, now in OPEN-QUESTIONS.md |
| Rejected with reasons | 2, both where the remedy assumed a client we do not have. One of them, on the ceiling's derivation, is conceded above |

**The most valuable finding was that FF-26 checks serialization, not honesty.**
We had a fitness function asserting that an interval exists and were treating
that as evidence the interval meant something. FF-33 now measures whether
nominal 95 percent intervals actually contain the truth 95 percent of the time.

That is the same failure this submission spends seventy documents warning about,
committed by us, in the capability we hold up as our example of getting it right.
Finding it in our own work an hour before submission is the most useful thing
this review could have done.

**The second most valuable was the accessibility floor.** We had written an
ordering and called it protection. An ordering under sustained pressure
eventually reaches the thing at the end of it.

Rounds 2 and 3 re-reviewed the fixes. Round 2 found **four self-contradictions**
we had introduced while making them. Round 3 **failed ADR-0014 outright** on a
threshold we had added in round 2, which above the cap it was supposed to
enforce.

Twice in three rounds, a repair created a new defect. That is the most useful
thing in this file.

That is the most instructive thing in this file. Our automated checker catches
drift between documents and is blind to a document contradicting itself, which
is a real gap we have recorded rather than quietly patched.

Three rounds, ending with ADR-0014 rebuilt rather than patched, ADR-0011's
acceptance test changed from a difference test to a non-inferiority test, and
ADR-0001 passing. Two findings remain open and are recorded as open.
