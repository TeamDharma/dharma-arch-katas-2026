# Quality attribute scenarios

*arc42 section 10. The characteristics in
[2_3](2_3-architecture-characteristics.md) say what we optimize for. This page
says what that means when something actually happens.*

We use the ATAM scenario form: a source produces a stimulus, against an
artifact, in an environment, and the system produces a response that can be
measured. A quality attribute stated without a scenario is an adjective.

The four scenarios we consider most revealing are written out in full. The rest
are tabulated, because repeating six headings fourteen times helps nobody.

---

## QS-01 The cloud link fails during peak admission

| | |
|---|---|
| **Source** | Network provider outage, outside our control |
| **Stimulus** | All connectivity between the estate and the cloud is lost |
| **Artifact** | Zone Nodes, turnstiles, point of sale |
| **Environment** | Saturday morning peak, roughly 3,000 arrivals per hour across twelve lanes |
| **Response** | Turnstiles continue validating pre-purchased tickets against locally held signed credentials and the last synchronized revocation list. On-site sales continue and record fiscally, queued for later submission. Telemetry buffers locally. Tier 1, 2 and 3 AI capabilities fall back to their heuristic baselines or to static content |
| **Measure** | Zero admission failures attributable to the outage. Zero lost sales records. Full reconciliation on reconnect with zero duplicate charges |

This is the scenario the whole architecture is shaped around. If the response
here were anything other than "carries on", the zone model would not be earning
its complexity.

---

## QS-05 The concierge gives a confidently wrong answer on a safety topic

| | |
|---|---|
| **Source** | A visitor asks whether an animal in an enclosure is dangerous |
| **Stimulus** | The model produces a fluent, plausible, incorrect answer |
| **Artifact** | Voice concierge, model gateway, evaluation harness |
| **Environment** | Normal operation, production traffic |
| **Response** | Safety-classified topics are routed to curated content rather than to open generation, by an intent classifier and, independently, by a lexical net over safety terms. Either signal routes. An output filter catches a generated answer that mentions a safety term before it is spoken. The model may read curated content aloud and may translate it. It may not compose an answer. Any such query is sampled at a higher rate for human review |
| **Measure** | Zero confidently wrong responses on safety topics in a golden set of 300, checked on every prompt or model change (FF-21). Routing recall of 100 percent on the safety golden set and its paraphrases, classifier-only misses reported (FF-36). Production sampling of 100 percent of safety-classified turns rather than the usual weekly 50 |

Note that the response is a routing constraint rather than a better prompt,
and the router is itself measured, because a classifier is a model and a miss
there is exactly the failure the constraint exists to prevent. We do not
believe a prompt can be made reliable enough for a question
whose wrong answer puts a child near a venomous animal, so that class of
question is removed from the model's reach.

---

## QS-10 The works council challenges the staff analytics

| | |
|---|---|
| **Source** | Works council, exercising co-determination rights |
| **Stimulus** | A formal question about whether the system can monitor individual staff performance |
| **Artifact** | Footfall analytics, staff deployment service, data schemas |
| **Environment** | Any time after deployment, potentially years later |
| **Response** | We demonstrate that no individual staff identifier exists in any analytics schema, that the assertion is enforced on every commit and every run, and that the build fails if it is violated |
| **Measure** | Evidence produced within one working day, drawn from FF-29 run history rather than from assurances |

The measure is the interesting part. Answering this question with a design
document would not satisfy anybody. Answering it with a failing build is a
different kind of answer.

---

## QS-12 A model provider raises prices mid-contract

| | |
|---|---|
| **Source** | Model provider commercial decision |
| **Stimulus** | Per-token pricing for the capability we use most increases sharply |
| **Artifact** | Model gateway, budget guard, affected capabilities |
| **Environment** | Production, at or near the 15,000 visitor target |
| **Response** | The budget guard observes cost per scanned admission crossing EUR 0.08 and begins degrading Tier 2 capabilities in a defined order before the ceiling is reached. In parallel, the gateway allows routing that capability to an alternative provider without changes outside the gateway |
| **Measure** | Degradation begins automatically within one hour of the cost signal. Provider substitution completed within two days, excluding re-embedding (FF-13) |

---

## The remaining scenarios

