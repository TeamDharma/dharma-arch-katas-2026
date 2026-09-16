# Round 3: raw output

Third pass over the same three ADRs after acting on round 2. Reproduced as
received, file-read log trimmed. Our response is in [findings.md](findings.md).

---

## Current verdict

| ADR | Verdict | Remaining problem |
|---|---|---|
| `ADR-0001` | **Pass at kata fidelity** | Legal assertions remain hypotheses, as now stated |
| `ADR-0011` | **Conditional pass** | Statistical acceptance criterion is still weak |
| `ADR-0014` | **Fail** | The ceiling remains arbitrary and is not actually enforced as a ceiling |

## 1. Jurisdiction: fixed

> "**Accepted as a planning assumption.** Not a settled fact."

— `ADR-0001`

This is now correctly framed. The ADR:

- distinguishes assumption from fact;
- names an owner and blocker;
- acknowledges that the evidence does not establish location;
- separates configuration, integration, physical, and workflow changes;
- treats moving outside the EU as an uncosted structural change;
- explicitly requires legal confirmation before implementation.

Not estimating migration cost is acceptable for this kata because the omission is now disclosed rather than hidden behind "nothing changes."

One sentence remains bad:

> "But `von` does not fit..."

A surname still says nothing useful about whether an estate is in the UK. Delete that clause and retain only the valid statement that the imagery motivated the planning assumption.

There are also legal details that require verification, the applicability of GDPR and other EU regimes does not simply "fall away" whenever an organization is outside the EU, but the ADR now labels all such claims as hypotheses.

**Result:** this is no longer one of the weak arguments.

---

## 2. Piranha interval: architecture fixed, statistics not quite fixed

The tagged result, refusal behavior, multidimensional reporting, temporal holdout, and distinction between absolute and trend alerts resolve the architectural defects.

The remaining weak claim is:

> "Pass condition: The 95 percent confidence bound on coverage contains 0.95."

— `ADR-0011`

That is not a strong calibration acceptance test. With only 40 observations, a genuinely under-covering model can still produce a wide confidence interval containing `0.95`. The test rewards uncertainty caused by a small sample.

It also does not say which binomial interval is used. Wald intervals are particularly unsuitable near `0.95`. More importantly, the real requirement is not "we failed to prove the coverage differs from 95%." It is "we have positive evidence that undercoverage is not operationally material." Failure to reject a bad model is not proof that the model is good.

Forty total observations also cannot support meaningful subgroup conclusions across turbidity, lighting, visible proportion, feeding state, and season. Reporting those subgroups does not make them statistically informative.

Two old defects also remain:

- The `0.15` width trigger is precisely defined but still not justified by a keeper decision.
- "Physical count" is called ground truth without defining its own measurement protocol or error.

### Required correction

Use an explicit non-inferiority criterion, for example:

- Define minimum acceptable coverage, such as `0.90`, separately from nominal coverage of `0.95`.
- Require the one-sided lower confidence bound on coverage to exceed the minimum.
- Use an exact binomial or Wilson-based method named in the ADR.
- Derive sample size from desired power and maximum tolerated undercoverage.
- Set minimum observations per operational stratum rather than merely reporting subgroups.
- Define the physical-count reference protocol and reconciliation of observer disagreement.
- Have keepers derive the width threshold from the smallest uncertainty compatible with a specific action.

Also replace:

> "An interval that does not contain the truth about 95 percent of the time is not a confidence interval."

It is a **prediction interval**, as the ADR correctly says elsewhere. Do not switch terminology.

**Result:** credible design, incomplete validation protocol.

---

## 3. Spend ceiling: still not defensible

The reservation is now concrete, the denominator is consistent, and the false capability-economics claim is gone. But the central number remains unsupported:

> "Twenty five percent is sized from expected translation and description volume at the projected visitor mix..."

— `ADR-0014`

Where is that forecast? What visitor mix, interaction rate, tokens per interaction, price schedule, and percentile were used? This is an assertion about a calculation that the ADR does not expose or reference.

More seriously, the control contradicts its own claim:

> "Metered vendor inference is capped at **EUR 0.10 per admission**..."

But verification permits:

> "Rolling 24 hour: **EUR 0.12**"

A control that reacts at EUR 0.12 does not cap expenditure at EUR 0.10. It allows at least 20% overspend before billing latency and monitoring delay.

The reservation semantics are also unresolved:

> "If protected demand exceeds the reservation, the reservation is extended from unprotected budget..."

What happens after all unprotected budget is consumed? The ADR alternately claims:

- accessibility has a protected floor;
- accessibility is "last" to degrade;
- the total is capped at EUR 0.10.

All three cannot hold under unbounded protected demand. Either protected service eventually degrades, or the total ceiling is soft. Pick one.

"Projected to period end" does not define the period, projection algorithm, demand forecast, or required confidence margin. "Maximum overshoot is bounded" is also empty without an actual bound.

### Required correction

The ADR needs:

1. **A derivation table** for EUR 0.10, EUR 0.08, and 25%, including source assumptions.
2. **Explicit semantics:** hard cap, soft target, or budget forecast. Right now it uses all three interchangeably.
3. **A terminal protected-service mode** when the total budget is exhausted, for example local deterministic accessibility content with no metered inference.
4. **A quantified overshoot bound** based on maximum request concurrency, billing delay, local accounting delay, and already-authorized calls.
5. **A defined accounting period** and projection algorithm.
6. **Thresholds below the ceiling.** A EUR 0.12 reaction threshold cannot enforce a EUR 0.10 cap.
7. **A validation scenario** proving the worst-case spend remains within the declared bound during a price increase, traffic spike, billing delay, and protected-demand surge.

**Result:** still the weakest of these three. It has more operational detail, but the business number remains invented and the supposed cap is mathematically not a cap.
