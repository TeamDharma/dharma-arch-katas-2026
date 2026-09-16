# ADR-0011: Report piranha population as an interval, never as a count

## Status

Accepted

## Context

The brief asks us to check population levels of the jumping piranha collection.

Counting fish reliably by camera is not a solved problem. They move, they
occlude one another, they are numerous, and the water is not always clear.
Turbidity varies seasonally and after feeding.

A detection model will produce a number. It will demo well. It will also be
wrong in ways nobody can detect from the output, which means it will be used as
though it were right.

Alternatives considered:

- **Report the model's count.** Simple, familiar, and it launders an unreliable
  measurement into an authoritative-looking figure. The failure mode is silent.
- **Report the count with an accuracy caveat in the documentation.** Caveats in
  documentation do not travel with the number into a spreadsheet or a decision.
- **Report a calibrated interval, alert on both absolute bounds and trend,
  refuse to estimate outside calibration, and validate coverage empirically.**

## Decision

The capability emits a **95 percent prediction interval for the true population
under declared operating conditions**, never a bare number.

**Interval semantics, stated precisely** because an earlier draft left them
ambiguous:

| Term | Definition |
|---|---|
| Interval | 95 percent **prediction** interval for the true population, not a confidence interval on a parameter, not a standard error, not a half-width. The term does not change anywhere in this repository |
| Width | `high` minus `low`, expressed as a proportion of the point estimate |
| Trigger | Width above **0.15** of the estimate requests a physical count |
| Estimator | Repeated observations across a session combined with a calibrated detection probability model conditioned on turbidity, lighting and observable proportion |

**Alerting is on both absolute thresholds and trend break**, not trend alone.
Keepers and a veterinarian set absolute bounds per enclosure for capacity,
welfare and mortality. An earlier draft alerted on trend only, which would have
missed a population outside a safe absolute range that happened to be stable.

**The output is a tagged type, not a number that may be missing.**

```
PopulationResult =
    Estimate { point, interval_low, interval_high, conditions, model_version }
  | MeasurementUnavailable { reason, conditions, model_version }
```

**Under out of distribution conditions the system returns
`MeasurementUnavailable`.** When turbidity, lighting or observable proportion
fall outside the range the calibration covers, the output is an explicit refusal
carrying its reason, not a wider interval.

Modelling this as a tagged type rather than an optional field matters. An
earlier version had FF-26 requiring that 100 percent of outputs carry an
interval, which would have rejected the refusal behaviour the same ADR
mandates. Adversarial review caught the contradiction. Both branches are now
tested. A very wide interval carries a false implication that the number
inside it means something.

Periodic physical counts remain the ground truth, calibrate the model, and
**validate that the intervals are honest**. They are never replaced by it.

## Consequences

+ The output communicates its own reliability, so a keeper can tell when to
  trust it.
+ Absolute bounds catch a population outside a safe range, and trend break
  catches gradual change that stays inside it. Neither alone is sufficient, and
  an earlier version of this ADR claimed trend was what mattered.
+ Degrading conditions produce a request for human verification rather than a
  quietly worse number.
+ It models the honest treatment of any uncertain measurement, and the pattern
  generalizes to the rest of the system.
− An interval is harder to put on a dashboard and harder to explain than a
  number. Someone will ask for the midpoint.
− **Calibration is a real cost.** Honest intervals require observations across
  population sizes, turbidity, lighting, feeding states and seasons. Until that
  data exists the capability runs in refuse-to-estimate mode more often than it
  reports, which will look like failure and is the correct behavior.
− Absolute thresholds have to be set by keepers per enclosure, which is work
  the capability cannot do for them.
− Physical counts remain necessary, so the capability reduces effort rather than
  removing it.
− We cannot answer "how many piranhas are there" precisely, which is
  superficially what was asked.

## Verification

FF-26 is a structural check: **every `Estimate` must carry an interval and every
non-estimate must be an explicit `MeasurementUnavailable` with a reason. A bare
number fails the build.** It is the only fitness function in this repository
that fails a build over an output format, and it earns that because a single
code path returning a bare integer destroys the entire value of the capability.

**FF-26 alone is not sufficient, and adversarial review caught that.** A
structurally valid but badly calibrated interval passes it. FF-33 closes that
gap by measuring empirical coverage against independent physical counts.

Coverage is tested statistically rather than as a raw percentage, because nine
successes in ten observations is 90 percent coverage and proves almost nothing:

| Property | Value |
|---|---|
| Nominal coverage | 0.95 |
| **Minimum acceptable coverage** | **0.90.** Stated separately, because the question is not whether coverage differs from nominal, it is whether undercoverage is operationally material |
| Test | **One sided lower Wilson score bound** on observed coverage. Wald is unsuitable this close to 1 and is not used |
| Pass condition | The lower bound must **exceed 0.90**. Failing to reject a bad model is not evidence of a good one |
| Minimum sample | **120 paired observations.** At true coverage 0.95 the Wilson lower bound crosses 0.90 at roughly n=100, so 120 gives usable power rather than a verdict driven by sample size |
| Per stratum | **30 paired observations minimum** before any stratum-level verdict. Below that the stratum is reported as not yet assessed |
| Strata | Turbidity, lighting, observable proportion, feeding state, season |
| Independence | Temporal holdout. Repeated observations of one population within a session count once |

A prediction interval that does not contain the truth about as often as it
claims is decoration with error bars.

**The uncomfortable consequence.** 120 paired observations means 120 physical
counts, and a physical count of a piranha enclosure is expensive. At a realistic
cadence this capability will not reach a validated state for a year or more, and
several strata may never reach 30 observations at all.

We are not going to pretend otherwise. Until the sample exists the capability
runs in a **provisional** state: estimates are published, labelled provisional,
and a keeper is told the calibration is unproven. That is a worse product than
the one implied by the fitness function, and it is the true one. An earlier
threshold of 40 observations would have produced a confident pass from evidence
that could not support it.

FF-27 monitors interval width daily and triggers physical verification above
0.15, with suppression not permitted. Systematic bias is checked against
physical counts, and a capability that cannot be de-biased is withdrawn rather
than tolerated.

Adversarial review of this ADR, and our response, is in
[../09-ai-disclosure/reviews/findings.md](../09-ai-disclosure/reviews/findings.md).
