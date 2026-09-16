# Glossary

*arc42 section 12. Terms we invented, terms we borrowed, and terms that mean
something specific here.*

## Our vocabulary

| Term | Meaning |
|---|---|
| **Zone** | A named area of the estate. The unit of connectivity, authority, state, analytics, staffing and AI deployment |
| **Zone Node** | Edge compute in a zone: MQTT broker, local inference, local store, sync agent, zone ops view. The gate zone's node also runs the admission service for every lane, and is the one node with a standby. Owns what happens in its zone |
| **Deterministic floor** | Capabilities in which no model output is permitted: ticketing, admission, payment, fiscal records, the animal register. Tier 0 |
| **Tier** | Criticality classification for an AI capability, 0 to 3. Decides what it may do, what it falls back to, and how hard its assurance must be. See [2_3](02-requirements/2_3-architecture-characteristics.md) |
| **Model gateway** | The single component through which every model call passes. Routing, caching, budget accounting, logging, provider abstraction |
| **Heuristic baseline** | The rule-based implementation of a capability. Ships first, and is never deleted. Both the cold start answer and the permanent fallback |
| **Budget guard** | Runtime control that degrades Tier 2 capabilities before AI spend per scanned admission reaches the ceiling |
| **Assurance plane** | Evaluation runs, drift detection, output sampling and the budget guard, treated as architecture rather than as process |
| **Golden dataset** | Curated evaluation data with expected outcomes and an acceptance threshold, per capability |
| **Override rate** | Proportion of Tier 1 recommendations a human rejects. Our primary signal for whether a capability is earning its place |

## Borrowed from real-time and multiplayer systems

| Term | Meaning here |
|---|---|
| **Area of interest** | A visitor device receives state only for nearby rides and enclosures, which cuts bandwidth on a patchy network |
| **Zone authority** | The zone, not the cloud, is the source of truth for what happens inside it |
| **Store and forward** | Data is written locally and forwarded opportunistically. The writer never waits for the reader |

## German regulatory terms

| Term | Meaning |
|---|---|
| **BetrVG** | Betriebsverfassungsgesetz, the works constitution act. Section 87(1)(6) governs staff monitoring |
| **Betriebsrat** | Works council. Holds co-determination rights, effectively a veto on staff monitoring |
| **BNatSchG** | Bundesnaturschutzgesetz, federal nature conservation act. Section 42 covers zoo authorization and records |
| **TierSchG / TierGesG** | Animal welfare act and animal health act |
| **BayDSchG** | Bavarian heritage protection act. Why sensing on the rides is non-invasive |
| **BayLDA** | Bavarian data protection supervisory authority for private bodies |
| **KassenSichV / TSE** | Cash register security ordinance, and the certified technical security device every electronic point of sale requires |
| **GoBD** | German principles for the retention of books and records. Source of the ten year fiscal retention |
| **BFSG** | German implementation of the European Accessibility Act |
| **Veterinäramt** | Local veterinary authority. Recipient of notifiable disease reports |
| **TÜV / ZÜS** | Technical inspection bodies. They inspect the rides, our models do not |

## Estate specific

| Term | Meaning |
|---|---|
| **Jumping piranha** | The collection the brief asks us to count. Aquatic, mobile, and in water that is not always clear, which is why we report an interval rather than a number |
| **Family pass** | A ticket product covering a defined group. Non trivial: group composition, transferability, guardian consent and split VAT treatment all attach to it |
| **The carnivorous plant collection** | Not a revenue asset. The stake. Sold if the estate misses its growth target |

## Terms we avoid

**"AI-powered".** It describes a supplier, not a behavior. Every capability here
states its tier, its fallback and its verification instead.

**"Human in the loop", unqualified.** It usually means a person can theoretically
see the output. We state where the human sits, what they see, and what their
override rate is. See [5_4](05-ai-assurance/5_4-human-in-the-loop.md).

**"Real time".** Everything here has a number instead. Turnstile validation
under 300ms at p99, occupancy under 60 seconds stale at p95.
