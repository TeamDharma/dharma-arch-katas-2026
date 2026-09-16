# ADR-0008: Anonymous counting at the edge, no biometric identification

## Status

Accepted

## Context

The Countess wants to know which parts of the estate are popular. The obvious
mechanism is cameras that count people.

The estate is a family attraction, so those cameras will process images of
children. That triggers a data protection impact assessment under GDPR Article
35, and children's data is on the supervisory authorities' list of processing
requiring one. Separately, the EU AI Act heavily restricts real time remote
biometric identification in publicly accessible spaces.

Alternatives considered:

- **Camera with re-identification across zones.** Gives full visitor journey
  analytics, which is genuinely more useful than zone counts. Requires
  processing biometric data about children, and would make the separated child
  feature possible.
- **Wristbands with location tracking.** Same journey analytics, no cameras,
  but now the estate holds a movement record per visitor and has to explain it.
- **Anonymous counting at the edge.** Count people crossing zone boundaries,
  process on the Zone Node, discard frames in the same cycle, emit only a
  number.

## Decision

Visitor counting is **anonymous, performed at the edge, retains no frames, and
identifies nobody.** Only counts leave the Zone Node.

No biometric identification, no re-identification across zones, no per visitor
movement record.

## Consequences

+ The DPIA outcome is straightforward, and there is no children's biometric
  processing to defend.
+ It is cheap. Shipping video would dominate the bandwidth budget on a patchy
  network.
+ It is the correct reading of the AI Act's restriction rather than an argument
  about whether an exemption applies.
+ Zone level counts answer the Countess's actual question, which was where to
  invest and deploy staff.
− **We lose visitor journey analytics.** We know a zone is busy, not what people
  did before arriving or where they went next. That is real analytical value
  given up.
− **The separated child feature is not possible.** At a family attraction this
  is the most frequent real operational incident, and an architecture that could
  help with it and chooses not to is making a genuine trade against a real harm.
− Counts are subject to systematic bias by lighting and gate geometry, and
  without identification we cannot deduplicate a visitor who crosses twice.
− Return visits are measured from purchase records inside the ticketing
  platform and from season pass scans, both as cohort aggregates. That is a
  coarser answer to the Countess's third question than journey analytics would
  give, and it is the one this decision permits.

## Verification

FF-09 samples regulated records for reconstructability, and the DPIA documents
the processing. The structural check is that no capability's declared inputs
include biometric or identification features.

Counting bias is measured by monthly manual calibration per zone, with a
correction applied per zone. Without that, a zone whose camera undercounts looks
unpopular, and the estate invests in the wrong place, which is precisely the
mistake we were hired to prevent.

## Note on what is unsettled

The alternative was wristband tracking specifically to enable the separated
child case, on the grounds that a lost child is a concrete harm and journey
analytics is a concrete benefit, while the privacy cost is abstract. Against
it: processing children's location data continuously to solve an infrequent
event, when staff and signage already handle it, is the wrong trade.

This ADR records the conservative option because it is the one the rest of the
documents assume, not because the question was settled. It remains open in
[OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md) and it is the decision we are least
sure of.
