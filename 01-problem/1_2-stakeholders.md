# Stakeholders

*arc42 section 1. Who has a stake in this system, what they expect from it, and
what they can do if they do not get it.*

The last column is the one that matters. A stakeholder list that records
interest but not leverage tells you who to inform, not who can stop you.

## Primary stakeholders

| Stakeholder | What they expect | Leverage |
|---|---|---|
| **The 72nd Countess Von Digitalis** | A profitable estate, 15,000 visitors a day within three years, and not returning to the garden gnome business | Owner. Funds or cancels the work |
| **Visitors and family groups** | To get in quickly, find their way, and have a day worth repeating | Revenue. They leave and do not come back |
| **Keepers and veterinarians** | Animals that stay healthy, and a system that supports their judgment rather than overriding it | Domain authority. If they do not trust the alerts, they will ignore them, and the capability becomes worthless |
| **Ride operators and estate staff** | To know where they are needed, and not to be individually monitored | Daily operation of the estate |
| **Estate management** | Visibility into what is popular, what it costs, and whether the target is reachable | Commissions and prioritizes the work |
| **The permanent technical team, 2 to 3 people** | A system they can actually run alongside their other jobs | They inherit everything. If it is unrunnable, it degrades whatever we write |

## Regulatory and institutional stakeholders

| Stakeholder | What they expect | Leverage |
|---|---|---|
| **Works council** | No technical system capable of monitoring individual staff performance, without their agreement | **Veto.** Under BetrVG section 87(1)(6), capability is the trigger, not intent. No agreement, no system |
| **BayLDA, the Bavarian data protection authority** | Lawful processing, a completed DPIA for visitor counting, and demonstrable minimization | Enforcement, including orders to stop processing |
| **Veterinary authority** | An accurate statutory animal register and prompt notification of notifiable disease | Licensing of the collection |
| **Ride inspection body** | Rides inspected on schedule by them, not by our models | Rides do not open without approval |
| **Heritage authority** | Protected 18th century structures not altered | Refusal of permission to mount anything invasive |
| **Tax authority** | Fiscally compliant records and receipts from every point of sale | Audit, penalty |

## Stakeholders with a veto

Three of the above can stop this system regardless of how good the architecture
is, and we designed around each specifically rather than hoping to negotiate
later.

**The works council** shaped FR-303 through FR-305 and FF-29. Staff analytics
are aggregate-only by design, and the absence of individual identifiers is
asserted at schema level on every build. This was not a privacy preference, it
was a precondition.

**The heritage authority** shaped the entire sensing approach. Non-invasive,
battery powered, removable. It is why ride telemetry looks the way it does in
FR-501.

**The keepers and veterinarians** hold a softer but equally real veto. Nothing
forces a keeper to act on an alert. A welfare system whose alerts are not
trusted is not a partially useful system, it is an expensive one that nobody
opens. That is why every Tier 1 capability logs override rate, and why an
override rate above 20 percent triggers a model review rather than a
conversation about compliance (FF-30).

## Who we are not designing for

**Tourists who want a mobile app.** Some will. Nothing in the visitor
experience may require one.

**Data scientists inside the estate.** There are none, and there will not be.
This constrains what kind of AI we can responsibly deploy more than any
technical limit does.

**Third party data consumers.** Opening the data platform externally is
interesting in year three. Naming them as stakeholders now would pull design
decisions toward a future that may not arrive.
