# ADR-0002: Zone based edge architecture

## Status

Accepted

## Context

WiFi coverage across the estate is patchy and the brief tells us not to expect
that to change. There is budget for MQTT capable hardware throughout the park.
The estate must serve 5,000 visitors a day today and 15,000 within three years.

The obvious architecture is a cloud application with sensors reporting to it.
That design has a property we cannot accept: when the link degrades, the estate
stops working. Turnstiles stop, welfare monitoring goes blind, and the failure
is total rather than partial.

Alternatives considered:

- **Cloud first with retry and buffering.** Simplest to build and to operate.
  Fails the availability requirement during an outage, because a turnstile that
  cannot reach the cloud cannot admit anyone regardless of how good the retry
  logic is.
- **Fully distributed, no cloud.** Removes the dependency entirely but makes
  analytics, forecasting and cross-zone reporting extremely awkward, and leaves
  a two to three person team operating hardware with no central management.
- **Zone based edge with cloud reconciliation.** Local authority per zone,
  opportunistic sync to a cloud that handles analytics and cross-zone concerns.

Massively multiplayer game servers face the same problem: thousands of
concurrent participants moving through a bounded space divided into regions,
over networks that fail. The zone model is how that problem is solved there,
and the estate is the same problem in physical form.

## Decision

The estate is divided into zones. Each zone has a **Zone Node** providing edge
compute, an MQTT broker, local storage, local inference and a zone ops view for
staff tablets.

Admission is a perimeter concern. Visitors are admitted to the estate at the
gate, and internal zones are not gated, so only the **gate zone's** node runs
the admission service, for every turnstile lane.

The Zone Node is authoritative for what happens in its zone. The cloud is where
zones reconcile, not where they live. Every link from estate to cloud is store
and forward.

## Consequences

+ Admission, point of sale and welfare monitoring survive a cloud outage,
  which is what makes the deterministic floor possible at all.
+ Bandwidth drops sharply, because events and embeddings cross the link rather
  than video.
+ Inference at the edge is capital expenditure rather than per-call operating
  cost, which helps the EUR 0.10 per scanned admission ceiling considerably.
+ Zone failures are contained. One zone down does not affect its neighbours.
− **Operability cost.** Deploying software and model updates to edge devices
  over patchy connectivity is a genuine distributed systems problem, and it
  lands on a two to three person team. NFR-19 exists because of this decision.
− Zone Node failure is now a real single point of failure for that zone. The
  degraded mode matrix shows welfare monitoring reverting to physical inspection
  and occupancy going unknown.
− The gate Zone Node carries Tier 0 admission for every lane, so it is the one
  node with a warm standby. That is a second box to operate, accepted because a
  single point of failure on the revenue path is the thing this decision exists
  to remove. It runs the fleet's software image, so it is not an eleventh
  system under FF-06.
− Reconciliation logic must be idempotent and resumable, which is harder to get
  right than a synchronous write.
− Physical hardware on site means physical maintenance, in a park, in weather.

## Verification

FF-03 partitions a zone in staging nightly and asserts that every Tier 0 and
Tier 1 capability behaves as the degraded mode matrix says it will. FF-05
simulates a four hour outage weekly and requires zero lost admissions and zero
duplicate charges on reconciliation. FF-01 runs a synthetic admission against
each zone every 60 seconds.

If FF-03 cannot be made to pass, this decision is wrong and we would return to
cloud first with a much smaller AI footprint.
