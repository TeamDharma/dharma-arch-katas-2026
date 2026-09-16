# ADR-0004: Offline verifiable ticket credentials

## Status

Accepted

## Context

ADR-0003 puts admission in the deterministic floor, and ADR-0002 requires a zone
to keep working when the cloud is unreachable. Those two decisions together
demand a way for a turnstile to decide whether a ticket is valid without asking
anyone.

Alternatives considered:

- **Live validation against the cloud.** Simple and exact, and it fails
  completely during an outage. Rejected by ADR-0002.
- **Full ticket database replicated to every zone.** Works offline, but means
  every zone holds every visitor's purchase record, which is a data protection
  problem and a synchronization problem at once.
- **Cryptographically signed credential, verified locally.** The turnstile holds
  a public key and verifies a signature. No lookup, no replication of purchase
  data, no network.

The third is how transit systems have worked for two decades. It is not novel,
and novelty here would be a defect.

## Decision

At purchase, the estate issues a signed credential carrying product type,
validity window and group size, and nothing else. A turnstile verifies the
signature locally and checks the credential against the most recent revocation
list it received.

Revocation lists sync opportunistically. The credential carries no personal
data.

**On-site sales during an outage** need a way to sign a credential with the
cloud unreachable. Three constraints meet here: credentials are signed by the
ticketing platform in the cloud, Zone Nodes hold no signing keys, and on-site
sales continue when the link is down. Delegated issuance is how all three hold.

The platform's root key signs a short lived issuing key, valid 48 hours and
rotated daily, for each point of sale unit. The unit keeps that key in a
hardware backed key store, a secure element or TPM on the device. A till
already has to protect a secret for its fiscal module, so this is a known
requirement on the device class rather than a new one; the fiscal module itself
is purpose bound and is not used for it. The gate receives the day's issuer certificates together with
the revocation list, so it verifies a chain rather than a single key. A morning
outage that begins before the daily rotation is covered by the previous day's
key. Zone Nodes still hold no signing keys, which keeps the threat model true.

## Consequences

+ Admission works with no network at all, which is what FR-104 requires.
+ No personal data is distributed to zones, so a compromised Zone Node exposes
  no visitor records.
+ Validation is fast, which helps the 300ms p99 target in NFR-05.
+ It composes with family passes: group size is in the credential, so the gate
  admits the right number without knowing who they are.
− **Revocation is eventually consistent.** A refunded ticket may be admitted
  during the window between refund and revocation list sync. We accept this. The
  fraud value of a refunded day ticket is low, and the alternative is a live
  check that fails during outages.
− Key management becomes a real operational responsibility for a very small
  team, including rotation and the consequences of a compromised signing key.
− Single use enforcement requires local state at the gate, which must survive a
  Zone Node restart.
− Key management now includes a daily delegation to every point of sale unit.
  A stolen unit yields a key worth at most two days of sales from one till,
  revoked at the next sync. That is the bound we accept.
− Verifying a chain rather than a single key costs a few milliseconds per
  admission and a slightly larger QR code.

## Verification

NFR-20 requires a penetration test on forgery and replay with no successful
forgery. FF-05 simulates a four hour outage and requires zero duplicate
admissions on reconciliation, which is where the single use enforcement is
actually tested. FF-01 checks admission success rate per zone every 60 seconds.

FF-02 stubs every cloud dependency and requires an on-site sale followed by
an admission of the credential it produced, which is the test that delegation
works. The same run presents a credential signed with a delegated key older
than 48 hours and requires the gate to reject it.

The revocation window is the known weakness, and we measure it: the time between
a refund and the last zone receiving the updated list is recorded, and if it
exceeds an hour in normal operation the sync design needs revisiting.
