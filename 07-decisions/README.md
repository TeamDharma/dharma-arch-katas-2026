# Architecture decision records

Sixteen decisions, one file each, plus the template. Every ADR carries a
**Verification** section, because a decision nobody can check is a preference.

Consequences are written with the bad news included. An ADR whose consequences
are all positive was written after the decision, to justify it.

| # | Decision | Status |
|---|---|---|
| [0001](ADR-0001-jurisdiction-and-regulatory-baseline.md) | Jurisdiction and regulatory baseline: Bavaria, Germany | Accepted |
| [0002](ADR-0002-zone-based-edge-architecture.md) | Zone based edge architecture | Accepted |
| [0003](ADR-0003-no-ai-in-the-revenue-path.md) | **No AI in the revenue path** | Accepted |
| [0004](ADR-0004-offline-verifiable-ticket-credentials.md) | Offline verifiable ticket credentials | Accepted |
| [0005](ADR-0005-model-gateway-as-single-seam.md) | The model gateway as the single provider seam | Accepted |
| [0006](ADR-0006-heuristic-baseline-retained-permanently.md) | Retain the heuristic baseline permanently | Accepted |
| [0007](ADR-0007-text-chat-concierge.md) | Text chat concierge | **Superseded by 0016** |
| [0008](ADR-0008-anonymous-edge-counting.md) | Anonymous counting at the edge, no biometric identification | Accepted |
| [0009](ADR-0009-aggregate-only-staff-analytics.md) | Aggregate only staff analytics | Accepted |
| [0010](ADR-0010-animal-register-as-system-of-record.md) | The animal register is the system of record | Accepted |
| [0011](ADR-0011-piranha-population-as-interval.md) | Piranha population as an interval, never a count | Accepted |
| [0012](ADR-0012-buy-ticketing-build-the-ai.md) | Buy ticketing and point of sale, build the AI | Accepted |
| [0013](ADR-0013-connectivity-backhaul.md) | Connectivity backhaul | **Proposed**, unresolved |
| [0014](ADR-0014-ai-spend-ceiling-and-budget-guard.md) | AI spend ceiling with a runtime budget guard | Accepted |
| [0015](ADR-0015-model-provider-exit-strategy.md) | Model provider exit strategy | Accepted |
| [0016](ADR-0016-voice-first-concierge.md) | Voice first visitor concierge | Accepted, supersedes 0007 |

## Three worth reading first

**[0003](ADR-0003-no-ai-in-the-revenue-path.md)** is where we decline to use AI.
In a competition about AI, the boundary is the argument.

**[0007](ADR-0007-text-chat-concierge.md) and
[0016](ADR-0016-voice-first-concierge.md)** are a decision and its reversal. We
left 0007 intact rather than editing it, because how we changed our minds is
more useful than a tidy history.

**[0013](ADR-0013-connectivity-backhaul.md)** is recorded as Proposed and not
answered. It needs a physical site survey we could not do, and inventing a
confident decision would have been worse than admitting the gap.