| ID | Stimulus | Environment | Response | Measure |
|---|---|---|---|---|
| QS-02 | A single zone is partitioned for four hours | Normal operating day | Zone continues Tier 0 unaffected; telemetry buffers; reconciliation on reconnect | Zero lost admissions, zero duplicate charges, 24h local buffer sufficient (FF-05, NFR-10) |
| QS-03 | Model provider suffers a total outage | Peak day | Every AI capability falls to its heuristic baseline. Tier 0 unaffected | Zero impact on admission or sales. Visitor-facing features signpost a human |
| QS-04 | A model we depend on is deprecated with 30 days notice | Any | Substitute inside the gateway; re-evaluate against the golden set before switching | Substitution and re-evaluation within the notice period, no capability shipped below threshold |
| QS-06 | A visitor attempts prompt injection on the concierge | Production, public | Input filtering, scope constraint, and refusal. Attempt logged and added to the adversarial corpus | Zero policy violations in 200 adversarial attempts per release (FF-22) |
| QS-07 | An animal is becoming ill but indicators stay inside thresholds | Continuous monitoring | Trend detection alongside threshold breach; keeper's own observation always overrides | False negative rate under 2 percent on withheld historical incidents (FF-24, FF-25) |
| QS-08 | Water turbidity rises and the piranha estimate loses precision | Aquatic house, seasonal | Interval widens, and when it exceeds 15 percent of the estimate a physical verification is triggered | 100 percent of outputs carry an interval (FF-26); verification triggered, never suppressed (FF-27) |
| QS-09 | Unforecast weather change produces a demand spike | Same day | Zone occupancy signals update within 60 seconds; staff deployment advice re-issued | Occupancy under 60s stale at p95 (NFR-08). Forecast miss recorded against model accuracy |
| QS-11 | An alert storm begins at 2am | Two to three person operations team, asleep | Alert routing suppresses non-Tier-0 alerts outside hours. Anything not requiring action before opening waits | Under 2 out-of-hours alerts per week (FF-08). An ignored alert counts as a failure, not as noise |
| QS-13 | A regulator audits the animal register | Announced or unannounced | Full reconstruction of any record, including which AI output informed it and which human confirmed it | 100 percent reconstructable for the full retention period (FF-09, NFR-30) |
| QS-14 | Input distributions drift six months after launch | Production | Drift detection alerts, shadow evaluation runs, capability reverts to baseline if it fails threshold | Population stability index under 0.2 (FF-31). Reversion is automatic, not a decision |

---

## Sensitivity points

Places where a small change moves a quality attribute a lot. These deserve
disproportionate design attention and disproportionate testing.

**The model gateway.** Evolvability, affordability and testability all pass
through it. It is the single most valuable component to get right and the
single worst one to bypass, which is why FF-14 forbids importing a provider SDK
anywhere else.

**The Zone Node.** Availability and partition tolerance both depend on it
holding local authority. Weakening that, for example by making admission
consult the cloud for a "quick check", silently converts the whole architecture
back into a connected one.

**The heuristic baseline.** It is the cold start answer and the permanent
fallback. Deleting it once models work, which will feel reasonable in year two,
removes the safety net from every AI capability at once.

## Tradeoff points

Places where improving one attribute demonstrably costs another. We took a
position on each rather than pretending there was no cost.

| Tradeoff | What we gave up | Why |
|---|---|---|
| Inference at the edge | Operability. Model rollout across patchy connectivity is genuinely hard (NFR-19) | Partition tolerance and affordability both improve, and they rank higher |
| Over-alerting on animal welfare | Precision, and veterinary time | A false negative costs an animal. The errors are not symmetric and we tuned accordingly |
| Provider lock-in for accessibility and translation | Evolvability | Output quality here affects whether a disabled visitor can use the estate at all. We accepted the lock-in and recorded it |
| Tables rather than a sentence template for requirements | Some precision | Density, because judges read many submissions. We compensated by checking unambiguity hardest |
| No visitor accounts | Personalization depth | Creating a personal data obligation the Countess never asked for, in order to deliver a feature she never asked for, is a poor trade |

## Risks

| Risk | Related scenario | Mitigation |
|---|---|---|
| Connectivity backhaul choice is still open, and it drives cost and partition behavior | QS-01, QS-02 | Logged in OPEN-QUESTIONS. The architecture is deliberately indifferent to which option wins |
| No historical data means every model launches unvalidated in the real environment | QS-07, QS-09, QS-14 | Heuristic baseline runs first and stays; models must beat it by a margin before taking over |
| Two to three person operations team is a single point of human failure | QS-11 | Managed services over self-hosted, alert budget enforced, six hour weekly ceiling |
| Dangerous animal rules vary by Land and we have not confirmed Bavaria's | QS-13 | Logged as an open question rather than assumed |

## Non-risks

Worth recording, because ATAM treats an examined and dismissed concern as an
output rather than an omission.

**Elastic scale.** Load is predictable within a day and a season. Provisioning
against a known peak is cheaper and simpler than building for elasticity.

**Telemetry volume.** Around 400 devices at roughly 40 messages per second is a
small load. The difficulty at the edge is connectivity, not throughput, and we
should not dress the latter up as the former.

**Regional failover.** One estate, one location. A failover story would cost
operability, which we ranked third.
