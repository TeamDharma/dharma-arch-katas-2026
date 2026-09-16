# Round 1: raw output

Reproduced as received, unedited. The model's file-read log has been trimmed;
everything from the first heading onward is verbatim, including the em-dashes
and typography we do not use elsewhere, because editing a quoted review to match
our own house style would defeat the point of quoting it.

**Prompt given:**

```
You are a senior architect reviewing these ADRs with an ATAM background.
Find the three weakest arguments. For each: quote the claim, say why it is
weak, and say what a rigorous version would look like. Be specific and do not
be polite. Do not summarize the documents back to me.
```

**Files given:** all sixteen ADRs in `07-decisions/`.

Our response to each finding is in [findings.md](findings.md).

---

## 1. Bavaria is inferred from decorative clues, then preferred because its laws make the design "more interesting"

> "Two signals in the brief point the same way:
> 1. 'Von Digitalis' uses `von`, the German nobiliary particle. French would be `de`, which rules out France.
> 2. The deck uses Neuschwanstein Castle…"
>
> "Germany's constraints do more architectural work."

— `ADR-0001`

### Why it is weak

This is not architectural reasoning. It is fictional archaeology followed by jurisdiction shopping.

A surname does not establish where an estate operates. Stock photography establishes even less. "French would be `de`, which rules out France" is simply invalid: a German-named owner can own an estate in France. Worse, Germany is selected partly because its regulations create more interesting design constraints. That reverses the causal direction. Applicable law must constrain the architecture; architects do not select applicable law because it improves the presentation.

The consequences are material: tax retention, cash-register controls, employee monitoring, children's consent, heritage restrictions, and animal-record obligations all propagate from this unsupported assumption. Calling the ADR "accepted" turns speculation into a false architectural invariant.

Its verification is circular: checking that invented regulatory constraints influence the design does not verify that the constraints actually apply.

### What a rigorous version would look like

Treat jurisdiction as an unresolved business fact and run sensitivity analysis:

- Establish the actual operating entity, physical site, controller/processor roles, sales jurisdictions, employment jurisdiction, and applicable zoo licence.
- Separate invariant EU obligations from jurisdiction-dependent rules.
- Define at least Germany, Austria, and UK deployment scenarios and identify which components change under each.
- Record legal claims as hypotheses requiring qualified legal confirmation, with owner and deadline.
- Prevent jurisdiction-specific implementation until the site is confirmed, except where Germany is explicitly declared a stakeholder-imposed planning assumption.
- Quantify reversibility: affected schemas, retention policies, fiscal integration, consent flows, works-council controls, cost, and migration time.

A defensible decision would say: "For planning only, Germany is scenario G. The architecture must preserve these listed variation points until the owner confirms the site by date X." It would not pretend a castle photograph is regulatory evidence.

---

## 2. The AI budget numbers are invented and disconnected from business value

> "AI inference is capped at **EUR 0.10 per visitor**, with a **budget guard** that begins degrading Tier 2 capabilities when rolling spend reaches EUR 0.08."

— `ADR-0014`

### Why it is weak

Neither number is derived from anything. The ADR admits that explicitly:

> "The ceiling is our estimate, not the Countess's budget."

That destroys the central argument. A runtime control can enforce a number; it cannot make an arbitrary number economically correct.

"Per visitor" is also an unjustified allocation unit. Concierge demand will vary by language, accessibility need, weather, group composition, season, and repeat usage. A seven-day average can hide a same-day cost spike and can penalize later visitors because earlier visitors consumed the shared budget. The ADR never defines whether "visitor" means ticket sold, admission scanned, unique credential, or estimated footfall.

It also excludes edge inference because it is capital expenditure, then claims to answer whether each capability "earns its cost." That claim is false. Hardware depreciation, energy, maintenance, observability, engineering, evaluation, and fallback-operation costs are still costs. The mechanism measures one vendor-billing category, not capability economics.

