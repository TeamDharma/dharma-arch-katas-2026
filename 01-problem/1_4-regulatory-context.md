# Regulatory context

*arc42 section 2. The constraints nobody asked us for.*

The estate is in Bavaria, Germany
([ADR-0001](../07-decisions/ADR-0001-jurisdiction-and-regulatory-baseline.md)).
Sixteen of our forty eight functional requirements come from this page rather
than from the brief.

**How to read this.** Every entry names a regime, the constraint it imposes, and
the architectural consequence. If a regime appears here but shapes nothing, it
is decoration and we removed it. Written at architecture kata fidelity: we are
not offering legal opinions, and items we could not confirm are in
[OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md).

## Data protection

| Regime | Constraint | Consequence |
|---|---|---|
| GDPR, Article 35 | DPIA required for large scale monitoring of public space and for children's data | Visitor counting is anonymous, edge only, retains no frames. FR-302, NFR-25 |
| GDPR, Article 8 (German election: 16) | Children under 16 cannot consent for themselves | Guardian consent in the family pass flow. FR-109 |
| BDSG | Employee data processing, and a designated data protection officer | The estate needs a DPO. Staff analytics constrained. FR-304 |
| TDDDG section 25 | Consent before accessing a terminal device | Any app storage, BLE beacon or cookie needs consent independent of GDPR basis |
| Supervisory authority | BayLDA, for private bodies in Bavaria | One named regulator rather than sixteen |

## Employment and co-determination

| Regime | Constraint | Consequence |
|---|---|---|
| **BetrVG section 87(1)(6)** | Works council co-determination over systems **capable** of monitoring staff performance. Capability is the trigger, not intent | **Aggregate zone signals only, never individual staff data.** FR-303 to FR-305, FF-29. A works agreement is a delivery gate |
| ArbZG | Working time, 11 hour rest periods, daily maxima | Hard feasibility bounds on deployment advice, enforced by rules outside the model |
| AGG | Anti-discrimination | Applies to deployment advice and to any pricing segmentation |

This is the single most design-shaping entry on the page. It is also the one we
would have missed entirely without doing this work, and it would have invalidated
a headline feature after build.

## Animals

| Regime | Constraint | Consequence |
|---|---|---|
| **BNatSchG section 42**, transposing EU Zoos Directive 1999/22/EC | Zoo authorization, statutory up to date records of the collection | **The animal register is a legal record.** AI is advisory, never the system of record. FR-407, Tier 0 |
| TierSchG section 11 | Permit to keep animals for public display, welfare duties | Welfare evidence must be auditable. FR-406 |
| TierGesG | Notifiable disease reporting to the Veterinäramt | Detection routes to a veterinarian who decides. **The system never notifies.** FR-409 |
| BArtSchV, CITES, EU Reg. 338/97 | Marking, registration and provenance for regulated species | Per animal documentary chain. FR-408 |
| Länder rules on dangerous animals | Varies by state, unconfirmed for Bavaria | Logged as an open question rather than assumed |

## Safety, buildings and heritage

| Regime | Constraint | Consequence |
|---|---|---|
| **BayDSchG** | Protected structures cannot be altered without permission | **Non-invasive, battery powered, removable sensing on the rides.** FR-501 |
| BayBO, Fliegende Bauten | Ride approval and acceptance | Inspection cycle our telemetry feeds |
| BetrSichV, DIN EN 13814, inspection by ZÜS or TÜV | Statutory ride inspection | Predictive maintenance advises. It never substitutes. FR-503 |

## Commerce, fiscal and accessibility

| Regime | Constraint | Consequence |
|---|---|---|
| **KassenSichV, AO section 146a** | Certified TSE on every electronic point of sale, plus receipt obligation | Every till needs a TSE, including its **offline** behavior. FR-106 |
| BGB section 312g(2) no. 9 | Withdrawal right exempt for dated leisure events | Dated tickets need no 14 day cancellation flow. Undated passes do |
| UStG section 12 | Reduced rate for zoo admission, standard rate for rides | **A combined family pass must apportion revenue across rates.** FR-107 |
| PAngV | Total price transparency | Bounds how any dynamic pricing may be displayed |
| UWG section 7 | Opt in for electronic marketing | Constrains the returning visitor mechanism. FR-604 |
| **BFSG**, implementing the European Accessibility Act, in force 28 June 2025 | Consumer digital services must be accessible | Online ticketing to EN 301 549 and WCAG 2.2 AA. FR-108, NFR-24 |
| GoBD, Abgabenordnung | Ten year retention of booking records | **Direct conflict with GDPR minimization.** Resolved by separating fiscal from behavioral data. FR-704, NFR-29 |
| ZAG, PSD2 | Strong customer authentication | Card data never touches estate infrastructure. NFR-23 |

## AI

| Regime | Constraint | Consequence |
|---|---|---|
| EU AI Act, Article 5 | Emotion recognition in the workplace prohibited; remote biometric identification restricted | Entire feature categories excluded. No sentiment inference on staff |
| EU AI Act, Annex III | Employment task allocation on individual behaviour is high risk | Staff deployment designed to stay out of scope. See [5_7](../05-ai-assurance/5_7-ai-act-obligations.md) |
| EU AI Act, Article 50 | Transparency, users must be told they are interacting with AI | Disclosure per concierge session. FR-203 |
| EU AI Act, Article 4 | AI literacy obligation on the deployer | Staff training is a roadmap delivery item |
| EU Data Act, from 12 Sep 2025 | Access rights over connected product data | Useful against vendor lock in on the MQTT estate |

## Explicitly out of scope

**NIS2.** An amusement park is not an essential or important entity under the
directive. We scoped it out deliberately rather than leaving it unaddressed,
because a silent omission and a considered exclusion look identical in a
document and are completely different in an architecture.

## The five that actually shape the design

If you read nothing else here, these five changed decisions:

1. **BetrVG section 87(1)(6)** killed individual staff tracking and reshaped
   footfall analytics
2. **EU AI Act Annex III** kept staff deployment advisory rather than decisional
3. **BNatSchG section 42 and TierGesG** made animal monitoring a compliance
   record with a human in the loop
4. **KassenSichV** put a surprising hard constraint on point of sale and its
   offline mode
5. **BayDSchG** forced non-invasive sensing on protected structures

## A note on children and cameras

Counting visitors with cameras in a family attraction means processing images of
children. That is a DPIA trigger and a genuine constraint on the obvious design.

We resolved it toward anonymous counting at the edge with no frame retention and
no identification of anyone. That decision costs us capability. It means we
cannot offer the separated child feature that a tracking system would enable,
which is a real operational need at a family attraction. The tradeoff is
recorded in [2_5](../02-requirements/2_5-quality-scenarios.md) and the
question it leaves open is in [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md).
