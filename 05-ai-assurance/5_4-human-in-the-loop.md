# Human in the loop

*Where a person sits between the model and the consequence, and what that
actually requires beyond saying the words.*

## The phrase is doing a lot of work

"Human in the loop" is the most over-claimed phrase in AI architecture. It
usually means a person can theoretically see the output. That is not a loop,
that is a window.

A real loop requires four things, and we hold every Tier 1 capability to all
four:

1. The human sees the output **before** the consequence, not after
2. The human has enough context to disagree, including what the model saw
3. Disagreement is **as easy** as agreement, not a form to fill in
4. Disagreement is **recorded and counted**, because an unmeasured override rate
   means nobody knows whether the loop is real

The fourth is the one that separates a designed loop from a claimed one.

## Where humans sit

| Capability | Human | What they see | What they decide |
|---|---|---|---|
| Animal welfare alert | Keeper, then veterinarian for anything clinical | The alert, the readings behind it, the recent trend, what normal looks like for that animal | Whether to inspect, treat, or dismiss. The register records their decision, not the model's |
| Notifiable disease indication | Veterinarian only | Same, plus the specific indicators triggering the classification | Whether to notify the authority. **The system never notifies** |
| Staff deployment | Zone manager | Aggregate zone demand forecast and current occupancy | Who works where. The system suggests, a person assigns |
| Predictive maintenance | Maintenance lead | Condition trend and predicted lead time | Whether to bring work forward. Statutory inspection is unaffected |
| Piranha population | Aquatic keeper | Estimate, interval, trend, date of last physical count | Whether to physically verify |
| Concierge safety topics | Pre-authored by keepers and vets | n/a, the content is written in advance | Humans wrote the answer before the visitor asked |

That last row is a different shape of loop and worth noticing. For the highest
consequence questions we do not put a human after the model, we put a human
**before** it. The answer is written, reviewed, and then read aloud. The model
is a delivery mechanism, not an author.

## What the human sees

Presenting a bare alert makes disagreement hard, because the human has nothing
to disagree with. Every Tier 1 output carries:

- The recommendation and the model's confidence
- **The evidence**: which readings, over what window, against what normal
- What the heuristic baseline says, when it differs
- Recent similar cases and what was decided then

The baseline comparison is unusual and we think it is important. When model and
rules disagree, that disagreement is information the human should have, not a
detail to hide behind a single confident number.

## Making disagreement easy

Dismissing an alert takes one action and an optional reason from a short list.
It does not require a free text justification, a manager, or a ticket.

This is a deliberate inversion of the usual instinct, which is to make overrides
hard so people do not casually ignore the clever system. Making overrides hard
does not produce better decisions. It produces silent compliance, which destroys
the only signal telling us whether the model deserves to be there.

## Counting overrides

Every override is recorded with capability, model version, what was recommended,
what was decided, and the optional reason.

| Override rate | What it means | Response |
|---|---|---|
| Above 20 percent | The model is not helping | Model review (FF-30) |
| 5 to 20 percent | Healthy. Humans are engaged and the model is usually right | None |
| Near zero on an advisory capability | **The loop is not real.** People are rubber-stamping | Investigate. This is a finding, not a success |

A near-zero override rate being treated as a problem is the part most teams get
backwards. For staff deployment in particular, total compliance would mean the
human is not exercising judgment, and human judgment is the entire legal basis
for the capability under both the works council agreement and the AI Act's
requirements for employment-related systems.

## What the human cannot do

The loop is not unlimited. Two constraints run the other way.

**A human cannot override into illegality.** A staff deployment override that
breaches rest periods is rejected by rules outside the model, because working
time law is not a judgment call.

**A human cannot promote a model output into the statutory register.** The
animal register records what a qualified person observed and decided. It may
record that a model flagged something first. It may not record a model's
conclusion as an observation.

## Staffing reality

All of this assumes humans are available. For a two to three person technical
team and a working estate, that assumption needs stating.

Welfare alerts go to keepers who are on site during opening hours, and the
out-of-hours path is the existing duty rota, not a new obligation. Anything
requiring a veterinarian is already a call-out procedure that exists today. We
have added a signal, not a shift pattern, and an architecture that quietly
assumed new night staff would be an architecture the Countess cannot afford.
