# Failure mode taxonomy

*What each AI capability does when it goes wrong, how we detect it, how fast,
and what happens automatically.*

Most architecture submissions say "we monitor accuracy". That is not a failure
analysis, it is an intention. This page names the actual failure modes per
capability and what the system does about each one without a human present.

Read the columns as a chain. A failure mode with no detection is invisible. A
detection with no automatic response is a notification. Only the last column is
architecture.

## Voice concierge, Tier 2

| Failure mode | What it looks like | Detection | Latency | Automatic response |
|---|---|---|---|---|
| Hallucination on fact | Confident, fluent, wrong answer about opening times, prices, animal facts | Golden set (FF-21), production sampling (FF-32) | Per release, weekly in production | Below threshold blocks release. In production, capability reverts to curated content |
| Hallucination on safety | Wrong answer about whether an animal is dangerous | Routing recall on the safety golden set and its paraphrases (FF-36), output filter on generated answers in production | Per release, real time | Two independent signals, the classifier and a lexical net, route the class to curated content. The output filter replaces any generated answer that mentions a safety term. A miss found in production reverts open ended generation to curated content pending fix |
| Prompt injection | Visitor coerces off-policy output | Adversarial suite (FF-22), input classifier in production | Per release, real time | Refusal. Attempt logged and added to the corpus |
| Speech recognition error compounding | Correct model, wrong transcript, wrong answer | Error injection testing at 10 percent word error rate (FF-23) | Weekly | Confirmation prompt on low ASR confidence before acting |
| Language degradation | Quality drops in a language with fewer reference passages | Per language scoring | Per release | Language disabled rather than served badly |
| Latency or cost spike | Provider slow or expensive | Gateway metrics, budget guard (FF-11) | Hourly | Route to smaller model, then to local concierge, then to static content |

## Animal welfare, aquatic and terrestrial, Tier 1

| Failure mode | What it looks like | Detection | Latency | Automatic response |
|---|---|---|---|---|
| **False negative** | Animal is ill, no alert raised | Withheld historical incidents (FF-24, FF-25), keeper observation | Weekly | Threshold lowered. We accept more false positives by design |
| False positive storm | Dozens of alerts, none real | Alert volume budget (FF-08), override rate (FF-30) | Daily | Alerts throttled to the ops console, not suppressed. Model review triggered |
| Sensor failure masquerading as animal health | Flat or absent readings read as normal | Sensor liveness check, independent of the model | Under 15 minutes | Enclosure reverts to schedule based physical inspection |
| Species model mismatch | A model tuned on one species applied to another | Per species accuracy breakdown (FF-25) | Weekly | Species falls back to threshold rules |
| Drift after enclosure change | New lighting, new furniture, model confused | Input drift (FF-31) | Daily | Shadow evaluation, revert to baseline if below threshold |
| Keeper stops trusting alerts | Silent. Alerts acknowledged and ignored | **Override rate** (FF-30) | Monthly | Above 20 percent triggers model review, not a compliance reminder |

The last row is the failure mode that kills welfare systems in practice, and it
produces no error, no exception, and no alert of its own. Measuring override
rate is the only way to see it.

## Piranha population, Tier 1

| Failure mode | What it looks like | Detection | Latency | Automatic response |
|---|---|---|---|---|
| Overconfident point estimate | A specific number that the evidence does not support | Structural. FF-26 fails the build if any output lacks an interval | Per commit | Cannot ship |
| Interval quietly widening | Turbidity or lighting degrades precision, nobody notices | Interval width monitor (FF-27) | Daily | Physical verification triggered when width exceeds 15 percent |
| Systematic undercount | Fish obscured consistently, trend looks stable | Calibration against periodic physical counts | Per calibration | Bias correction, or the capability is withdrawn |
| Escape or predation event read as noise | Real population drop dismissed as variance | Trend alerting rather than absolute value | Daily | Alert on trend break regardless of interval width |

## Footfall and staff deployment, Tier 1

| Failure mode | What it looks like | Detection | Latency | Automatic response |
|---|---|---|---|---|
| Counting bias by conditions | Enclosure lighting or weather skews counts systematically | Per zone calibration against manual counts | Monthly | Zone specific correction, or zone excluded from comparison |
| Individual staff data leaks into analytics | A schema change introduces an identifier | Schema assertion (FF-29) | Per commit and per run | **Build fails.** This is a legal commitment, not a preference |
| Advice that violates working time rules | Deployment suggestion breaches rest periods | Rule check outside the model | Per run | Suggestion suppressed. Rules are not the model's job |
| Over-trusted advice | Managers follow suggestions without judgment | Override rate, deliberately expected to be non-zero | Monthly | An override rate near zero is investigated, not celebrated |

That last row is deliberate. For an advisory capability, total compliance means
the human is not really in the loop, and the human-in-the-loop is the entire
legal basis for the capability under the AI Act and BetrVG.

## Demand forecasting, Tier 3

| Failure mode | What it looks like | Detection | Latency | Automatic response |
|---|---|---|---|---|
| Model worse than the heuristic | Sophisticated model, worse answers | Continuous comparison (FF-28) | Weekly | Revert to baseline. The baseline is never deleted |
| Weather feed failure | Forecast silently loses its strongest signal | Feed liveness | Hourly | Fall back to seasonal averages, flag reduced confidence |
| Regime change | A new attraction or a pandemic invalidates history | Drift (FF-31), forecast error spike | Daily | Revert to baseline, rebuild the training window |

## Cross-capability failure modes

| Failure mode | Detection | Automatic response |
|---|---|---|
| Model provider outage | Gateway error rate | Every capability to its baseline. Tier 0 unaffected |
| Provider silently changes a model behind a stable name | Golden set scores shift with no deployment on our side | Capability pinned to last known good, alert raised |
| Cost ceiling approached | Rolling spend per scanned admission (FF-11) | Unprotected Tier 2 degrades in defined order before the ceiling breaks. Accessibility holds its reserved floor |
| Evaluation harness itself breaks | Harness self-test in CI | Build fails. A green build with a broken evaluator is the worst state to be in |

## The pattern

Read down the automatic response column and the same three answers recur:
revert to baseline, fall back to curated content, or fail the build. That is
intentional. Three well understood responses applied consistently are worth more
than a bespoke recovery path per capability that nobody can hold in their head,
particularly for a team of two to three people who will be woken up by these
systems at three in the morning.
