# Open questions

Things we could not settle inside the kata window. Listed here rather than
papered over, because a reader deserves to know where the architecture is
resting on an assumption we did not get to test.

## Regulatory

- **Dangerous and venomous animal keeping is regulated at Länder level in
  Germany and the rules vary.** We assumed Bavaria in ADR-0001 but did not
  confirm what Bavaria specifically requires for venomous species, escape
  notification, or antivenom provisioning. This affects the incident scenarios
  in `10-security/`.
- **VAT treatment of a combined ticket.** Zoo admission and amusement rides
  attract different rates in Germany. We assumed the family pass must apportion
  revenue across both, but we did not confirm the rates or whether a bundled
  leisure ticket is treated as a single supply.
- Whether the estate is large enough to trigger a mandatory works council in
  the first place. Our staff analytics design assumes one exists. If it does
  not, the constraint becomes individual employee consent, which is weaker but
  messier.

## Architecture

- We have not decided between LoRaWAN, private 5G, and a mesh WiFi backhaul for
  the parts of the estate with no coverage. The cost model currently carries a
  placeholder. This is the single biggest open number in `06-economics/`.
- Whether the animal register should be the system of record inside our
  platform or whether we should integrate an existing zoological records system
  such as ZIMS. Buying would cut scope and match the two person operations
  constraint, but we did not get far enough into the integration surface to
  commit.

## Tensions we recorded rather than resolved

- **Per visitor location tracking through a wristband, for the separated child
  case.** The case for it is concrete: a lost child is a real harm, and journey
  analytics would be a real benefit. The case against is that processing
  children's location data continuously, to handle an infrequent event that
  staff and signage already cover, is the wrong trade, and that most of the
  benefit is available from anonymous zone counting anyway. We never settled
  this. The documents describe the conservative option because it is the one
  everything else assumes, and no ADR yet decides it.

## Numbers we could not validate

Thirteen thresholds in this architecture are conventional defaults adopted from
practice elsewhere and never validated for this domain. They are listed, with
our reason for doubting each, in
[2_6-claim-confidence.md](02-requirements/2_6-claim-confidence.md).

We flag them together rather than individually because the risk is cumulative.
Any one plausible default is fine. A set of them, each presented beside a
fitness function, acquires an authority none of them has earned.

## Raised by adversarial review, accepted, not fixed

Both from the piranha capability. See
[09-ai-disclosure/reviews/findings.md](09-ai-disclosure/reviews/findings.md).

- **The physical count trigger should be derived from decision loss, not from a
  percentage.** Width above 0.15 of the estimate is a plausible number with
  nothing behind it. The right version asks what the smallest population change
  requiring action is, and triggers when the interval can no longer resolve it.
- **Physical counts are treated as ground truth without their own error rate.**
  Counting fish by hand is not exact either. A rigorous design states the
  counting procedure, its error, and how a disagreement between count and model
  is adjudicated.

We accepted both and ran out of kata window. They are the first things we would
fix.
