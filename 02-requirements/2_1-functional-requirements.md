# Functional requirements

## How to read this table

Three columns carry the argument.

**Source** says where the requirement came from. *Brief* means the Countess
asked for it. *Derived* means we concluded the system needs it in order to
deliver something she asked for. *Regulatory* means the law requires it whether
anyone asked or not. Separating these matters, because a reader should be able
to see which parts of the scope we were given and which parts we added, and
challenge the second set.

**Tier** is the AI criticality tier from
[2_3-architecture-characteristics.md](2_3-architecture-characteristics.md).
Tier 0 means no model output is permitted in that path.

**Verified by** names the fitness function or test that proves it works. Every
requirement has one. A requirement nobody can check is a wish.

**Phase** is the delivery phase from
[1_3](../01-problem/1_3-assumptions-and-constraints.md), and it is how we
prioritize. We chose phase over a MoSCoW scale because "must" is a word
everybody applies to their own requirement, whereas a phase forces a real
ordering against a real calendar. Everything in Phase 0 ships before anything
in Phase 1.

## How these requirements were obtained

Worth stating plainly, because it bounds how much confidence they deserve.

We had one written source, the organizers' brief, and one opportunity to ask a
question of the client, during the live session, which we spent establishing
that the system is greenfield. Everything else is document analysis and
inference.

That is a thin elicitation base by any standard, and it is the reason
[1_3](../01-problem/1_3-assumptions-and-constraints.md) is unusually long. When
you cannot ask, you assume, and the honest response is to make the assumptions
visible and falsifiable rather than to present inferences as though they were
requirements.

## The quality criteria we applied

We checked every requirement against six criteria before it went in the table.

| Criterion | How we checked it |
|---|---|
| **Atomic** | One requirement per row. No row contains the word "and" joining two testable things |
| **Verifiable** | Every row names a fitness function or a test. A row with no verification method was rewritten or deleted |
| **Traceable** | Every row names its source, and every row links forward to a check |
| **Necessary** | Derived requirements must trace to something in the brief or to a regulatory obligation. We removed several that only traced to our own enthusiasm |
| **Prioritized** | Every row carries a phase |
| **Unambiguous** | Numbers rather than adjectives. "Under 300ms at p99" rather than "responsive" |

We did not apply a full sentence template such as the Rupp form. Tables are
denser, and density matters when judges are reading many submissions under time
pressure. The tradeoff is that a table tempts you into terse rows that hide
ambiguity, so unambiguity is the criterion we checked hardest.

## FR-1xx Ticketing and admission

| ID | Requirement | Source | Tier | Verified by | Phase |
|---|---|---|---|---|---|
| FR-101 | Visitors can buy tickets online before arrival and on site on the day | Brief | 0 | FF-02 | 0 |
| FR-102 | Family passes cover a defined group, with a stated policy on group composition and transferability | Brief | 0 | FF-02 | 0 |
| FR-103 | Season passes and repeat visit products exist as a distinct product type | Derived | 0 | FF-02 | 1 |
| FR-104 | A turnstile can validate a ticket with no network connection available | Derived | 0 | FF-01, FF-03 | 0 |
| FR-105 | Revoked or already used tickets are rejected once revocation data reaches the zone | Derived | 0 | FF-05 | 0 |
| FR-106 | Every sale produces a fiscally compliant record and receipt | Regulatory | 0 | FF-09, FF-10 | 0 |
| FR-107 | Combined tickets apportion revenue correctly across differing tax treatments | Regulatory | 0 | FF-09 | 0 |
| FR-108 | Ticket purchase meets accessibility requirements for consumer digital services | Regulatory | 0 | Accessibility audit, see NFR-24 | 0 |
| FR-109 | Guardians can consent on behalf of minors where the applicable age of consent requires it | Regulatory | 0 | FF-09 | 0 |

## FR-2xx Visitor experience

| ID | Requirement | Source | Tier | Verified by | Phase |
|---|---|---|---|---|---|
| FR-201 | Visitors can ask questions by voice and receive spoken answers about wayfinding, opening times, queues, facilities and animals | Derived | 2 | FF-21, FF-23 | 2 |
| FR-202 | The concierge declines confidently outside its scope rather than guessing | Derived | 2 | FF-21, FF-22 | 2 |
| FR-203 | The concierge discloses that it is an AI system | Regulatory | 2 | FF-21 | 2 |
| FR-204 | Content is available in multiple languages covering the estate's main visitor nationalities | Derived | 2 | FF-21 | 2 |
| FR-205 | Audio description and simplified language options exist for visitors who need them | Regulatory, Derived | 2 | Accessibility audit | 2 |
| FR-206 | Live queue and capacity information is available per zone | Derived | 3 | FF-03 | 1 |
| FR-207 | Visitors receive itinerary suggestions based on current conditions and their stated interests | Derived | 2 | FF-21 | 2 |
| FR-208 | All visitor facing capabilities degrade to static signposted content when unavailable | Derived | 0 fallback | FF-03, FF-22 | 0 |
| FR-209 | Nothing in the visitor experience requires installing an app | Derived | 2 | Manual acceptance test | 0 |

## FR-3xx Footfall and operations