The degradation order is equally unsupported. "Accessibility and translation, last" sounds virtuous but is not an operational policy. It provides no reserved capacity, minimum service level, demand forecast, or proof that earlier degradation leaves enough budget to protect them.

### What a rigorous version would look like

Start with unit economics and an explicit cost-allocation model:

- Define contribution margin per paid admission and the maximum percentage available for digital services.
- Estimate usage distributions by capability, not just averages: median, p95, peak-day, and adverse provider-price scenarios.
- Include full lifecycle cost: inference, embeddings, edge hardware amortization, energy, support, evaluation, monitoring, and baseline maintenance.
- Attribute measurable value to each capability: conversion uplift, reduced support demand, queue reduction, staffing savings, accessibility obligation, or avoided incident cost.
- Define the budget period and denominator precisely.
- Reserve protected capacity for accessibility and translation instead of merely putting them last in a shutdown list.
- Specify overload behavior per request and per capability, including fairness across visitors and languages.
- Derive warning and hard-stop thresholds from forecast error and response time. For example, trigger at the level that still leaves enough reserved budget to operate protected services through the end of the accounting period at p95 demand.
- Test scenarios such as a 10x price increase, a holiday attendance spike, one language consuming disproportionate traffic, and sustained abuse.

Only after that analysis could `EUR 0.10` and `EUR 0.08` be credible outputs rather than decorative precision.

---

## 3. The piranha "confidence interval" is statistical theatre

> "The capability emits a **population estimate with a confidence interval, never a bare number**. The interval is derived from observed conditions: turbidity, lighting and observable proportion of the enclosure."

— `ADR-0011`

### Why it is weak

Turbidity, lighting, and visible enclosure proportion do not magically produce a confidence interval. The ADR specifies neither:

- the estimator,
- the confidence level,
- the error model,
- calibration data,
- coverage validation,
- treatment of correlated occlusion,
- distribution shift,
- nor how physical counts constitute reliable ground truth.

Without those, the interval is just two numbers surrounding another number. Requiring every output to carry an interval verifies serialization, not honesty. A structurally valid but catastrophically miscalibrated interval passes FF-26.

The `15 percent` threshold is also unexplained. "15 percent of the estimate" is ambiguous - is that total interval width, half-width, or relative standard error? It is insensitive to population size and to the welfare consequence of missing a decline. For 20 fish, plus or minus 3 may be unacceptable; for 2,000 fish, plus or minus 300 may be operationally useless. The threshold is not tied to any keeper decision.

"Alerting is on trend break, not on absolute value" is particularly dangerous. Absolute thresholds may matter for enclosure capacity, welfare, breeding, mortality, and statutory records. Trend detection is also not inherently easier than estimation: autocorrelation, seasonality, feeding behavior, camera movement, and changing turbidity can all manufacture a trend break.

### What a rigorous version would look like

Define the decision first, then design the measurement:

- Identify the operational decisions the estimate supports and the smallest population change requiring action.
- Define separate absolute and trend-based alert rules with veterinarian or keeper approval.
- Specify the estimator and uncertainty method - for example, repeated observations combined with a calibrated detection-probability model.
- State the interval semantics, such as a 95% prediction interval for the true population under declared operating conditions.
- Build calibration data across population sizes, turbidity, lighting, feeding states, occlusion levels, seasons, and camera positions.
- Validate empirical coverage: nominal 95% intervals must contain the independently established population approximately 95% of the time, including subgroup results by environmental condition.
- Define out-of-distribution conditions under which the system refuses to estimate rather than emits a wider but meaningless interval.
- Derive the physical-count trigger from decision loss and measured calibration, not an arbitrary percentage.
- Specify how physical counts are performed, their own error rate, and how disagreements are adjudicated.
- Test missed mortality events and false trend alarms, not merely whether an interval field exists.

Until those elements exist, the correct output is "measurement unavailable under current conditions," not a confidence interval carrying counterfeit authority.
