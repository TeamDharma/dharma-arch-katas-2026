# Reference technology choices

*What we would actually install, at kata fidelity. Every row is a reference
choice: the class of thing is the decision, the named product is a defensible
instance of it, and the last column says what a substitute would cost.*

A kata is about structure rather than products, but a structure with no named
instance leaves a reader unable to judge whether it is buildable and runnable
by three people. This page exists to answer that. Nothing here is a claim that
the named product is the best one.

## On the Zone Node

| Concern | Reference choice | Why | If substituted |
|---|---|---|---|
| Hardware | Small form factor ARM or x86 box with an inference accelerator, NVIDIA Jetson Orin class or an x86 board with a Hailo module, in a weatherproof enclosure | Runs a detector at the frame rate counting needs, under 60 W, mains with battery backup | Any box that runs containers and ONNX. Hardware is the easiest swap on this page |
| MQTT broker | Eclipse Mosquitto, MQTT 5, one instance per node | Small, mature, per topic QoS, runs on anything. Eleven instances of one image is one system under FF-06, not eleven | EMQX or HiveMQ Edge if a node ever needs clustering, which we do not expect |
| Edge runtime | Containers under a lightweight orchestrator, models exported to ONNX and run through ONNX Runtime with the accelerator's execution provider | One artefact format for every edge model, so the staged rollout in NFR-19 is one mechanism | TensorRT engines for one accelerator, at the cost of a second artefact format |
| Counting model | A YOLO class detector with a line crossing counter, fine tuned in phase 1 on the estate's own gate geometry | Runs at the edge, discards frames in the same cycle, and is the shape of model every vision team already knows | Any detector with equivalent recall at zone boundaries. The monthly manual calibration protects the count, not the model choice |
| Local store | SQLite in WAL mode, with the 24 hour buffer as a rolling table | Zero operational surface. There is no database to administer on a box in a park | Embedded PostgreSQL if a node ever needs concurrent writers, which this design does not |
| Sync agent | Ours, small. HTTPS, resumable batches keyed on record id, acknowledgements from the backbone | The idempotent, resumable and bounded properties in [3_5](3_5-connectivity-and-edge.md) are the whole component | A managed edge connector from the cloud provider, if it can resume from the last acknowledged id |
| Speech recognition, local intents | Whisper class model, small variant, on the accelerator | The twenty common questions do not need cloud recognition, and local recognition is what keeps the concierge working under C1 | Cloud recognition would put the most used path behind the least reliable link |
| Zone ops view | A web application served from the Zone Node to staff tablets over the staff segment of the zone's local WiFi, separate from the visitor segment | Works during a partition, which is when it is needed most | Native tablet apps would need an app store and a second build pipeline |

## Credentials

| Concern | Reference choice | Why |
|---|---|---|
| Format | CBOR Web Token in a QR code, signed with Ed25519 | Compact enough for a QR, standard, fast to verify on a small box |
| Key hierarchy | Platform root key signs 48 hour delegated keys for each point of sale unit, held in the unit's secure element or TPM. Issuer certificates reach the gate with the revocation list | On-site sales continue through a cloud outage, and a stolen point of sale key is worth two days of one till, [ADR-0004](../07-decisions/ADR-0004-offline-verifiable-ticket-credentials.md) |
| Revocation | Signed list, pulled opportunistically, applied on next presentation | Eventually consistent by decision |

## In the cloud

| Concern | Reference choice | Why | If substituted |
|---|---|---|---|
| Region | One hyperscaler region inside the EU, Frankfurt class | Data residency for the DPIA, one timezone, one estate | Any EU region. Multi region is declined in [2_3](../02-requirements/2_3-architecture-characteristics.md) |
| Application runtime | Managed Kubernetes or the provider's serverless container service, one cluster | The gateway, assurance plane, experience orchestration, forecasting, ops console and register are ordinary services. One managed runtime is one of the six systems | Serverless functions for the forecasting job alone, if the cluster is otherwise idle |
| Event backbone | The provider's managed Kafka compatible service | Ordered, durable, and somebody else patches it | Any managed log. Self hosting fails FF-06 |
| Lakehouse | Object storage with an open table format, Delta or Iceberg, behind the provider's managed query engine | Commodity. The raw to curated flow in [3_11](3_11-data-architecture.md) is two tables and a scheduled job | Any managed warehouse. The separation from the fiscal store matters more than the engine |
| Ticketing, point of sale, fiscal | The bought platform, selected against the two hard criteria in [ADR-0012](../07-decisions/ADR-0012-buy-ticketing-build-the-ai.md) | Procurement, not ours to name here | |
| Animal register | Ours, append only, on the runtime's managed PostgreSQL with point in time recovery. Integration with ZIMS remains open | A statutory record wants a boring database | ZIMS as the record, if its integration surface allows the anti-corruption layer in [3_3](3_3-domain-model.md) |
| Identity for staff | The provider's managed identity service, or a managed Keycloak | Never build authentication. Short lived zone scoped tokens for offline use, [3_7](3_7-identity-and-access.md) | Any OIDC provider |
| Model gateway | Ours, thin. An open source routing library may sit inside it, but the metering, logging and budget guard are ours because they are the argument | Local metering on every call cannot be an afterthought in a bought proxy | |
| Language models | Whichever frontier and small hosted models pass the golden set this quarter, behind the gateway. Small model first, frontier on escalation. No fine tuning | Substitutability is the property, [ADR-0015](../07-decisions/ADR-0015-model-provider-exit-strategy.md). Naming a vendor in a document with a three year horizon is a claim about the wrong year | |
| Translation and speech synthesis | The provider whose output scores best on the 150 reference passages per language, with lock in accepted | Quality is a usability floor here, [2_5](../02-requirements/2_5-quality-scenarios.md) | |
| Observability | The provider's managed metrics and logs, with the gateway's model log as the AI specific source | One place to look, for a team of three | Managed Grafana and Prometheus |
| Evaluation | The harness in [code/](../code/), extended with live invocation behind a flag. Scoring rubrics ours; an open source evaluation library may run them | The checks are the argument, so they stay ours | |

## Backhaul

Undecided, per [ADR-0013](../07-decisions/ADR-0013-connectivity-backhaul.md).
The working assumption for costing is LoRaWAN for battery sensors plus LTE for
Zone Nodes, with fibre where it already exists.

## What this page does not claim

That any of these is the best choice. Each is a defensible instance of a class,
named so that a reader can check that three people could run the result. Where
the class matters and the instance does not, the table says so.
