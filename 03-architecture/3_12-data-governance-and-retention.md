# Data governance and retention

*Every category of data has a stated purpose, a lifecycle, and something that
checks it.*

## Retention schedule

| Category | Retained | Then | Why that period |
|---|---|---|---|
| Fiscal records | **10 years** | Archived, immutable | GoBD and AO |
| Animal register entries | Per licensing regime, indefinite in practice | Retained | BNatSchG record keeping |
| Animal provenance and CITES documents | Life of the animal plus statutory period | Retained | Wildlife trade regulation |
| Admission records | 90 days | Aggregated, raw deleted | Operational only. Fiscal record is separate and already retained |
| Keyed hash of the purchaser email, inside the ticketing platform, key held by the vendor | 24 months | Deleted, cohort aggregates retained | Repeat purchase measurement, FR-603. Legitimate interest with a documented balancing test, in the DPIA and the privacy notice. Cohorts under fifty suppressed. Never joined to estate data |
| Camera frames | **Never stored** | n/a | Destroyed on the Zone Node in the same processing cycle |
| Zone counts | 90 days raw, then aggregated | Aggregates retained | Trend analysis needs the aggregate, not the event |
| Sensor telemetry | 90 days full resolution | Downsampled | Welfare trend analysis needs months, not every reading |
| Model logs, inputs and outputs | 90 days | Aggregated, raw deleted | Evaluation and incident investigation |
| Speech audio | **Never stored** | n/a | Transcript only where a query escalates, and that follows model log retention |
| Staff records in analytics | **Never created** | n/a | FF-29 fails the build if a staff identifier appears |
| Works agreement and DPIA documentation | Life of the system | Retained | Evidence of lawful basis |

## Four rows that are structural rather than policy

Camera frames, speech audio, staff identifiers and the absence of a visitor
master record are not retention settings. They are properties of the
architecture.

Frames are destroyed at the edge before anything else sees them. A staff
identifier cannot enter analytics because the build fails. There is no visitor
record to retain because the domain model has no such aggregate.

A retention policy can be changed by someone with database access and good
intentions. These cannot, without changing the system, which is exactly the
durability we wanted for the decisions that matter most.

## Purpose limitation

Each category has one stated purpose, and use outside it requires a decision at
ADR level rather than a query.

| Data | Purpose | What it may not be used for |
|---|---|---|
| Zone counts | Investment and staffing decisions | Anything at individual level, which is impossible by construction anyway |
| Welfare telemetry | Animal health | Assessing keeper performance |
| Model logs | Evaluation, cost, audit | Building a profile of any visitor |
| Fiscal records | Tax compliance | Behavioral analysis |
| Keyed purchaser hash | Repeat purchase rate by cohort | Anything at individual level, any join to zone counts, admissions or model logs, any marketing use without the separate UWG opt in |

The second row is worth stating explicitly. Welfare data reveals a great deal
about how carefully individual keepers work, and repurposing it that way would be
staff monitoring by the back door, inside a system that has spent considerable
effort staying out of exactly that.

## Data protection roles

| Role | Who |
|---|---|
| Controller | The estate |
| Processors | Cloud provider, ticketing platform vendor, model providers |
| DPO | Required under BDSG section 38 given the scale of monitoring. The estate must appoint one |
| Supervisory authority | BayLDA |

The DPO line is a delivery item, not an observation. An architecture that
creates an obligation and does not say so hands the Countess a problem she does
not know she has.

## What checks this

| Check | What it does |
|---|---|
| FF-09 | Weekly sample of 20 regulated records, 100 percent must be fully reconstructable |
| FF-10 | Monthly retention conformance. Zero behavioral records past their lifecycle, zero fiscal records deleted early |
| FF-29 | Schema assertion, no staff identifiers, every commit and every run |
| Structural | No frame or audio storage path exists in the edge codebase |

FF-10 checks both directions deliberately. Keeping data too long is the failure
everyone anticipates. Deleting fiscal records early is also a failure, and it is
the one a privacy-minded team is more likely to cause.

## The tension we did not fully resolve

A larger model log corpus would make evaluation better. Minimization says keep
less. We chose 90 days, which is long enough to investigate an incident and
build a quarter's evaluation set, and short enough to defend.

We are not certain it is right. A longer window would improve the assurance
story this submission rests on, and would weaken the privacy position it also
rests on. It is recorded here as a judgment rather than as a derived answer.
