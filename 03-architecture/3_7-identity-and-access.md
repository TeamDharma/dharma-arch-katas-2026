# Identity and access

*Who the system thinks you are, and how little it needs to know.*

## The principle

**Identify the entitlement, not the person.** Almost everything this estate
needs to do requires knowing what someone is allowed to do, not who they are.

That is not only a privacy position. It is simpler, it works offline, and it
removes an entire category of data we would otherwise have to protect.

## Visitors

**There are no visitor accounts.** Buying a ticket does not create one.

| Need | How it is met | What is stored |
|---|---|---|
| Prove entitlement at the gate | Signed credential, verified locally | Product, validity window, group size. No name |
| Family pass for a group | Group size in the credential | No relationships, no names, no ages |
| Use the concierge | Nothing. It is anonymous | Session only, discarded |
| Receive a receipt | Email if the visitor wants one | Handled by the bought ticketing platform, not us |
| Know whether people come back | The ticketing platform keys a hash of the purchaser email it already holds, with a secret it keeps, and reports repeat purchase rates by cohort, suppressing cohorts under fifty | An aggregate. The hash and its key never leave the vendor, and nothing on the estate links a person to a visit |

Repeat visits are the one place identity is unavoidable. We keep it inside the
ticketing platform, which already holds a purchaser email for receipts and
refunds. It computes cohort rates on a keyed hash of that email, with the key
held by the vendor so nothing we receive can be reversed, suppresses any cohort
under fifty purchasers, and hands us the aggregate. The processing is
legitimate interest with a documented balancing test, and it appears in the
DPIA and the privacy notice. Season and annual passes, which are
multi-visit credentials by design, give a second measure at no privacy cost.

Creating visitor accounts would mean a personal data obligation the Countess
never asked for, in order to deliver personalization she never asked for. See
[ADR-0008](../07-decisions/ADR-0008-anonymous-edge-counting.md) for the same
reasoning applied to counting.

## The family pass, which is the interesting case

| Question | Position | Why |
|---|---|---|
| What is a family? | A defined group size with at least one adult | Verifying relationships creates an obligation with no operational benefit |
| Transferable? | No. Single use per visit | Transferability and offline validation are hard to reconcile without a live revocation check |
| Children's data? | None collected | Group size is sufficient. Where age affects price it is checked visually at the gate, as it is today |
| Guardian consent? | Not required by this design | FR-109 remains for any future case that cannot avoid processing a child's data |
| Split across VAT rates? | Yes, apportioned | FR-107, and a reminder that a pass is a fiscal object as well as an access one |

Row three is worth dwelling on. Avoiding children's data started as a compliance
move and produced a simpler product with less to get wrong. That is the useful
pattern: the privacy-preserving option is frequently the operationally simpler
one, and framing it only as compliance obscures that.

## Staff

Staff do need real identity, because they act on regulated records.

| Role | Sees | Can do |
|---|---|---|
| Keeper | Welfare alerts, enclosure state, own zone in detail | Record observations, dismiss concerns with a reason |
| Veterinarian | All welfare data, full animal history | Write register entries, initiate notifiable disease reporting |
| Ride operator | Ride state, own zone | Report faults, record cycles |
| Maintenance lead | Condition data, maintenance history across all rides | Prioritize work. **Cannot alter inspection records** |
| Zone manager | Aggregate zone demand, staffing suggestions | Assign shifts |
| Estate management | Aggregate analytics, cost, forecasts | No operational write access |
| Technical team | System state, model performance, logs | Deploy, configure. **No access to the animal register** |

Two rows carry deliberate weight. The maintenance lead cannot touch inspection
records, because those belong to an accredited body. The technical team cannot
write to the animal register, because a statutory record should not be alterable
by the people who run the database.

## What we do not do

**No role called administrator with access to everything.** Separation between
the technical team and the statutory records is the point, and a superuser role
would dissolve it.

**No staff location tracking**, which is
[ADR-0009](../07-decisions/ADR-0009-aggregate-only-staff-analytics.md) again.
Staff authenticate to systems, not to places.

**No biometrics for anyone**, staff included. Convenient, and a category of data
we decline to hold.

## Offline authorization

Staff devices need to work in a partitioned zone. Authorization is a short lived
signed token cached on the device, valid for a shift, scoped to a zone and a
role. Revocation is opportunistic, exactly as it is for visitor credentials.

The same mechanism, applied twice, and the residual risk is the same: a
revocation window. A dismissed keeper retains zone access until the next sync,
which is a real exposure bounded by shift length and accepted for the same
reason the ticket revocation window is.
