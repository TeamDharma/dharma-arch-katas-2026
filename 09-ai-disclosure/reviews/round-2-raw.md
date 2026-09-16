# Round 2: raw output

The revised ADRs handed back to the same reviewer. Reproduced as received,
unedited apart from trimming the file-read log. Our response is in
[findings.md](findings.md).

---

The revisions are materially better, but only one of the three arguments is close to defensible.

## 1. Jurisdiction: still not an accepted decision

> "Germany and Austria were both defensible and we had to pick one. ... At that point the choice was a coin toss and we took Germany."

— `ADR-0001`

### What improved

You removed the false claim that `von` rules out France and stopped claiming that Germany should be chosen because its regulations make the architecture more interesting. The variation-point table is useful.

### What remains weak

An acknowledged coin toss is not an accepted architecture decision. It is a planning assumption. Labeling it "Accepted" still launders missing stakeholder information into certainty.

This statement is also overconfident:

> "Nothing in the architecture changes. What changes is a set of parameters..."

That is not demonstrated and is contradicted by the table immediately above it. A different fiscal device is an integration change, not merely a parameter. Heritage rules can change permissible sensor placement and therefore topology. Employment law can alter workflow and authorization boundaries. Moving outside the EU would affect far more than configuration.

The document also says the choice creates a ripple through several ADRs and the cost model, while simultaneously claiming that Austria would require only reconfiguration. Both cannot be true without a concrete impact analysis.

### What a rigorous version now needs

- Change the status to **Provisional** or **Accepted planning assumption**, with an owner and confirmation deadline.
- Define the triggering condition: "This decision becomes accepted when the physical location and operating entity are confirmed."
- Replace "nothing changes" with a bounded claim supported by a portability matrix at component, data, integration, and operational-process level.
- Include at least one non-EU scenario because the ADR considered the UK.
- Estimate the cost and elapsed time of changing jurisdiction.
- Distinguish configuration changes from adapter replacement, schema migration, data deletion/retention changes, and redesigned human workflows.
- State which implementation work is blocked until legal confirmation.

**Verdict:** improved honesty, but still the weakest of the three. The unsupported assumption remains; it is merely documented more accurately.

---

## 2. Spend ceiling: clearer accounting, but the actual decision is still unjustified

> "Metered vendor inference is capped at **EUR 0.10 per admission**, with a budget guard that begins degrading unprotected Tier 2 capabilities when rolling spend reaches EUR 0.08."

— `ADR-0014`

### What improved

The denominator is now precise. The ADR correctly limits its claim to volatile vendor billing, explicitly excludes total capability economics, and replaces the vague "accessibility last" promise with reserved capacity.

### What remains weak

The two decisive numbers, EUR 0.10 and EUR 0.08, are still invented. Nothing derives them from margin, budget, attendance distribution, expected usage, or provider-price volatility.

The reserved floor is also unspecified:

> "A fixed portion of the budget is allocated to them..."

What portion? Based on what demand forecast? Is it per day, per week, or per admission? Can unused reserved capacity be borrowed? What happens when protected demand itself exceeds the reservation? Without those answers, this is not an enforceable policy.

There is also a direct contradiction:

> "It does not answer 'does this capability earn its keep'."

But the consequences still claim:

> "It gives a concrete answer to whether each capability earns its cost."

Delete the second statement. The ADR now correctly explains why it is false.

The enforcement model is incomplete. A rolling seven-day average does not produce a hard EUR 0.10 cap. Spend can exceed the ceiling before the average or hourly monitor reacts. FF-11 measures expenditure; it does not prove that the ceiling cannot be breached.

Finally, the text changes the denominator to "admission," but verification still says "spend per visitor." Terminology must be exact in a financial control.

### What a rigorous version now needs

- Derive the ceiling from an approved annual or monthly budget and conservative admission forecast.
- Show expected and p95 spend by capability under normal, peak, abuse, and provider-price-increase scenarios.
- Specify the reserved accessibility amount and its replenishment period.
- Define whether reservation borrowing is allowed.
- Add a short-window or projected-spend control to complement the seven-day metric.
- Distinguish warning threshold, degradation threshold, and hard enforcement threshold.
- State the behavior when protected demand exceeds its reservation.
- Replace every remaining "visitor" denominator with "scanned admission."
- Remove the false capability-economics consequence.
- Verify maximum overshoot under the worst allowed monitoring and billing delay.

**Verdict:** substantially improved structure, but the business threshold, the heart of the ADR, still has no derivation.

---

## 3. Piranha interval: the argument is now credible, but the acceptance test is incomplete

> "The capability emits a **95 percent prediction interval for the true population under declared operating conditions**, never a bare number."

— `ADR-0011`

### What improved

This fixes most of the original problem. The ADR now defines interval semantics, names an estimator class, adds absolute thresholds, refuses out-of-distribution estimation, and tests empirical coverage. That converts the interval from presentation formatting into a potentially meaningful measurement.

### What remains weak

The `0.15` trigger is still arbitrary. Defining it precisely does not justify it. It must come from the smallest estimation uncertainty compatible with a keeper's decision, not from architectural preference.

The coverage criterion is underspecified:

> "Empirical coverage ... must fall between 90 and 98 percent..."

Coverage cannot be accepted or rejected without a sample size and statistical test. Nine successes in ten observations gives 90% empirical coverage but proves almost nothing. A fixed observed percentage range also behaves badly across sample sizes. You need a confidence bound or calibration test, not just raw sample coverage.

"Subgroup results reported by turbidity band" is insufficient. The estimator is conditioned on lighting and observable proportion too, and the consequences identify feeding state and season as calibration variables. Reporting only turbidity can hide failure in the other dimensions.

"Physical counts remain the ground truth" is still an assertion. Fish counts can themselves be uncertain. The ADR must define the reference method, repetition, observer agreement, and treatment of disagreement.

There is also a structural inconsistency:

- The system can output `measurement unavailable`.
- FF-26 says "100 percent of outputs must carry an interval."

Either unavailable is not considered an estimate output, or FF-26 will reject the required refusal behavior. Define a tagged result type such as `Estimate | MeasurementUnavailable` and test both branches.

Finally, this consequence is now obsolete:

> "Trend alerting catches the thing that actually matters..."

The revised decision correctly says absolute bounds also matter. The consequence should not continue claiming that trend is the singular important outcome.

### What a rigorous version now needs

- Derive the 15% threshold from keeper decisions and the consequences of false negatives and false positives.
- Define minimum calibration and validation sample sizes.
- Use a statistical calibration test or confidence bounds around observed coverage.
- Validate across every conditioning dimension, including combinations, not only turbidity.
- Define temporal holdout validation so repeated observations of the same population do not create fake sample independence.
- Specify the physical reference-count protocol and its uncertainty.
- Model the output as an explicit tagged union and update FF-26 accordingly.
- Remove the obsolete claim that trend is the only thing that matters.

**Verdict:** no longer one of the three weakest arguments in the ADR set. It has moved from statistical theatre to a plausible design requiring threshold provenance and a real validation protocol.
