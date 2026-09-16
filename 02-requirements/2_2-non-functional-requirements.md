# Non functional requirements

Each NFR names the characteristic it serves, a target with a number, and the
fitness function that checks it. Where a number is an estimate rather than a
given, the basis is stated. Inventing precise-sounding numbers without showing
the arithmetic would make this document look more rigorous than it is.

Load figures derive from
[A2](../01-problem/1_3-assumptions-and-constraints.md): 5,000 visitors per day
today, 15,000 at the three year target. We size for the target, not for today.

## Availability

| ID | Requirement | Characteristic | Target | Verified by |
|---|---|---|---|---|
| NFR-01 | Admission succeeds during opening hours | Availability | 99.95% of attempts | FF-01 |
| NFR-02 | On-site ticket sale and admission continue with all cloud services unreachable. Online sale is the one Tier 0 function that lives in the cloud and does not | Availability, partition tolerance | 100% of on-site Tier 0 functions | FF-02, FF-03 |
| NFR-03 | Planned maintenance occurs outside opening hours | Availability | Zero in-hours planned downtime | Change process |
| NFR-04 | Loss of one Zone Node affects only that zone. The gate zone, which admits for every lane, has a warm standby | Availability | Zero cross-zone impact, zero admission impact from one gate node failing | FF-03 |

## Performance

| ID | Requirement | Characteristic | Target | Verified by |
|---|---|---|---|---|
| NFR-05 | Turnstile validation feels instant to the visitor | Availability | Under 300ms at p99, measured at the gate | FF-01 |
| NFR-06 | A turnstile sustains peak arrival throughput | Availability | 20 admissions per minute per lane | Load test |
| NFR-07 | Voice concierge responds within conversational tolerance | Affordability | Under 1.5s to first audio at p95 | FF-21 |
| NFR-08 | Zone occupancy figures are current | Testability | Under 60s old at p95 | FF-03 |

Basis for NFR-06: at 15,000 visitors per day we assume 40% arrive within a two
hour morning peak, which is 3,000 arrivals per hour. Across twelve lanes that
is roughly 4 per lane per minute sustained. We size to 20 to absorb bursts and
lane closures, which gives a comfortable margin rather than a tight one.

## Resilience and partition tolerance

| ID | Requirement | Characteristic | Target | Verified by |
|---|---|---|---|---|
| NFR-09 | A zone operates independently during a network partition | Partition tolerance | Up to 4 hours with no functional loss in Tier 0 | FF-03 |
| NFR-10 | Buffered telemetry survives a partition without loss | Partition tolerance | 24 hours of local retention per Zone Node | FF-05 |
| NFR-11 | Reconciliation after a partition is correct | Partition tolerance | Zero lost admissions, zero duplicate charges | FF-05 |
| NFR-12 | Every capability has a documented degraded behavior | Partition tolerance | No blank cells in the degraded mode matrix | FF-04 |

## Scalability

| ID | Requirement | Characteristic | Target | Verified by |
|---|---|---|---|---|
| NFR-13 | The platform supports the three year visitor target without redesign | Availability | 15,000 visitors per day | Load test |
| NFR-14 | Adding a zone is a configuration change, not an architectural one | Operability | Under one day of work per zone | Rehearsal |
| NFR-15 | Sensor fleet growth is absorbed without re-architecture | Operability | 3x current device count | Load test |

Basis for NFR-15: roughly 400 devices at launch across 55 enclosures, 40 rides,
counters and environmental sensors, at around 40 messages per second aggregate.
This is a small telemetry load by any modern standard, and we say so rather than
implying the volume is challenging. The difficulty here is connectivity, not
throughput.

## Operability

