# Evaluation strategy

*arc42 section 8, crosscutting. How we know each AI capability works, and how we
find out when it stops.*

## The claim this section has to support

The README makes one promise: every AI capability in this system has a defined
way to prove it is working, a threshold at which it counts as broken, and
something deterministic to fall back to when it breaks.

That is a testable promise, which is the only kind worth making. This page and
the six that follow are the evidence.

## Why AI needs its own evaluation story

A conventional component is verified by asserting that a known input produces a
known output. Repeat the test, get the same answer. That property is what makes
regression testing meaningful.

Model-backed components break that property in three ways at once. The same
input can produce different outputs between runs. The correct output is often a
range rather than a value, and sometimes a judgment rather than a fact. And the
component can degrade without any code changing, because the world moved or the
provider silently updated something.

So the question shifts from "does this produce the right answer" to "does this
produce acceptable answers at an acceptable rate, and would we notice if that
changed". Every technique below follows from that shift.

## Four layers

Nothing here is exotic. The discipline is in applying all four to every
capability rather than one of them to the capability that worried us most.

### Layer 1: offline evaluation against golden datasets

Every capability has a curated dataset with expected outcomes, an acceptance
threshold, and an automated run in CI. A change to a prompt, a model, a routing
rule, or a retrieval corpus triggers the run. Below threshold, the build fails.

This is enforced structurally: **FF-20 fails the build if any AI capability
lacks a golden dataset, a threshold, and a CI evaluation.** A capability that
cannot be evaluated cannot ship. See
[5_2-golden-datasets.md](5_2-golden-datasets.md) for how we build these with no
historical data.

### Layer 2: adversarial evaluation

Correctness on expected inputs is not the same as safety on hostile ones. The
visitor concierge is a public endpoint at a family attraction, which makes it a
target. We maintain a suite of injection attempts, jailbreaks, and off-topic
coercion, and every real attempt observed in production is added to it.

FF-22 requires zero policy violations in 200 attempts, per release and weekly in
production shadow. See
[../10-security/10_2-ai-specific-threats.md](../10-security/10_2-ai-specific-threats.md).

### Layer 3: shadow and canary in production

Offline evaluation tells you about the inputs you thought of. Production tells
you about the rest.

A new model or prompt runs in shadow first, receiving real traffic and producing
outputs that are scored but never shown to anyone. When shadow results hold
above threshold, it goes to canary on a slice of traffic, then to full rollout.
Any stage can revert automatically.

### Layer 4: continuous monitoring

Once live, three things are watched permanently: input distribution drift
against the training window (FF-31), output sampling by a human (FF-32), and
human override rate on every Tier 1 capability (FF-30).

The override rate is the one people forget. If keepers override 40 percent of
welfare alerts, the model is not helping, whatever its offline accuracy says.
That is why an override rate above 20 percent triggers a model review rather
than a conversation about compliance.

## Evaluation intensity follows the tier

The tier model in
[2_3](../02-requirements/2_3-architecture-characteristics.md) decides how hard
each capability's assurance has to be. Applying Layer 3 shadow deployment to a
weekly forecasting job would be ceremony. Omitting adversarial testing on a
public voice endpoint would be negligence.

| Tier | Offline eval | Adversarial | Shadow and canary | Continuous monitoring |
|---|---|---|---|---|
| **0** Deterministic floor | Conventional tests only. No models present | n/a | n/a | Conventional observability |
| **1** Advisory | Required, with asymmetric error analysis | Where an input is externally influenced | Canary only | Drift, sampling, **override rate** |
| **2** Visitor facing | Required | **Required, every release** | Required, shadow then canary | Drift, sampling, safety topic rate |
| **3** Analytical | Required, backtested | n/a | Not needed, outputs are not live | Drift, accuracy against baseline |

## What we evaluate against when there is no ground truth

Three honest cases, because pretending every capability has a clean label is
where evaluation strategies usually become fiction.

**Where truth exists but is delayed.** Demand forecasting is scored against what
actually happened. The evaluation is real but arrives days later, so the live
guard is drift and the comparison against the heuristic baseline, not accuracy.

**Where truth exists but is expensive.** Piranha population. A physical count is
the ground truth and we cannot do it daily. So we evaluate the model against
occasional physical counts, report intervals rather than values, and trigger a
physical count when the interval gets too wide. The expensive truth is used to
calibrate, not to operate.

**Where truth is a judgment.** Concierge answer quality. Here we use a scored
rubric applied by humans to build the golden set, then automated scoring against
that set, with weekly human sampling to check the automated scorer has not
drifted from the rubric. We do not treat a model scoring another model as
ground truth. It is a cheap approximation of a human judgment, and it is
audited against human judgment on a schedule.

## What would falsify our approach

Worth stating, because a strategy that cannot fail is not a strategy.

If a capability passes its golden set every week for six months, holds no drift,
and still produces a harmful output in production that nobody caught, then our
golden set did not represent the real input distribution and our sampling rate
was too low. The response is not to add a rule for that one case. It is to
re-derive the dataset from production traffic and raise the sampling rate for
that capability's tier.

We expect this to happen at least once. Designing as though it will not is how
assurance becomes paperwork.
