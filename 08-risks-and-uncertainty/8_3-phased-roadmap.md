# Phased roadmap

*Zero to thirty six months. The ordering is the argument.*

## The principle

**Revenue before instrumentation, instrumentation before intelligence.**

The estate needs to sell tickets before it needs to be clever, and it needs data
before it can have models. Every phase boundary is a point where the Countess
could stop and still have something that works.

## Phase 0, months 0 to 6: the estate can trade

Six months, because three is not achievable from a standing start when the
site survey has not run, the backhaul is undecided and the ticketing vendor has
not been selected. The first two months are those three things. The estate continues on
its present manual arrangements until the new system takes over.

| Months | Ships | Why first |
|---|---|---|
| 0 to 2 | Site survey and backhaul decision, closing [ADR-0013](../07-decisions/ADR-0013-connectivity-backhaul.md) | Everything physical depends on it |
| 0 to 2 | Ticketing vendor selected against the two hard criteria in [ADR-0012](../07-decisions/ADR-0012-buy-ticketing-build-the-ai.md) | The floor is partly a bought product |
| 0 to 2 | Heritage permissions for sensing and Zone Node siting | A refusal here changes the physical design |
| 2 to 6 | Ticketing, family passes, point of sale with TSE | Revenue on the new system from month six |
| 2 to 6 | Offline verifiable credentials, delegated issuance, turnstiles | Admission survives the network |
| 2 to 6 | Zone Nodes installed, gate standby, connectivity backhaul | Everything later depends on it |
| 2 to 6 | Fiscal records, accessibility conformance | Legal from the first sale |

**No AI at all.** Deliberately. The estate has to sell a ticket and admit a
visitor before it does anything sophisticated, and this phase is the
deterministic floor arriving before anything is allowed to stand on it.

**Exit criterion:** FF-01 and FF-02 passing. The estate trades through a
simulated cloud outage, including an on-site sale followed by admission of the
credential it produced.

## Phase 1, months 6 to 12: the estate can see

| Ships | Why |
|---|---|
| Sensing across enclosures and rides | Non-invasive, per [ADR-0002](../07-decisions/ADR-0002-zone-based-edge-architecture.md) and heritage constraints |
| Anonymous zone counting | Answers "which parts are popular" with measurement, no model |
| Welfare monitoring on **threshold rules** | Keeper written, needs no data, catches most real incidents |
| Data platform, event backbone, lakehouse | Where the training data will come from |
| Curated concierge FAQ and wayfinding | The permanent fallback, shipped before the thing it backs up |
| Accessibility: reference translations, static audio description | Legal obligation, and the highest value capability per euro |

Three of the six "unknown" baselines in
[1_1](../01-problem/1_1-business-goals-and-challenges.md) become numbers here.
That is the phase's real deliverable: the Countess stops guessing.

**Exit criterion:** every zone reporting occupancy, twelve weeks of welfare data
accumulated, yield per visitor measured for the first time.

## Phase 2, months 12 to 18: the estate can reason

Capabilities move from rules to models, **one at a time, each only when it beats
its baseline**. Six months is tight for eight capabilities with eight and twelve
week evaluation windows. The windows run on data collected from phase 1, and a
capability that misses its gate slides into phase 3 rather than shipping below
its baseline.

| Ships | Gate |
|---|---|
| Voice concierge, open ended queries | Golden set of 300, FF-21, FF-22, FF-23 |
| Welfare anomaly detection, aquatic then terrestrial | Beat threshold rules on false negative rate over 12 weeks |
| Demand forecasting | Beat the lookup table by 10 percent MAPE over 8 weeks (FF-28) |
| Staff deployment advice | Beat the ratio rule on manager acceptance over 8 weeks |
| Piranha population estimation | Calibrated against 12 physical counts |
| Predictive maintenance | Demonstrated lead time on 3 real events |
| Model gateway, assurance plane, budget guard | Ship before the first model, not after |

The last row is not negotiable. The assurance plane exists before the first
capability it assures, because FF-20 fails the build for any AI capability
without a golden set, a threshold and a CI evaluation.

**Exit criterion:** every shipped capability holding above threshold for eight
consecutive weeks, AI spend under the ceiling.

## Phase 3, months 18 to 36: the estate can grow

| Ships | Why here |
|---|---|
| Scale to 15,000 visitors per day | Capacity work, largely not software |
| Return visit products and cohort analysis | Needs a year of data to be meaningful |
| Itinerary suggestions | The lowest value capability, so it goes last and degrades first |
| Full language coverage | Expanded as visitor mix is actually measured |
| AI literacy training for staff | AI Act Article 4. A delivery item, not somebody else's problem |

## What each phase costs

| Phase | Capital | Cumulative |
|---|---|---|
| 0 | EUR 900,000 | EUR 900,000 |
| 1 | EUR 1,000,000 | EUR 1.9 million |
| 2 | EUR 700,000 | EUR 2.6 million |
| 3 | EUR 200,000 | EUR 2.8 million |

Two thirds of the capital is spent before the first model ships. That is not an
accident of scheduling, it is what "revenue before instrumentation,
instrumentation before intelligence" costs, and we think it is the right shape
for a business with a plant collection at stake.

## Where the Countess can stop

| After | What she has | What she has spent |
|---|---|---|
| Phase 0 | A trading estate with compliant ticketing that works offline | EUR 900,000 |
| Phase 1 | The above, plus knowing which zones are popular, what a visitor is worth, and whether animals are unwell | EUR 1.9 million |
| Phase 2 | The above, plus every AI capability, each of which beat a working alternative before shipping | EUR 2.6 million |

Every boundary is a working system rather than a half-built one. For an estate
whose failure condition is financial, that optionality is worth more than
arriving faster.
