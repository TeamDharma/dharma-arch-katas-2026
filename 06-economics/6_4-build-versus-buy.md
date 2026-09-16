# Build versus buy

*The decision is in
[ADR-0012](../07-decisions/ADR-0012-buy-ticketing-build-the-ai.md). This page is
the arithmetic behind it.*

## The constraint that decides it

Two to three technical staff will run this permanently, and they will have other
jobs. Operability is our third ranked characteristic
([2_3](../02-requirements/2_3-architecture-characteristics.md)), and FF-06 caps
distinct systems requiring routine human operation at six.

Every build decision spends some of that budget. That is the real currency here,
not euros.

## The split

| Component | Decision | Why |
|---|---|---|
| Ticketing, passes, point of sale, TSE, payments | **Buy** | Solved, regulated, and the regulation changes without us |
| Zone Node and edge runtime | **Build** | Nothing off the shelf fits patchy connectivity plus local admission authority |
| Model gateway | **Build** | Thin, and it is the seam three characteristics depend on |
| Assurance plane | **Build** | The differentiator. Buying it would mean accepting someone else's definition of adequate |
| AI capabilities | **Build** | Domain specific. No product knows what a healthy piranha enclosure looks like |
| Lakehouse and event backbone | **Buy**, managed | Commodity, and self-hosting fails the operability budget outright |
| Identity for staff | **Buy**, managed | Never build authentication |

## The arithmetic on ticketing

The clearest case, so worth showing.

| | Build | Buy |
|---|---|---|
| Capital | ~EUR 600,000. Ticketing, passes, TSE certification, payment integration, accessibility conformance | EUR 180,000 license and implementation |
| Annual operating | Our team maintains fiscal compliance forever | EUR 90,000 to 140,000 license |
| Operability budget | 2 of our 6 systems | 1 of our 6 |
| Regulatory change | **Ours** | **Theirs** |
| Time to phase 0 | 9 months minimum | 3 months |

The decisive row is regulatory change. German fiscal requirements move, and a
two person team owning a certified point of sale implementation in perpetuity is
the kind of commitment that looks affordable in year one and is unbearable by
year four.

## The two hard requirements on the bought product

It must support **offline validation of credentials at the gate**, and
**delegated issuance at the point of sale** so an on-site sale during a cloud
outage still produces a credential the gate can verify
([ADR-0004](../07-decisions/ADR-0004-offline-verifiable-ticket-credentials.md)).

A product requiring connectivity at the turnstile, or one that can only issue
from its cloud, is disqualified regardless of its other merits, because either
would put the deterministic floor behind a network link we have been told is
unreliable.

If no product meets both bars, ADR-0012 reverses and the build scope grows by
roughly EUR 400,000 and six months. That is the contingency, and it is the main
risk in this decision.

## Why we build the assurance plane

It is the most obviously buyable thing we chose to build, so it needs a reason.

Evaluation and monitoring products exist and several are good. They are built
around a generic notion of model quality, and our thresholds are domain specific
in ways that matter: a false negative on a sick animal is not comparable to a
false negative anywhere else, the piranha capability must structurally refuse to
emit a bare number, and staff analytics must fail a build over a schema field.

Those are not configurations of a general tool. They are the argument of the
submission, and we would rather own them.

The build is also small. Golden sets, a scoring runner, a drift check, a budget
guard and sampling. Most of it is data rather than code, which is why it fits a
team that also has to ship everything else.

## What we would revisit

If the estate ever grows a real technical team, self-hosting parts of the data
platform becomes worth reconsidering. Until then, every managed service is
buying back hours from a team of three, and hours are the constraint.
