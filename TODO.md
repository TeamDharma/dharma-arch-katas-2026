# TODO

Working task list for the kata. Checked items are done and committed.

Deadline: submission by **Wednesday evening IST, September 16**. The hard
organizer deadline is 9:29am IST Thursday September 17, kept as insurance only.

Owners follow the allocation in [TEAM.md](TEAM.md). Anyone can pick up an
unclaimed item, just put your initials next to it.

## Foundation

- [x] Repository structure and conventions
- [x] README with positioning, reading paths, criteria traceability, arc42 map
- [x] TEAM.md with all four members and draft ownership
- [x] OPEN-QUESTIONS.md, .gitignore
- [x] ADR template with a mandatory Verification section
- [x] ADR-0001 Jurisdiction and regulatory baseline
- [x] GLOSSARY.md

## 01 Problem

- [x] 1_0 Problem statement
- [x] 1_3 Assumptions and constraints, with derived budget and the EUR 0.10 ceiling
- [x] 1_1 Business goals and challenges, with measurable targets
- [x] 1_2 Stakeholders, with leverage and the three veto holders
- [x] 1_4 Regulatory context, the Bavaria register

## 02 Requirements

- [x] 2_1 Functional requirements, 48 with provenance and verification columns
- [x] 2_2 Non functional requirements, 37 tied to characteristics
- [x] 2_3 Architecture characteristics and the AI criticality tier model
- [x] 2_4 Fitness functions, 31 platform and AI checks, three added after the adversarial review and one after the flow-tracing pass
- [x] 2_5 Quality scenarios in ATAM form, 14 scenarios plus sensitivity points, tradeoff points, risks and non-risks

## 03 Architecture

- [x] 3_0 Solution strategy, arc42 section 4, with validated diagram
- [x] 3_1 System context, C1
- [x] 3_2 Container view, C2
- [x] 3_3 Domain model with bounded contexts
- [x] 3_4 Event storming, with hotspots
- [x] 3_5 Connectivity and edge
- [x] 3_6 Deployment view
- [x] 3_7 Identity and access
- [x] 3_8 Degraded mode matrix, with cost degradation ordering
- [x] 3_9 External data sources
- [x] 3_10 Diagram legend, with the inline key rule enforced by the checker
- [x] 3_11 Data architecture
- [x] 3_12 Data governance and retention
- [x] 3_13 Animal register as master data
- [x] 3_14 Reference technology choices, one defensible instance per component

## 04 AI scenarios

One folder each, following a single template: purpose, tier, inputs, approach,
fallback, verification, diagram. Three are written deeply, five to the template.

- [x] visitor-experience, the voice concierge. **Deep**
- [x] animal-welfare-aquatic. **Deep**
- [x] footfall-and-staffing. **Deep**
- [x] animal-welfare-terrestrial
- [x] piranha-population
- [x] predictive-maintenance
- [x] accessibility-and-translation
- [x] ticketing-and-passes, the Tier 0 case where the answer is no AI

## 05 AI assurance

The section we are betting the submission on. Deepest content goes here.

- [x] 5_1 Evaluation strategy
- [x] 5_2 Golden datasets, four sources with honesty about what each is worth
- [x] 5_3 Production monitoring and drift, including provider drift
- [x] 5_4 Human in the loop, four conditions for a real loop
- [x] 5_5 Failure mode taxonomy, per capability with automatic responses
- [x] 5_6 Cold start strategy, heuristics first and permanently
- [x] 5_7 EU AI Act obligations mapped to assurance activities

## 06 Economics

- [x] 6_1 Cost model, bottom up, which revised the budget upward
- [x] 6_2 AI spend ceiling and the runtime budget guard
- [x] 6_3 Business case against the 15,000 visitor target
- [x] 6_4 Build versus buy

## 07 Decisions

Target twelve to fifteen ADRs. At least one refusal, at least one superseded.

- [x] ADR-0001 Jurisdiction and regulatory baseline
- [x] ADR-0002 Zone based edge architecture
- [x] ADR-0003 No AI in the revenue path. **The refusal ADR**
- [x] ADR-0004 Offline verifiable ticket credentials
- [x] ADR-0005 Model gateway as the single provider seam
- [x] ADR-0006 Heuristic baseline retained permanently
- [x] ADR-0007 Text chat concierge, **superseded by ADR-0016**
- [x] ADR-0008 Anonymous edge counting, no biometric identification
- [x] ADR-0009 Aggregate only staff analytics
- [x] ADR-0010 Animal register as system of record, AI advisory only
- [x] ADR-0011 Piranha population reported as an interval, never a count
- [x] ADR-0012 Buy ticketing and point of sale, build the AI
- [x] ADR-0013 Connectivity backhaul, recorded as **Proposed**, deliberately unresolved
- [x] ADR-0014 AI spend ceiling and budget guard
- [x] ADR-0015 Model provider exit strategy
- [x] ADR-0016 Voice first concierge, supersedes ADR-0007

## 08 Risks and uncertainty

- [x] 8_1 AI provider uncertainty, model churn, price change, shutdown
- [x] 8_2 Risk register
- [x] 8_3 Phased roadmap, zero to thirty six months

## 09 AI disclosure

- [x] How we used AI to produce this submission, framed around the method
- [x] Where AI was wrong and we overrode it, six documented errors
- [x] checks/ with three runnable suites, 19 checks, no dependencies
- [x] Architecture consistency checks, which found two real inconsistencies
- [x] Claim confidence register, replacing a review process the window did not allow

Optional, only if someone finds an hour:

- [ ] A practitioner pass over the category B thresholds in `2_6-claim-confidence.md`.
      Edit the numbers in place. Nothing else needs to change
- [x] Adversarial AI review of the ADRs, run in VS Code Copilot against a
      different model family, published verbatim with our response to each finding

## 10 Security

- [x] 10_1 Threat model
- [x] 10_2 AI specific threats, prompt injection on the public concierge
- [x] 10_3 Incident scenarios, animal escape, medical, separated child

## code/

- [x] Evaluation harness, offline, stdlib only, 7 checks, exits non-zero on failure
- [x] Golden dataset sample, 12 concierge questions with 4 safety classified
- [x] Adversarial suite sample, 8 attack classes

## video/

Only needed if we are named a semifinalist on October 5. Video is due October 12.

- [x] narrative.md, drafted as a five minute structure

---

## Rolling checks before publishing

*Deliberately left unticked. These are recurring, not one-off. Last full run:
2026-09-17, all clean across 84 markdown files.*

- [ ] Run the diagram checker. Every block renders **and** every file holding a
      diagram carries an inline **Key** plus a link to `3_10-diagram-legend.md`.
      The brief asks for a key explicitly, so this is scored, not cosmetic
- [ ] `check-docs.py` and `check-architecture.py` pass
- [ ] Relative links resolve
- [ ] README reading paths still point at files that exist
