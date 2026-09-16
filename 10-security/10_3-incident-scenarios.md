# Incident scenarios

*What the system does when something goes badly wrong in the physical world.
None of these are software incidents.*

## Venomous animal escape

| | |
|---|---|
| **Detection** | Enclosure sensors, keeper observation, or a visitor report. The system is not the primary detector and should not be presented as one |
| **System role** | Zone occupancy data shows how many people are in the affected zone and adjacent ones, immediately, without identifying anyone |
| **What it does not do** | Decide anything. Evacuation is a human decision under an existing emergency procedure |
| **Degraded** | If the Zone Node is down, occupancy is unknown for that zone and the emergency procedure runs as it does today, without our help |

The useful contribution is small and specific: a count. Knowing that 340 people
are in the aquatic house changes how an evacuation is run. An architecture that
claimed more than that would be overselling.

## Separated child

The most frequent real incident at a family attraction, and **the one we
deliberately cannot help with.**

[ADR-0008](../07-decisions/ADR-0008-anonymous-edge-counting.md) rules out
re-identification across zones, which is exactly the capability that would let
the system find a child.

| | |
|---|---|
| **System role** | None, beyond zone occupancy context |
| **Why** | Continuously processing children's location data to solve an infrequent event, when staff and signage already handle it, was judged the wrong trade |
| **Unsettled** | Whether wristband tracking should be added for this case. Recorded in [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md), and it is the decision we are least sure of |

We are stating this plainly rather than omitting it, because a reader evaluating
the privacy decision deserves to see what it costs. The cost is a real harm to a
real family, weighed against continuous surveillance of every child on the
estate, and reasonable people took different views inside this team.

## Medical emergency

| | |
|---|---|
| **Detection** | Human |
| **System role** | Zone location context for responders, and step-free route information for stretcher access |
| **What it does not do** | Triage, or anything resembling a clinical judgment |

## Ride incident

| | |
|---|---|
| **Detection** | Ride operator, or ride safety systems that are entirely separate from ours |
| **System role** | Preserve telemetry from the period before the incident, unaltered, for the investigation |
| **Critical constraint** | Our predictive maintenance output is **not** evidence of ride safety and must never be presented as such. Statutory inspection is the safety regime ([ADR-0003](../07-decisions/ADR-0003-no-ai-in-the-revenue-path.md), FR-503) |

The telemetry preservation point is worth emphasizing. After an incident, the
temptation to look at the data is strong and the risk of contaminating it is
real. Telemetry for the affected ride is frozen automatically on incident
declaration.

## Notifiable animal disease

| | |
|---|---|
| **Detection** | Welfare monitoring may flag indicators. A veterinarian confirms |
| **System role** | Advisory alert, plus the evidence trail |
| **What it does not do** | **Notify the authority.** Ever. A veterinarian decides and reports (FR-409) |
| **Why** | Notification is a regulated act with consequences for the estate's licence. A false positive notification is not a minor error |

## Total connectivity loss during peak

Covered as QS-01 in
[2_5](../02-requirements/2_5-quality-scenarios.md) and in the
[degraded mode matrix](../03-architecture/3_8-degraded-mode-matrix.md).

Summary: turnstiles keep admitting, point of sale keeps selling and recording,
welfare monitoring continues at the edge, the concierge answers common questions
locally, and open ended queries state their limit. The estate carries on.

## The pattern across all of these

In every scenario the system's role is to **supply context to a human running an
existing procedure**. It does not detect, decide, escalate or notify.

That is a deliberately modest position, and it is the same one the tier model
takes everywhere else. The estate had emergency procedures before we arrived.
Our job is to make them better informed, not to replace them with something that
has a confidence score.
