# Deployment view

*arc42 section 7. What runs where, and what that costs to operate.*

## Three places

| Place | What runs there | Who operates it |
|---|---|---|
| **Field** | Sensors, turnstiles, point of sale units | Estate maintenance, physically |
| **Zone**, ten of them plus a gate standby | Zone Node: broker, edge inference, local store, sync, local concierge, zone ops view. Admission service on the gate node only | The technical team, remotely, with a physical visit for hardware faults |
| **Cloud**, one region | Ticketing, fiscal, register, backbone, lakehouse, gateway, assurance, experience, forecasting, ops console | Managed services wherever possible |

## Zone Node specification

| | |
|---|---|
| Compute | Small form factor x86 or ARM with an inference accelerator |
| Storage | Local SSD, encrypted, 24 hours of buffered records |
| Power | Mains with battery backup sized for an hour, enough to complete a graceful shutdown and cover brief interruptions |
| Network | Backhaul per ADR-0013, plus local WiFi in the zone with separate segments for visitor devices and staff tablets |
| Enclosure | Weatherproof, tamper evident, lockable |
| Redundancy | **None within a zone, except the gate zone**, which has a warm standby. See below |

## Why no redundancy within a zone

A second Zone Node per zone would roughly double hardware cost and, more
importantly, add ten more systems for a team of three to operate. FF-06 caps
distinct systems requiring routine operation at six.

The exception is the gate. Its node carries Tier 0 admission for every lane,
so a second node there is EUR 12,000 against the revenue path, and it runs the
same software image as the rest of the fleet, so it is not another system to
learn. Everywhere else the failure is made survivable rather than prevented:

| On Zone Node failure | Response |
|---|---|
| Admission, gate zone | Warm standby takes over. If both gate nodes fail, lanes verify signatures alone and single use is reconciled afterward; the duplicate window is measured |
| Admission, any other zone | Not applicable. Only the gate zone admits |
| Welfare monitoring | Enclosures revert to scheduled physical inspection, keeper told which |
| Occupancy | Zone reports unknown. Neighbours unaffected |
| Local concierge | Static signage and staff |

This is the honest cost of edge authority, documented in the
[degraded mode matrix](3_8-degraded-mode-matrix.md) rather than engineered away.

## Cloud deployment

**One region.** No multi region failover. One estate, one location, one
timezone, and a failover story would cost operability, which we ranked third.

What a region outage costs is column C6 of the
[degraded mode matrix](3_8-degraded-mode-matrix.md): online sales for its
duration, the cross-zone view, staff advice and forecasting. On-site sale,
admission, welfare monitoring and the local concierge do not depend on it. That
is the trade, stated rather than implied by the word "floor".

Managed services throughout: managed Kubernetes or serverless for application
workloads, managed streaming for the backbone, managed lakehouse, managed
identity. Every one of these is buying back hours from a team of three, which is
the actual scarce resource.

## Environments

| Environment | Purpose | Zone Nodes |
|---|---|---|
| Development | Feature work | Simulated, no hardware |
| **Staging** | Partition testing, degradation rehearsal, model canary | **Two real Zone Nodes**, physically present |
| Production | The estate | Ten, plus the gate standby |

The two real Zone Nodes in staging are not a luxury. FF-03 partitions a zone
nightly and asserts degraded behavior matches the matrix, and that test is
meaningless against a simulator. The same environment is where the cost
degradation order is exercised, because an order never tested is an order nobody
should trust.

## Deployment cadence

| Component | Cadence | Mechanism |
|---|---|---|
| Cloud services | Continuous, behind feature flags | Standard pipeline |
| Zone Node software | Weekly at most, outside opening hours | Staged, one zone first, automatic rollback |
| Edge models | On evaluation pass only | Signed artefacts, staged, previous version retained |
| Prompts | Continuous, gated by golden set | Versioned as data, FF-12 blocks cost regressions |

Prompts deploy independently of code, which is why they are versioned data. A
prompt change that fails its golden set never reaches a visitor, and a prompt
change that raises cost per interaction by more than 15 percent needs an ADR.

## What the operations team actually does weekly

The six hour budget in FF-07, spent:

| Task | Roughly |
|---|---|
| Review alerts that reached a human | 1 hour |
| Review sampled Tier 2 model outputs, about 100 a week, plus an independent handful of Tier 1 outputs. The bulk of Tier 1 sampling is done by the keepers, managers and maintenance lead already in those loops | 1.5 hours |
| Review override rates and drift indicators | 1 hour |
| Deploy and verify | 1 hour |
| Physical attendance to a hardware fault | 1.5 hours, amortized |

Writing this down was uncomfortable and useful. It is easy to design a system
whose weekly operational load exceeds what the estate can staff, and the only
way to notice is to add the hours up. A flat fifty samples per capability
across eight capabilities would be four hundred a week, which does not fit in
the ninety minutes above. That is why the sampling is tiered, why the Tier 1
samples go to the people who already look at those outputs every day, and why
this team keeps a small independent sample of its own.
