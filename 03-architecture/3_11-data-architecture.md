# Data architecture

*arc42 section 8, crosscutting. Where data lives, why it lives there, and what
it is allowed to be used for.*

## Four categories, deliberately kept apart

The separation is the design. Collapsing these is how you get a system where a
retention rule for tax records deletes a welfare history, or where behavioral
analytics quietly acquires a legal obligation.

| Category | Examples | Store | Retention | Governed by |
|---|---|---|---|---|
| **Statutory records** | Animal register, provenance documents, welfare decisions | Master data store, append only | Per licensing regime | BNatSchG, TierSchG |
| **Fiscal records** | Sales, receipts, TSE records | Separate fiscal store | **10 years**, immutable | GoBD, AO |
| **Operational state** | Zone occupancy, ride condition, current entitlements | Operational stores, zone local and cloud | Short. Days to months | Operational need |
| **Behavioral and analytical** | Counts over time, forecasts, cohorts | Lakehouse | **Minimized.** Aggregated early, raw deleted | GDPR |

## The collision, and how it resolves

GoBD requires ten years of booking records. GDPR requires personal data to be
kept no longer than necessary. Both apply, and they point in opposite
directions.

They are only in conflict if the data is in one place. Separated:

- **Fiscal records** contain what tax law requires: transaction, amount, time,
  tax treatment. They do not contain behavioral data, and they are retained for
  ten years because that is the obligation.
- **Behavioral data** contains what analytics needs: counts, durations, zone
  transitions. It contains no purchase identity, and it is aggregated early and
  the raw records deleted.

The link between them is deliberately weak. We can say that 3,000 tickets were
sold and that the aquatic house saw 4,200 visits. We cannot say which
ticket-holder went where, and we have declined to build the capability that
would let us. Repeat purchase rates arrive from the ticketing platform as
cohort aggregates computed on a hashed purchaser identifier, and the hash never
enters the lakehouse.

That is the cost of the resolution, and it is the same cost
[ADR-0008](../07-decisions/ADR-0008-anonymous-edge-counting.md) already paid.

## Flow

| Stage | Where | What happens |
|---|---|---|
| Capture | Field devices | Sensor reading over MQTT |
| Edge processing | Zone Node | Inference, aggregation. **Frames and raw audio discarded here** |
| Local buffer | Zone Node | 24 hours, survives partition |
| Forward | Sync agent | Store and forward, idempotent, resumable |
| Ingest | Event backbone | Ordered, durable |
| Land | Lakehouse | Raw zone, then curated |
| Serve | Analytics, forecasting, ops console | Curated only |

The irreversible step is edge processing. Frames and audio are destroyed on the
Zone Node and no copy exists anywhere. That is a deliberate one-way door: a
future team cannot decide to start retaining visitor imagery without physically
changing what the edge does, which makes the privacy position durable rather
than a configuration someone can flip.

## Master data

Three sets, each with one owner.

| Master data | Owner | Why it is master |
|---|---|---|
| **Animal register** | Compliance and Records | Statutory. See [3_13](3_13-animal-register.md) |
| **Asset register** | Estate Operations | Rides, Zone Nodes, sensors. Drives maintenance and inspection |
| **Product and entitlement catalogue** | Ticketing and Access | What can be sold, and what it grants |

There is deliberately **no visitor master record**, which is discussed in
[3_3](3_3-domain-model.md) as an absence that expresses a privacy decision in the
domain model.

## Model logs

Every model call is recorded through the gateway: capability, model version,
prompt version, input, output, tokens, cost, latency, evaluation score.

One record serving three purposes, which is why it is worth its storage cost.
It is the evaluation corpus, the cost ledger, and the AI Act audit trail.

Retained 90 days, then aggregated and raw records deleted, except where a record
forms part of a regulated decision trail and follows the register's retention
instead. The tension with wanting a large evaluation corpus is real and is
resolved toward minimization in
[5_3](../05-ai-assurance/5_3-production-monitoring.md).

## What we do not build

**No data warehouse for its own sake.** Everything in the lakehouse serves a
named question in [1_1](../01-problem/1_1-business-goals-and-challenges.md).

**No external data sharing platform.** Interesting in year three. Naming it now
would pull decisions toward a future that may not arrive, and it carries data
protection exposure the estate does not need to take on.

**No customer data platform.** There are no visitor accounts to build one from,
by design.
