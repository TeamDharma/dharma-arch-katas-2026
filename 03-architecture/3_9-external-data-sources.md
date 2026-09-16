# External data sources

*The cheapest accuracy improvement available to this estate, and the one most
easily forgotten.*

## Why this has its own page

Demand forecasting for an outdoor attraction is mostly not about the attraction.
Weather and school holidays explain more of daily attendance variation than
anything the estate controls, and both are published, free, and available before
the day they describe.

A team that builds a sophisticated model on internal history and ignores the
weather has built a worse forecaster than a lookup table with a rain column.

## Sources

| Source | What it gives | Update | If it fails |
|---|---|---|---|
| **Weather forecast** | Temperature, precipitation probability, wind, by hour | Hourly, 7 days ahead | Fall back to seasonal averages, flag reduced confidence |
| **Weather observation**, on site | Actual conditions at the estate, not the nearest city | Continuous | Use the forecast provider's observation |
| **Bavarian school holiday calendar** | Term dates for Bavaria and neighbouring states | Annual, published in advance | Static copy, refreshed annually. Low risk |
| **Public holidays** | Bavarian and national, which differ | Annual | Static copy |
| **Local events calendar** | Competing or complementary attractions nearby | Manual, periodic | Omitted from the forecast |
| **Public transport status** | Disruption on routes serving the estate | Real time where available | Omitted, degrades forecast slightly |

## Why an on site weather station

A forecast for the nearest city is not the weather at the estate, and for animal
welfare the difference matters more than for attendance. Terrestrial enclosure
conditions are evaluated against actual local temperature and humidity, not
against a regional forecast.

It is also cheap, it works during a network partition, and it gives a ground
truth against which to score the forecast provider.

## School holidays deserve more respect than they get

German school holidays are staggered by Bundesland, deliberately, to spread
holiday traffic. For a Bavarian estate near other states, attendance is driven
by **Bavarian term dates and by those of neighbouring states whose families
travel**.

This is a published dataset, stable a year ahead, and it probably explains more
seasonal variation than any model could learn from two seasons of the estate's
own history. It goes into the heuristic baseline in phase 1, before any model
exists.

## How they enter the system

External data is **data, never instruction.** It arrives as typed values into a
template, never as prose concatenated into a prompt.

That is stated in the [AI threat model](../10-security/10_2-ai-specific-threats.md)
as the control against indirect prompt injection. A weather feed is not an
attacker, but a compromised or malformed one should not be able to become one.

| Property | Treatment |
|---|---|
| Freshness | Each source has a liveness check. Stale data is flagged, not silently used |
| Bounds | Values outside plausible ranges are rejected rather than forwarded |
| Attribution | Every forecast records which external inputs it used, and their timestamps |
| Availability | No forecast depends on any single external source being present |

## The cost

Effectively nothing. Weather APIs at this volume are inexpensive, the holiday
calendar is a published file, and a weather station is a few hundred euros of
capital.

This is the highest ratio of forecast improvement to euro spent anywhere in the
architecture, which is why it is in phase 1 alongside the heuristic baseline
rather than waiting for the models in phase 2.
