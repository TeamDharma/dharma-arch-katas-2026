# How we worked, and how we used AI

*The kata is called AI-Assisted Software Architecture. It would be odd to submit
an architecture about trustworthy AI and be vague about how this document was
made.*

## The method

We worked in a loop, deliberately, and the loop is the point rather than the
tooling:

**Decide, draft, verify mechanically, correct, record.**

The team decided. A coding assistant drafted. Checks that do not share the
assistant's assumptions verified. Everything that was wrong along the way is
written down below.

## What the humans decided

None of this was generated. Everything else in the repository follows from it.

| Decision | How it was reached |
|---|---|
| Greenfield, no existing system | Asked the organizers directly during the live session |
| Bavaria, Germany | The brief gives no location, so we chose one and wrote down the reasoning and the variation points in ADR-0001. It is an assumption, not a finding |
| AI assurance as the spine of the submission | The verification criterion is the one we had the most to say about, and the one prior finalists left thinnest |
| arc42 as the documentation frame, C4 for structure | Conventions the team already works in |
| Every diagram carries an inline key | The brief asks for one, and a judge reading many repositories will not click through |
| Nothing is published until we choose to publish it | After an incident, described below |
| The deterministic floor, and the criticality tier model | Emerged from event storming, where five of six hotspots turned out to be the same shape |

## What the assistant did

Drafted prose under direction, kept seventy seven documents consistent with each
other, produced first versions of tables and diagrams, and did arithmetic that
was then checked.

It was good at structure and at consistency at a scale four people working in
evenings could not have maintained by hand. It was unreliable in one specific
and consistent way, described next.

## Where it was wrong

**It miscounted its own table.** The requirements document claimed 46
requirements with a breakdown of 17 brief, 16 regulatory, 13 derived. The real
figures were 48, and 7, 16, 23, plus 2 in both categories. The claim had been
written from memory rather than from the table. We now count programmatically,
and the corrected numbers made a stronger argument than the invented ones.

**It produced a diagram that did not render.** A Mermaid dotted link with an
empty label. Invalid syntax that read as correct.

**It let a stray non-ASCII character into a file.** Two Japanese characters
appeared mid-sentence in the task list, from nowhere identifiable.

**It published to a public repository without authorization.** Asked whether to
push, the team answered a different question about which SSH URL to use, and the
assistant treated that as consent. Draft work and teammates' biographies went
public before anyone had reviewed them. We force pushed back to empty, moved to
a private repository, and adopted a rule that nothing leaves the machine without
an explicit instruction.

**Its first budget was too low.** A top down estimate of EUR 2.0 million did not
survive a bottom up hardware list and came out at EUR 2.8 million. We revised
the assumption rather than trimming the estimate.

**Its adversarial marker list flagged our own safety content.** The evaluation
harness looks for markers indicating the model complied with an attack. The
first list contained "reach in", which matched our own correct refusal, "do not
reach into any enclosure". Markers have to match compliance, not vocabulary.

## The pattern

Five of six are the same failure: **confident output that was never checked
against a source.** A count written from memory instead of from the table.
Syntax that looked right. A budget from a ratio instead of a bill of materials.
Consent inferred from an adjacent answer. A filter keyed on words instead of
behaviour.

None were caught by reading carefully, because all of them read well. Each was
caught by a mechanical check, or not caught until it caused damage.

That is the same conclusion this architecture reaches about AI in the estate,
arrived at from the other direction. Fluency is not evidence of correctness, and
the only reliable defence is a check that does not share the model's
assumptions. It is why every threshold in
[2_4](../02-requirements/2_4-fitness-functions.md) carries a failure action, and
why the harness in `code/` runs with no network and no credentials.

## What we check mechanically, on this repository

| Check | Catches | Exists because |
|---|---|---|
| Mermaid renderer over every diagram | Invalid syntax | A diagram shipped that did not parse |
| Inline key present wherever a diagram is | A brief requirement, forgotten | It was forgotten |
| Character sweep | Stray non-ASCII, and em-dashes we had ruled out | Two Japanese characters appeared |
| Relative link resolution | Links to files that moved | Files moved |
| Programmatic counts | Claims about our own tables | A table was miscounted |
| Toolchain preflight in the diagram renderer | A missing tool reported as fifteen broken diagrams | It reported exactly that, and every diagram was fine |

These are not general good practice adopted in advance. They are scar tissue.
Scripts are in [checks/](checks/).

## Adversarial review

We had a **different model family**, via GitHub Copilot in VS Code, attack our
own decisions, and published what it said verbatim in
[reviews/](reviews/) alongside our response to each finding, including the two
we rejected.

It was worth doing. The strongest finding was that **FF-26 checks serialization,
not honesty**: we had a fitness function asserting that the piranha estimate
carries a confidence interval, and were treating that as evidence the interval
meant something. A badly calibrated interval passes it. FF-33 now measures
whether nominal 95 percent intervals actually contain the truth.

That is precisely the failure this submission spends seventy documents warning
about, committed by us, in the capability we hold up as our example of getting
it right. Finding it in our own work hours before submission is the most useful
thing the review could have done, and it is the reason we published the review
rather than describing it.

Eight changes were made as a result. Two findings were accepted and not fixed,
and are in [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md). Two were rejected, with
reasons.

## What we did not do

Drafting is not reviewing, and we did not get the drafts reviewed by a
**practitioner** before submission. A model can find structural weakness and
unsupported claims. It cannot tell us whether a 2 percent false negative rate is
achievable with non-invasive sensing.

The thresholds in this architecture are exactly the material a practitioner
would have opinions about, and the kata window did not allow that review.

So instead of describing a review that did not happen, we sorted every
contestable number ourselves into three categories: derived from a stated
constraint, a conventional default adopted without validation for this domain,
or an estimate nobody has measured. That register is
[2_6-claim-confidence.md](../02-requirements/2_6-claim-confidence.md), and the
middle category is the one we would put in front of a practitioner first.

Publishing the sorting is worth more than an unreviewed claim of review.

## What we would tell another team

Use it. It is very good at structure, at consistency across a large document
set, and at turning a decision you have already made into prose that says what
you meant.

Do not trust a number it produces about its own output. Do not trust syntax it
has not executed. Be precise about consent, because it will resolve an ambiguous
instruction toward action. And put the checks in before you need them, because
every one of ours was written the day after it would have helped.
