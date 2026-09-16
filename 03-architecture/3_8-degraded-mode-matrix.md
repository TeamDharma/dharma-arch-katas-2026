# Degraded mode matrix

*arc42 section 8, crosscutting. What every capability does when something it
depends on is unavailable.*

WiFi coverage is patchy and we are told not to expect it to improve. That makes
degraded operation the normal case rather than the exception, and a capability
without a declared degraded behavior is a capability that will fail in a way
nobody planned.

**FF-04 fails the build if any cell in this table is blank.** That is the
mechanism that stops this page becoming stale the moment someone adds a feature.

## Failure conditions

| Code | Condition |
|---|---|
| **C1** | Zone to cloud link down, zone otherwise healthy |
| **C2** | Model provider unreachable or failing |
| **C3** | Zone Node itself down |
| **C4** | Cost ceiling reached |
| **C5** | Evaluation threshold breached for a capability |
| **C6** | Cloud region or cloud provider down, estate network healthy |

## The matrix

| Capability | Tier | C1 cloud link down | C2 model provider down | C3 Zone Node down | C4 cost ceiling | C5 eval breach | C6 cloud down |
|---|---|---|---|---|---|---|---|
| Ticket purchase, online | 0 | Unaffected, runs in cloud | Unaffected | Unaffected | Unaffected | Unaffected | **Unavailable** for the duration. Visitors buy at the gate. Accepted, see 3_6 |
| Ticket purchase, on site | 0 | Continues on the point of sale unit's delegated 48 hour issuing key, records locally, queues fiscal submission | Unaffected | Point of sale units keep their own delegated key and TSE. Gate standby node takes over lane state | Unaffected | Unaffected | As C1 |
| Admission at turnstile | 0 | **Continues.** Signed credential validated locally against issuer certificates and the last revocation list | Unaffected | Gate standby takes over. If both gate nodes fail, lanes verify signatures alone and single use is reconciled afterward; the duplicate window is measured | Unaffected | Unaffected | As C1 |
| Fiscal record and receipt | 0 | Records locally, submits on reconnect | Unaffected | Records at the point of sale device. The TSE is local to the till | Unaffected | Unaffected | As C1 |
| Animal register writes | 0 | Taken by the zone ops view, queued on the Zone Node, reconciled on reconnect | Unaffected | Paper fallback, keyed in later. This is the statutory path anyway | Unaffected | Unaffected | As C1 |
| Water quality monitoring | 1 | Continues at edge, alerts to the zone ops view | Continues, threshold rules only | **Enclosure reverts to scheduled physical inspection** | Unaffected, edge inference is capex not opex | Reverts to threshold rules | As C1 |
| Terrestrial welfare monitoring | 1 | Continues at edge, alerts to the zone ops view | Continues, threshold rules only | Scheduled physical inspection | Unaffected | Reverts to threshold rules | As C1 |
| Piranha population estimate | 1 | Estimate produced locally, published on reconnect | Continues, last calibration | Physical count schedule unchanged | Unaffected | Physical count only | As C1 |
| Zone occupancy counting | 1 | Counts locally, buffers | Unaffected, this is measurement not inference | Zone shows as unknown, neighbours unaffected | Unaffected | n/a | Counts locally, buffers. Cross-zone view unavailable |
| Staff deployment advice | 1 | Last received advice remains on the ops console, marked stale | Falls back to occupancy divided by staffing ratio | Zone excluded from advice | Suspended, advisory only | Falls back to ratio rule | Unavailable. Managers apply the ratio rule by hand |
| Predictive maintenance | 1 | Buffers telemetry, no live advice needed | Falls back to manufacturer intervals | Telemetry gap logged against the ride | Suspended | Falls back to intervals | Manufacturer intervals |
| Voice concierge, common intents | 2 | **Continues.** Local concierge answers from zone cache | Continues, local intents need no provider | Static signage and staff | Unaffected, local | Reverts to curated FAQ | Continues, local |
| Voice concierge, open ended | 2 | Unavailable. Local concierge states the limit and offers staff | Reverts to curated FAQ | Unavailable | **First capability degraded** | Reverts to curated FAQ | As C1 |
| Translation and accessibility | 2 | Cached languages continue, others unavailable | Cached content only | Unavailable | Reserved floor the guard cannot consume. At the hard stop, local cached content. Never dark | Language disabled individually | Cached languages and recorded descriptions continue |
| Itinerary suggestions | 2 | Unavailable, static recommended routes shown | Static routes | Static routes | Second capability degraded | Static routes | Static routes |
| Demand forecasting | 3 | Unaffected, runs in cloud on buffered data | Falls back to lookup table | Zone data gap, forecast flagged | Suspended, weekly job | Falls back to lookup table | Unavailable. Last forecast stands, marked stale |
| Operations console | 1 | Shows last known state with staleness marked | Unaffected | Zone shown as unreachable | Unaffected | Unaffected | Unavailable. Zone ops views continue per zone |

## Degradation order under cost pressure

When the budget guard triggers at EUR 0.08 per scanned admission, capabilities are
degraded in this order, and it is fixed in advance rather than decided under
pressure:

**Accessibility and translation hold a reserved budget floor that the guard
cannot touch.** The guard degrades only the unprotected remainder, in this
order:

1. Itinerary suggestions
2. Voice concierge, open ended queries, falling back to curated FAQ
3. Demand forecasting, falling back to the lookup table

An earlier design put accessibility last in the shutdown queue rather than
behind a floor. Adversarial review pointed out that an ordering only delays the
outcome: under sustained pressure the queue eventually reaches the thing you
said you would protect. A floor does not.

**At the hard stop, when all metered budget is exhausted**, accessibility
continues on local cached content: reference translations, recorded audio
description, step free routing. Zero marginal cost, so it cannot be exhausted.
That is how a protected floor, an ordering, and a hard cap can all be true at
once, and it only works because
[ADR-0006](../07-decisions/ADR-0006-heuristic-baseline-retained-permanently.md)
keeps every baseline permanently.

The reasoning is unchanged. For most visitors the concierge is a convenience.
For a visitor who depends on audio description or on a language they can
actually read, it is the difference between using the estate and not.

## Two things this table makes visible

**No on-site Tier 0 capability has a blank or a failure in the C1, C2 or C6
columns.** The estate sells tickets at the gate and admits visitors through a
cloud link outage, a total model provider failure and a cloud region outage.
Online sales stop under C6, and the matrix says so rather than hiding it behind
a claim about the floor. That is the deterministic floor, demonstrated rather
than asserted.

**C3, the Zone Node itself failing, is where the real losses are.** Welfare
monitoring reverts to physical inspection, occupancy goes unknown for that zone,
and the concierge goes silent locally. That is the honest cost of putting
authority at the edge, and it is why Zone Node hardware is specified with
redundant power and why the gate zone, the one that admits, is the one zone
with a standby node.

We did not design a Zone Node failure away. We made it survivable and wrote down
what it costs.