| ID | Requirement | Characteristic | Target | Verified by |
|---|---|---|---|---|
| NFR-16 | The platform is operable by the permanent team | Operability | 2 to 3 staff, under 6 hours per week | FF-07 |
| NFR-17 | Alert volume stays within human capacity | Operability | Under 20 per week, under 2 out of hours | FF-08 |
| NFR-18 | Distinct systems requiring routine operation stay bounded | Operability | 6 or fewer | FF-06 |
| NFR-19 | Zone Node software updates deploy over intermittent connectivity | Operability | Staged rollout, automatic rollback on failure | Rehearsal |

NFR-19 is easy to overlook and hard to retrofit. Pushing model and software
updates to edge devices across a park with patchy coverage is a genuine
distributed systems problem, and it is the operational cost of choosing edge
inference.

## Security

| ID | Requirement | Characteristic | Target | Verified by |
|---|---|---|---|---|
| NFR-20 | Ticket credentials cannot be forged or replayed | Auditability | Cryptographic signature, single use enforced at the gate | Penetration test |
| NFR-21 | Visitor facing AI resists adversarial input | Testability | Zero policy violations in 200 adversarial attempts | FF-22 |
| NFR-22 | Zone Nodes are individually compromised without lateral movement | Operability | Per-device credentials, no shared secrets | Penetration test |
| NFR-23 | Payment handling stays out of scope for estate systems | Operability | No card data touches estate infrastructure | Design review |

## Privacy and accessibility

| ID | Requirement | Characteristic | Target | Verified by |
|---|---|---|---|---|
| NFR-24 | Consumer digital services meet accessibility standards | Regulatory | EN 301 549 and WCAG 2.2 AA | Accessibility audit |
| NFR-25 | Visitor counting retains no images and identifies no one | Regulatory | Edge processing only, counts leave the device, frames do not | FF-09, DPIA |
| NFR-26 | Personal data is minimized against its stated purpose | Regulatory | Documented purpose and lifecycle per data category | FF-10 |
| NFR-27 | Staff data never reaches an individual level in analytics | Regulatory | Zero identifying fields, asserted at schema level | FF-29 |

## Auditability

| ID | Requirement | Characteristic | Target | Verified by |
|---|---|---|---|---|
| NFR-28 | Regulated records are fully reconstructable | Auditability | Actor, timestamp and evidence for every change, for the full retention period | FF-09 |
| NFR-29 | Fiscal and behavioral data follow independent lifecycles | Auditability | Separate stores, separate retention | FF-10 |
| NFR-30 | AI decisions affecting a regulated record carry their evidence | Auditability | Model version, inputs, confidence, and the human confirmation | FF-30 |

## Cost

| ID | Requirement | Characteristic | Target | Verified by |
|---|---|---|---|---|
| NFR-31 | AI inference stays within the per admission ceiling | Affordability | Under EUR 0.10, guard at EUR 0.08 | FF-11 |
| NFR-32 | Platform operating cost stays within budget | Affordability | Under EUR 495,000 per year today, under EUR 975,000 at target scale | Monthly review |
| NFR-33 | Cost per interaction does not regress silently | Affordability | No increase above 15% without an ADR | FF-12 |

## Evolvability and observability

| ID | Requirement | Characteristic | Target | Verified by |
|---|---|---|---|---|
| NFR-34 | A model provider can be substituted per capability | Evolvability | Under 2 days, excluding re-embedding | FF-13 |
| NFR-35 | Provider specific code exists in exactly one place | Evolvability | Zero SDK imports outside the model gateway | FF-14 |
| NFR-36 | Every AI capability can be disabled independently | Evolvability | Feature flag per capability, no Tier 0 impact | FF-02 |
| NFR-37 | Model behavior in production is observable | Testability | Input and output sampling, drift metrics, cost per capability | FF-31, FF-32 |

## The number we are least confident about

NFR-34 sets provider substitution at under two days. We have not rehearsed it,
because there is nothing built to rehearse against. It is an intent expressed
as a target, and FF-13 exists to turn it into a measurement once there is a
system. We would rather write it as a testable claim we might fail than as a
comfortable statement about loose coupling.
