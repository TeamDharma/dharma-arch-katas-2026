# Assumptions and constraints

The organizers confirmed during the live session that no existing system
exists. This is greenfield, with no inherited technology and no stated budget,
timeline, team, or location. Everything in this file is therefore a choice we
made, not a fact we were given. We state them here so that every later decision
can be read against them, and so a reader who disagrees with an assumption can
see exactly which parts of the architecture it holds up.

## A1. Location

Bavaria, Germany. Reasoning and alternatives are in
[ADR-0001](../07-decisions/ADR-0001-jurisdiction-and-regulatory-baseline.md).
The regulatory consequences are in
[1_4-regulatory-context.md](1_4-regulatory-context.md).

## A2. Scale and revenue

We derive these rather than assert them, because the budget depends on them.

| Input | Value | Basis |
|---|---|---|
| Visitors per day, today | 5,000 | Given in the brief |
| Operating days per year | 250 | Seasonal outdoor attraction, closed midwinter |
| Visitors per year, today | 1.25 million | 5,000 x 250 |
| Yield per visitor | EUR 40 | Admission plus food, beverage, and retail |
| Revenue per year, today | about EUR 50 million | 1.25M x 40 |

At the three year target of 15,000 visitors per day the same arithmetic gives
3.75 million visitors and roughly EUR 150 million, before any change in yield.

## A3. Budget

*Revised after costing the build bottom up. The original top down figure of
EUR 2.0 million did not survive contact with a hardware list, which is recorded
in [6_1](../06-economics/6_1-cost-model.md) rather than quietly corrected.*

| Line | Value | Basis |
|---|---|---|
| Capital budget | **EUR 2.8 million over 18 months** | Bottom up build, see [6_1](../06-economics/6_1-cost-model.md). Revised upward from an initial top down estimate of EUR 2.0 million |
| Operating budget | EUR 495,000 per year today, **EUR 975,000 at target scale** | Operating cost is not flat. It scales with visitors because inference does. See [6_1](../06-economics/6_1-cost-model.md) |
| AI inference ceiling | **EUR 0.10 per scanned admission** | 0.25 percent of assumed yield, a policy choice, see A4 |

## A4. The AI spend ceiling

We cap metered inference at EUR 0.10 per scanned admission, which is 0.25
percent of the assumed EUR 40 yield. At the 15,000 per day target that is
EUR 1,500 per day and about EUR 375,000 per year.

This is deliberately a hard constraint and not a forecast. It forces small
models, inference at the edge, aggressive caching, and routing cheap requests
away from expensive models. It also requires a runtime budget guard that
degrades AI features when the ceiling is approached, which is a component in
the architecture rather than a line in a spreadsheet.

The number is generous enough to be achievable, which is the point. A ceiling
nobody can hit is theater.

## A5. Timeline

The Countess has three years. We phase against that.

| Phase | Window | What ships |
|---|---|---|
| 0 | 0 to 6 months | Months 0 to 2: site survey, backhaul decision, ticketing vendor selection, heritage permissions. Months 2 to 6: ticketing, payments, admission, connectivity backbone. No AI in the path. |
| 1 | 6 to 12 months | Telemetry, animal welfare monitoring, footfall sensing, the data platform |
| 2 | 12 to 18 months | AI capabilities: visitor experience, operations support, forecasting, each as it beats its baseline |
| 3 | 18 to 36 months | Scale to 15,000 per day, optimize, extend. A capability that misses its phase 2 gate lands here |

Phase 0 carries no AI on purpose. The estate has to be able to sell a ticket
and admit a visitor before it does anything clever. Three months would not be
achievable from a standing start with a site survey still to run, a vendor to
select and heritage permissions to obtain, so phase 0 is six. The estate
continues on its present manual arrangements until then.

## A6. Team

| | Assumption | Consequence |
|---|---|---|
| Build | 8 engineers, 1 architect, product and design, for 18 months | Fits the capital budget |
| Run | **2 to 3 technical staff, permanently** | This is the important one |

A country estate will not staff a platform team. Everything we design has to be
operable by two or three people who also have other jobs. That promotes
operability into a top tier architectural characteristic and biases nearly
every decision toward managed services over anything we would have to run
ourselves. It is also the strongest single argument for the things we chose not
to build.

## A7. Data

**There is no historical data.** Greenfield means the estate has never
instrumented anything. On opening day there is no attendance history, no
feeding records in machine readable form, and no labeled images of animals.

Every demand forecast, every anomaly detector, and every recommendation has a
cold start problem. We treat this as a first class design concern rather than
assuming a training set into existence. See
[5_6-cold-start-strategy.md](../05-ai-assurance/5_6-cold-start-strategy.md).

## A8. Physical constraints carried over from the brief

- WiFi coverage is patchy and we cannot assume it improves.
- MQTT capable hardware can be installed throughout the park, and there is
  budget for it.
- The rides are 18th century and very likely protected structures, so sensing
  attached to them must be non invasive, battery powered, and removable.

## What we are explicitly not assuming

- That the estate has any existing IT, staff with technical skills, or vendor
  relationships.
- That connectivity will be fixed by someone else before we go live.
- That visitors will download an app. Anything that requires one has to work
  without it as well.
- That the animal collection is uniform. Aquatic and terrestrial species need
  different sensing, and we design them separately.
