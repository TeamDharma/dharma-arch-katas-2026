# ADR-0001: Jurisdiction and regulatory baseline

## Status

**Accepted as a planning assumption.** Not a settled fact.

This becomes a decision when the physical location and operating entity are
confirmed. Until then it is the assumption the rest of the architecture is built
against, and adversarial review was right that labelling an acknowledged coin
toss "Accepted" launders a missing fact into certainty.

Owner: Kirtimaan Lodha. Confirmation blocked on information no one in this kata
can obtain, since the brief states no location and there is no client to ask.

## Context

The brief gives the Von Digitalis Estates no location. During the live kata
session the organizers confirmed there is no existing system and no inherited
technical constraint, so this is greenfield in every respect.

We could have left the location unstated. We decided not to, because the
requirements in the brief are not jurisdiction neutral. Ticketing touches
fiscal law. Animal monitoring touches zoo licensing and animal health
reporting. Counting visitors with cameras touches data protection. Knowing
where to deploy staff touches employment law. In each case the answer changes
depending on where the estate sits, and an architecture that ignores this is
answering an easier question than the one we were asked.

Two signals in the brief point the same way:

1. "Von Digitalis" uses `von`, the German nobiliary particle, also used in
   Austria and historically in Sweden and among the Baltic German nobility.
   This indicates German-speaking ownership. It does **not** establish where
   the estate stands, and an earlier draft of this ADR wrongly claimed it ruled
   out France. A German-named owner can own a French estate.
2. The deck uses Neuschwanstein Castle on both the cover and the slide that
   opens the problem, attributed CC BY-SA 3.0 de. Neuschwanstein is in Bavaria.

Alternatives we considered:

- **Austria.** Equally consistent with `von`. It has a simpler regulator map
  (one national data protection authority, federal heritage law) and a stricter
  employee monitoring regime under ArbVG section 96, where a works agreement is
  mandatory rather than merely co-determined. We preferred it briefly for the
  smaller number of authorities to explain.
- **United Kingdom.** The judges are UK based, and the Zoo Licensing Act 1981
  gives a clean animal records story. We set it aside because the brief's own
  imagery is Bavarian, which is the only signal here with any bearing on
  location. A surname says nothing about where an estate stands, in the UK or
  anywhere else.

Germany and Austria were both defensible and we had to pick one. Naming BayLDA,
the Bavarian supervisory authority for private bodies, gave the same economy of
explanation that had made Austria attractive, which removed our only substantive
reason to prefer it. At that point the choice was a coin toss and we took
Germany.

An earlier draft justified the choice on the grounds that Germany's constraints
"do more architectural work". That reverses the causality and we have removed
it. Applicable law constrains an architecture. An architect does not select the
applicable law because it makes the design more interesting to present.

## Decision

We assume the Von Digitalis Estates are in **Bavaria, Germany**, and we design
against German federal law, Bavarian state law, and directly applicable EU law.

We do not assume the estate is Neuschwanstein. That building is 19th century
Romanesque Revival and is state owned, while the brief describes 18th century
rides on a private family estate. The imagery fixes the setting and nothing
more.

## Variation points if the estate is not in Bavaria

Because this is an assumption rather than a fact, it is worth stating what
actually moves. Adversarial review raised this and it was a fair point.

| Layer | Portable | Changes with jurisdiction |
|---|---|---|
| Zone model, deterministic floor, tier model, assurance plane | Yes, entirely | |
| GDPR, EU AI Act, EU Zoos Directive, European Accessibility Act | Yes, EU-wide | |
| Fiscal point of sale mechanism | | KassenSichV/TSE in Germany, RKSV signature card in Austria, different again outside the EU |
| Records retention period | | 10 years Germany, 7 Austria |
| Children's consent age | | 16 Germany, 14 Austria, 13 elsewhere in the EU |
| Employee monitoring | | BetrVG section 87 Germany, ArbVG section 96 Austria which is stricter |
| Heritage protection | | State-level in Germany, federal in Austria |
| Supervisory authority | | BayLDA, or a single national authority in Austria |

**A bounded claim, replacing an overclaim.** An earlier version of this section
said "nothing in the architecture changes", which was contradicted by the table
directly above it and by this ADR's own consequences. Sorted properly:

| Level | Austria | Outside the EU |
|---|---|---|
| Zone model, tier model, deterministic floor, assurance plane | Unchanged | Unchanged |
| Configuration: retention period, consent age | Parameter change | Parameter change |
| **Integration: fiscal device** | **Adapter replacement.** RKSV signature card is not a TSE | Unknown, likely larger |
| **Physical: sensor placement under heritage rules** | Possible topology change if permissible mounting differs | Possible |
| **Workflow: co-determination** | Austrian ArbVG section 96 is stricter, so our aggregate-only design still passes. A weaker regime would permit a design we decline anyway | Varies |
| EU-wide obligations: GDPR, AI Act, Zoos Directive, Accessibility Act | Unchanged | **Substantially replaced, but not simply absent.** GDPR and the AI Act both reach organizations outside the EU that target people inside it, so an estate selling tickets to EU visitors would remain partly in scope. We have not analyzed this and would not guess at it |

So: moving to Austria is adapter replacement plus configuration. Moving outside
the EU is a different exercise and we have not costed it. The UK was considered
and set aside, and post-Brexit it now sits in the second column.

We have not estimated the cost or elapsed time of a jurisdiction change, which
adversarial review asked for. For a fictional estate we judged that
disproportionate, and we would do it for a real one.

The one genuinely structural dependency is that our staff analytics design is
aggregate-only, which satisfies both German and Austrian co-determination law.
A jurisdiction with weaker employee protection would permit a richer design we
have declined anyway.

## Consequences

- Fixes one data protection authority (BayLDA), one heritage regime
  (BayDSchG), and one building code (BayBO), so the regulatory narrative stays
  short.
- Produces constraints that do real work rather than sitting in an appendix.
  BetrVG section 87(1)(6) shapes footfall analytics. BayDSchG rules out
  invasive sensor mounting on protected ride structures. BNatSchG section 42
  makes the animal register a legal record. KassenSichV constrains the offline
  behavior of every point of sale.
- The EU AI Act applies directly, which sets hard limits on some designs we
  might otherwise have reached for, including emotion recognition on staff.
- Ten year retention under GoBD and the Abgabenordnung conflicts with GDPR
  minimization. We have to resolve this rather than assert both.
- Choosing 16 as the age of consent complicates the family pass flow relative
  to jurisdictions that elected 13 or 14.
- Rules on keeping dangerous and venomous animals sit with the Länder and vary.
  We have logged this as an open item rather than guessing.
- We are now committed to Bavaria across every document. Changing it later
  would ripple through the regulatory register, several ADRs, and the cost
  model.

## Verification

This decision is verified by review rather than by a runtime metric. Each
regulatory claim in `01-problem/1_4-regulatory-context.md` names the regime and
the constraint it imposes, and every constraint is traceable to at least one
requirement or ADR. If a constraint appears in the register but shapes nothing,
it is decoration and we remove it.

We write at architecture kata fidelity. We name the regime and derive the
constraint. We do not claim verified legal positions, and anything we could not
confirm is listed in OPEN-QUESTIONS.md. Every regulatory claim in this
repository is a hypothesis that would require qualified legal confirmation
before implementation.

Adversarial review of this ADR, and our response, is in
[../09-ai-disclosure/reviews/findings.md](../09-ai-disclosure/reviews/findings.md).
