# ADR-0013: Connectivity backhaul between zones and cloud

## Status

**Proposed.** This is the largest open decision in the architecture.

## Context

ADR-0002 puts authority at the Zone Node and makes every estate to cloud link
store and forward. That decision deliberately reduces how much the backhaul
choice matters, but it does not eliminate it. Reconciliation latency, telemetry
freshness and operating cost all depend on it.

The estate is large and sprawling, with protected structures, animal enclosures
where cabling is disruptive, and existing coverage described only as patchy.

Options:

| Option | Strengths | Weaknesses |
|---|---|---|
| **Fibre to each Zone Node** | Fast, reliable, cheap to run once installed | Capital cost, groundworks across a heritage estate, and permission problems near protected structures |
| **Private 5G** | Good coverage, high capacity, one network to manage | Highest capital cost, spectrum and licensing, and an operational burden a two person team should not carry |
| **Mesh WiFi backhaul** | Cheapest, incremental, no groundworks | Least reliable, degrades in weather and foliage, which is exactly the failure we are told already exists |
| **LoRaWAN for sensors plus LTE for Zone Nodes** | Very low power for sensors, no groundworks, LTE where it works | LoRaWAN bandwidth suits telemetry but not the concierge; LTE coverage on the estate is unverified |

## Decision

**Not yet made.** We are recording it as proposed rather than inventing a
confident answer.

What we can say is that the architecture is deliberately indifferent to which
option wins. Because every zone holds local authority and every cross-boundary
link is store and forward, the backhaul choice affects reconciliation latency
and running cost, not correctness. A slower or less reliable backhaul makes the
estate's data staler, not its turnstiles broken.

Our working assumption for the cost model is **LoRaWAN for sensors plus LTE with
fibre where it already exists for Zone Nodes**, and the cost model carries a
placeholder that is the largest single uncertainty in
[6_1](../06-economics/6_1-cost-model.md).

## Consequences

+ Recording this as open is more useful than a fabricated decision, and the
  quality scenarios already treat backhaul failure as a normal condition.
+ The architecture's indifference to the answer is a genuine property, and it is
  worth stating because it is the payoff from ADR-0002.
− The cost model has a placeholder in a material line item, so the total is
  softer than it looks.
− Site survey work is the first two months of phase 0, which is six months
  partly to make room for it and for vendor selection.
− If the eventual answer is much worse than assumed, telemetry freshness targets
  such as NFR-08 may need relaxing.

## Verification

FF-03 and FF-05 test behaviour under partition regardless of the backhaul
technology, which is why they were written in terms of the failure rather than
the medium. Whatever is chosen, those tests stay the same.

The decision needs a physical site survey, scheduled in the first two months
of phase 0. Until then it stays
proposed, and it is the first entry under Architecture in
[OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md).
