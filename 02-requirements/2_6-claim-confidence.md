# Claim confidence

*Which numbers in this repository are derived, which are conventional defaults
we adopted, and which are estimates nobody has measured.*

## Why this page exists

This architecture is full of thresholds. A drift alarm at 0.2. A false negative
rate under 2 percent. A golden set of 300. Ninety day log retention. Forty euros
of yield per visitor.

Written in a table with a fitness function beside it, every one of those looks
equally authoritative. They are not. Some are derived from a constraint we
stated, some are conventions borrowed from practice elsewhere, and some are
guesses that phase 1 exists to replace.

Treating them as equally solid would be the same mistake this submission argues
against everywhere else: fluent presentation is not evidence.

So they are sorted here, and the sorting is the useful part.

## A. Derived

Traceable to a stated constraint, with the arithmetic visible. Challenge the
input and the output moves predictably.

| Claim | Where | Derived from |
|---|---|---|
| EUR 2.8 million capital | 6_1 | Bottom up parts list and team cost. Replaced our own top down estimate of EUR 2.0 million, which was wrong |
| Operating cost EUR 495,000 today, EUR 975,000 at target | 6_1 | Line by line, and it scales with visitors because inference does |
| 20 admissions per minute per lane | NFR-06 | 3,000 arrivals per hour across twelve lanes, sized with margin for bursts and lane closures |
| 24 hour local buffer | NFR-10 | Chosen against the stated four hour partition target, with headroom |
| Six systems, six operational hours per week | FF-06, FF-07 | Set as a budget from the two to three person constraint, then the weekly breakdown was written out to check it fits |

## B. Conventional defaults, adopted and not validated for this domain

**This is the category that deserves the most suspicion**, and the one most
likely to go unexamined, because a conventional number looks like a researched
number.

Each of these is a reasonable value drawn from practice elsewhere. None has been
validated against a Bavarian estate with 55 enclosures, an unreliable network,
and no historical data.

| Claim | Where | Why we are unsure |
|---|---|---|
| AI inference ceiling EUR 0.10 per scanned admission | A4, 6_2, ADR-0014 | The arithmetic is derived, the input is not. It is 0.25 percent of an assumed yield, a policy choice checked against three routing scenarios. The share of operating cost it implies is a consequence, and would be circular as a source |
| Drift alarm at population stability index above 0.2 | FF-31 | A common bar in credit scoring. Possibly too coarse for per-species welfare, where a single enclosure change matters |
| 95 percent concierge correctness | FF-21 | Feels right. No basis for why not 90 or 98 |
| Override rate above 20 percent triggers model review | FF-30 | Invented. The threshold matters less than measuring it at all, but the number will be quoted as though it means something |
| Model must beat baseline by 10 percent MAPE over 8 weeks | FF-28 | Both margin and window are plausible and arbitrary |
| False negative rate under 2 percent on welfare | FF-24, FF-25 | Asymmetric error reasoning is sound. This specific rate may be unachievable with non-invasive sensing |
| No species above 5 percent false negative | FF-25 | The construction is right, a per-class bar alongside an aggregate. The value is a guess |
| Golden set of 300 questions, 60 safety | 5_2 | Sized to what four people could review properly, not to what statistical coverage requires |
| Word error rate injection at 10 percent | FF-23 | Plausible for a noisy park. Not measured in one |
| Interval width above 15 percent triggers physical verification | FF-27 | The mechanism matters more than the threshold. The threshold is still a guess |
| Model log retention of 90 days | 5_3, 3_12 | A judgment between evaluation corpus size and data minimization, not a derivation |
| Under 1.5s to first audio at p95 | NFR-07 | Conversational tolerance is real. This number is from general voice experience, not from this pipeline |
| Eight adversarial attack classes | code/ | A starting suite. Real coverage comes from production attempts |
| Two day provider substitution | NFR-34 | Stated as an intent with a rehearsal attached, and never rehearsed, because nothing is built |

## C. Estimates awaiting measurement

Nobody knows these. The estate has never been instrumented, which is the point
of phase 1.

| Claim | Where | When it becomes knowable |
|---|---|---|
| EUR 40 yield per visitor | A2 | Phase 1. **The business case rests on this** |
| 250 operating days per year | A2 | Immediately, from the estate |
| 40 percent of arrivals in a two hour peak | NFR-06 | Phase 1 |
| EUR 250,000 connectivity | 6_1, ADR-0013 | Site survey. Largest single uncertainty in the cost model |
| 11 people at EUR 85,000 fully loaded | 6_1 | Depends on a delivery model not yet chosen |
| Estate payroll near EUR 6 million | 6_3 | From the estate's own accounts |
| 5 percent staff efficiency improvement | 6_3 | Phase 2, and it may be smaller |
| EUR 1 per visitor yield improvement | 6_3 | Phase 2. Carries the business case and is the least evidenced number in it |

## What we did not do

We did not have these reviewed by a practitioner before submission.

The category B thresholds are exactly the material a practitioner would have
opinions about, and the kata window did not allow that review. Rather than
describe a review process that did not happen, we sorted the claims ourselves
and published the sorting.

If you are reading this as a judge and category B looks thin, that is a fair
reading and it is why the category exists.

## How a reader should use this

**Category A** can be argued with on its inputs. Disagree with EUR 40 yield and
the whole cost model moves in a way you can follow.

**Category B** should be read as "this is the shape of the check, and the number
is provisional." The architecture's claim is that these checks exist, are
automated, and have failure actions. It is not a claim that 0.2 is the correct
drift bar for piranha enclosures.

**Category C** is why phase 1 measures before phase 2 models. The estate
currently cannot tell whether it is succeeding, and three of its six baselines
are unknown. Every number here is a reason that ordering is right.

## The thing we would fix first with more time

The category B thresholds, in one sitting, with a practitioner. Not because any
individual number is likely to be badly wrong, but because a set of plausible
defaults presented with fitness functions beside them acquires an authority none
of them has earned, and that is precisely the failure this submission spends
seventy documents warning about.
