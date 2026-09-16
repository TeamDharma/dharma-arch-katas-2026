# Threat model

*What can go wrong deliberately, as distinct from what can go wrong by
accident, which is [8_2](../08-risks-and-uncertainty/8_2-risk-register.md).*

Scoped to the things this architecture actually changes. We are not writing a
general security programme for a stately home.

## Assets worth attacking

| Asset | Why someone wants it | Worst case |
|---|---|---|
| Ticket credentials | Free entry, resale | Revenue loss at scale if forgery is possible |
| Point of sale and fiscal records | Tax fraud, or sabotage | Regulatory exposure, criminal liability for the estate |
| Animal register | It is a licensing record | Falsified welfare history, licence at risk |
| Visitor personal data | Ordinary theft, and children are present | Regulatory and reputational, and the reputational is worse |
| Zone Nodes | Physical devices in a public park | Foothold, or denial of admission in a zone |
| The concierge | A public endpoint with a brand attached | Reputational, at a family attraction |

## Trust boundaries

| Boundary | Direction | Posture |
|---|---|---|
| Visitor device to Zone Node | Inbound | **Fully untrusted.** Everything validated server side, per [ADR-0004](../07-decisions/ADR-0004-offline-verifiable-ticket-credentials.md) |
| Zone Node to cloud | Outbound | Authenticated per device, no shared secrets |
| Cloud to model provider | Outbound | Untrusted output. Treated as data, never as instruction |
| Staff device to ops console | Inbound | Authenticated, managed identity |
| Third party to anything | Inbound | Resellers write through a narrow API. No direct data access |

The server-authoritative posture on the first row is borrowed directly from
game servers, where the client is assumed hostile by default. A turnstile does
not trust a phone screen, it verifies a signature.

## Threats and controls

| Threat | Control | Where |
|---|---|---|
| Ticket forgery | Cryptographic signature verified locally, public key only on the gate | ADR-0004, NFR-20 |
| Ticket replay | Single use enforced at the gate, local state survives restart | FF-05 |
| Refund abuse in the revocation window | Accepted, low value, measured | R11 in the risk register |
| Zone Node physical compromise | Per device credentials, no shared secrets, no visitor personal data held locally, encrypted storage | NFR-22 |
| Lateral movement from one Zone Node | Per device identity, zone-scoped authorization | NFR-22 |
| Point of sale tampering | Certified TSE, which is the regulatory control doing security work | FR-106 |
| Card data theft | Card data never touches estate infrastructure | NFR-23 |
| Point of sale unit theft | Delegated issuing key valid 48 hours, scoped to one till, revoked at next sync. Credentials it signs after revocation are rejected at the gate | ADR-0004 |
| Animal register falsification | Every change carries actor, timestamp and evidence, fully reconstructable | FF-09, NFR-28 |
| Denial of service on the concierge | Rate limiting, and degradation to curated content rather than failure | Degraded mode matrix |
| Model provider compromise | Output treated as untrusted data. No model output reaches Tier 0 | ADR-0003 |

## What the deterministic floor does for security

[ADR-0003](../07-decisions/ADR-0003-no-ai-in-the-revenue-path.md) was made for
availability reasons. It turns out to be a security control too.

Because no model output reaches ticketing, payment, fiscal records or the animal
register, a compromised or manipulated model cannot cause a financial or
regulatory event. The worst a poisoned or hijacked model achieves is a bad
answer to a visitor or a spurious welfare alert that a human then dismisses.

That containment is structural rather than configured, which is the kind of
security control that survives a team change.

## What is out of scope

**Physical security of the estate.** Fences, gates and the animal collection's
own containment are not our problem and we should not pretend otherwise.

**Insider threat from estate management.** We provide audit trails. We do not
design against the owner.

**Nation state adversaries.** An amusement park in Bavaria is not that target,
and designing for it would spend the operability budget we do not have.

## The uncomfortable one

Zone Nodes are physical computers in a public park, reachable by anyone with a
screwdriver and some patience. We can encrypt storage, scope credentials and
detect tampering, but we cannot make them physically secure.

The design response is to assume a Zone Node will eventually be opened, and to
ensure that what it holds is worth very little: no visitor personal data, no
shared secrets, no signing keys, and credentials scoped to one zone. A stolen
Zone Node should be an expensive brick rather than a key to the estate.

Signing keys live in two places only. The root is in the ticketing platform.
A 48 hour delegated key sits in a hardware backed key store on each point of
sale unit, a secure element or TPM, which is a requirement a till already meets
for its fiscal module
([ADR-0004](../07-decisions/ADR-0004-offline-verifiable-ticket-credentials.md)).
Neither is on a Zone Node.
