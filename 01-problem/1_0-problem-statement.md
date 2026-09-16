# Problem statement

## The situation

After a gardening accident, the 204th in line to the Von Digitalis estates has
become the 72nd Countess Von Digitalis. The estates are large, sprawling, and
unprofitable. The family business, manufacturing highly explosive garden
gnomes, is no longer viable. The Countess wants digital solutions that let her
monetize parts of the estate.

## What there is to monetize

**An amusement park.** Forty rides, an extensive and historically important
collection dating to the 18th century. They recently passed safety inspection,
after the asbestos, broken glass, and garden gnomes were removed.

**An exotic animal collection.** Over 200 animals across 55 displays and
enclosures, a mix of aquatic and land based, some of them poisonous. The
collection was private and is now opening to the public.

**A carnivorous plant collection.** This is not a revenue asset. It is the
stake. If the estate misses its growth target, the family is forced to sell it.

## The numbers in the brief

| | Today | Target |
|---|---|---|
| Visitors per day | 5,000 | 15,000 within three years |
| Rides | 40 | |
| Animals | 200+ | |
| Displays and enclosures | 55 | |

## What the Countess asked for

1. A system that lets people buy tickets, including family passes, to access
   the estates.
2. An understanding of how popular different parts of the park are, so she
   knows where to improve things.
3. Careful monitoring of the animal collection: health, how much and how well
   they are eating, and for the jumping piranhas, population levels.
4. A way to grow visitor numbers and make the estates more profitable.

## The challenges she named herself

- No real idea which parts of the estate are popular, so no basis for deciding
  where to invest or where to put staff.
- Animal care is expensive, and much more so when animals get sick. She wants
  healthy and happy animals.
- She wants more returning visitors and does not know how to get them.

## Technical context

- WiFi coverage across the park is patchy.
- Cloud services are available, but getting information from the estate to the
  cloud is our problem to solve.
- There is budget for MQTT capable hardware installed throughout the park.

## The mandate

The brief asks for a new comprehensive modern architecture for the estates,
with a focus on how AI could solve the Countess's problems. It also asks that
AI enhance the solution for the company **and for the company's customers**.
We read that as two distinct surfaces, operations and visitor experience, and
we design for both. An answer that only instruments the back of house has
answered half the question.

## How we read the brief

Three things in the problem shaped our architecture more than anything else.

The first is that the network is unreliable and the money is not. Ticketing is
the revenue path, and it has to work when the link to the cloud does not. That
gave us the idea of a deterministic floor: a set of capabilities that never
depend on a model or on connectivity, with AI layered above it.

The second is that profitability is the actual goal. "Or it is back to the
garden gnome business" is a real constraint, not a joke. An AI feature that
costs more than it earns fails the brief, so we put a per admission ceiling on
inference spend and treated it as a design input rather than a report we run
later.

The third is that the animal collection is not only an operations problem. Once
the collection is open to the public it sits inside a licensing regime with
statutory record keeping. That changes what AI is allowed to be in this system:
a recommender that a human confirms, never the record itself.