| ID | Requirement | Source | Tier | Verified by | Phase |
|---|---|---|---|---|---|
| FR-301 | The estate can see how popular each zone, ride and enclosure is, over time | Brief | 3 | FF-03 | 1 |
| FR-302 | Counting is anonymous, performed at the edge, with no image retention and no biometric identification | Regulatory | 1 | FF-09, DPIA | 1 |
| FR-303 | Staff deployment recommendations are produced per zone as aggregate demand signals | Brief | 1 | FF-29 | 2 |
| FR-304 | Staff deployment output contains no individual level staff data of any kind | Regulatory | 1 | FF-29 | 2 |
| FR-305 | A human assigns staff. The system never assigns | Regulatory | 1 | FF-30 | 2 |
| FR-306 | Zone level demand forecasts are produced for the coming days | Derived | 3 | FF-28 | 2 |
| FR-307 | Forecasts incorporate weather and regional school holiday calendars | Derived | 3 | FF-28 | 2 |

## FR-4xx Animal welfare

| ID | Requirement | Source | Tier | Verified by | Phase |
|---|---|---|---|---|---|
| FR-401 | Animal health indicators are monitored continuously per enclosure | Brief | 1 | FF-24, FF-25 | 1 |
| FR-402 | Feeding quantity and feeding behavior are recorded and monitored | Brief | 1 | FF-24, FF-25 | 1 |
| FR-403 | Aquatic enclosures monitor water quality continuously against per species thresholds | Derived | 1 | FF-24 | 1 |
| FR-404 | Terrestrial enclosures monitor activity and environmental conditions appropriate to the species | Derived | 1 | FF-25 | 1 |
| FR-405 | Population level of the jumping piranha collection is estimated, reported with a confidence interval, and alerted on trend | Brief | 1 | FF-26, FF-27 | 2 |
| FR-406 | Welfare alerts are advisory. A keeper or veterinarian confirms before any record changes | Regulatory | 1 | FF-30 | 1 |
| FR-407 | The animal register is maintained as the statutory record of the collection | Regulatory | 0 | FF-09 | 0 |
| FR-408 | Provenance and movement documentation is held per animal for regulated species | Regulatory | 0 | FF-09 | 0 |
| FR-409 | Suspected notifiable disease follows a defined path to human veterinary confirmation and onward reporting | Regulatory | 1 | FF-30 | 1 |
| FR-410 | Welfare monitoring continues during a network partition and reconciles afterward | Derived | 1 | FF-03, FF-05 | 1 |

## FR-5xx Rides, maintenance and safety

| ID | Requirement | Source | Tier | Verified by | Phase |
|---|---|---|---|---|---|
| FR-501 | Ride telemetry is captured without invasive attachment to protected structures | Regulatory | 1 | Installation review | 1 |
| FR-502 | Maintenance is prioritized using condition data alongside the scheduled regime | Derived | 1 | FF-30 | 2 |
| FR-503 | Predictive output never substitutes for a statutory inspection | Regulatory | 1 | FF-09 | 0 |
| FR-504 | Incident scenarios have defined system behavior, including animal escape, medical emergency and separated child | Derived | 0 | Tabletop exercise | 0 |

## FR-6xx Growth and profitability

| ID | Requirement | Source | Tier | Verified by | Phase |
|---|---|---|---|---|---|
| FR-601 | Revenue is attributable per zone and per product | Derived | 3 | FF-09 | 1 |
| FR-602 | AI inference spend is measured per scanned admission and enforced against a ceiling | Derived | 0 | FF-11, FF-12 | 2 |
| FR-603 | Repeat purchase rate is measurable at cohort level, computed inside the ticketing platform on a hashed purchaser identifier, with only aggregates leaving it | Derived | 3 | FF-10, DPIA | 2 |
| FR-604 | Marketing contact honors opt in requirements | Regulatory | 0 | FF-09 | 0 |

## FR-7xx Platform and records

| ID | Requirement | Source | Tier | Verified by | Phase |
|---|---|---|---|---|---|
| FR-701 | Every zone continues operating independently during a partition of up to four hours | Derived | 0 | FF-03, FF-05 | 0 |
| FR-702 | All model calls pass through a single gateway | Derived | 0 | FF-14 | 2 |
| FR-703 | Model inputs and outputs are logged sufficiently to support evaluation and regulatory obligation | Regulatory, Derived | 0 | FF-20, FF-32 | 2 |
| FR-704 | Fiscal and behavioral data are separated with independent retention lifecycles | Regulatory | 0 | FF-10 | 0 |
| FR-705 | Any AI capability can be disabled independently without affecting Tier 0 | Derived | 0 | FF-02, FF-03 | 2 |

## What the provenance column shows

Forty eight functional requirements, from a brief that names four needs.

| Source | Count |
|---|---|
| Brief | 7 |
| Derived | 23 |
| Regulatory | 16 |
| Both regulatory and derived | 2 |

Seven requirements came directly from what the Countess asked for. The other
forty one are things she did not mention, and a third of the total are legally
mandatory whether anyone asks for them or not.

We are not making a point about the client. Asking for ticketing, popularity
data, animal monitoring and growth is a perfectly good statement of need. The
point is about the gap between a statement of need and a scope, because that
gap is where most of the cost and nearly all of the risk lives. An architecture
proposal that returns only the seven has not finished reading the problem.

It also explains why we spent the first day of a sixteen day kata on the
regulatory register rather than on diagrams. Sixteen requirements we would
otherwise have missed came out of that work, including the constraint that
keeps the staff deployment feature legal.
