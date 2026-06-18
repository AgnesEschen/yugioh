# Decision Axes

The framework for evaluating a deck configuration **beyond raw consistency**. Consistency is
necessary but not sufficient: optimizing it alone bloats the deck, because it has no stop
signal (see §1). This file defines the full objective — consistency as a *constraint*, then
**quality / redundancy / direction / coverage** as the things to actually optimize.

Companion files: `glossary.md` (vocabulary, incl. play / line / dig), `probability-toolkit.md`
(methods + reachability), `open-questions.md` (worklog), `end-board-tiers.md` (the tiers a line
targets), `card-reference.md` / `card-schema.md` (card data + the `Functional equivalence` field
this framework relies on).

---

## 1. The objective structure

**Consistency is a constraint, not a maximand.** Hold

    P(functional opener) = P(>=1 play, going first, 5-card hand)  >=  ~90%

as a *floor* (the community competitive threshold; some RT configs fail it, so the floor
discriminates — it carries information). Above the floor, a marginal point of P(F) buys almost
nothing, yet adding a decent card never *costs* P(F) either, so as a maximand it is useless and
slightly perverse.

- **Why maximizing consistency bloats the deck.** Each card's cut value = (intrinsic value) −
  (slot rent ~1.1 pts). Every card whose intrinsic value clears the rent "earns its slot," so
  consistency keeps *adding* engine forever. **Proof:** the consistency-maximizing configuration
  of the contested deck is **41 cards** — cut only the non-engine Shiina, keep the 3rd Pot
  (92.4% > best 40 at 92.2%). Consistency literally rewards going above 40. Hence: constraint.

**Subject to the floor, optimize:**
1. **Hand quality** — distinct plays (§2).
2. minimize **Redundancy** (§3).
3. respect **Direction** — going-first / going-second (§4).
4. **Matchup coverage** — the non-engine suite; on win-rate / playtesting, *not* draw math.

---

## 2. Hand quality — distinct plays

The primitive is not card count, nor consistency, but the number of distinct **plays** in the hand.

### What is a play
A **play** = an independent action that establishes board presence / initiates the combo,
identified by its **outcome, not the card**. Two gates (the "useful filter") — a card contributes
a play iff it passes **both**:
1. **Liveness** — it does something in *this* state (going first, empty board). Fails: dead
   conditionals (lone Ascendance w/o Manifestation; lone Meghala/Krosea w/o enabler),
   wrong-direction cards (a sided going-2nd card held going 1st).
2. **Distinct function** — it adds a *new* outcome, not one already counted.

The mechanism behind gate 2 is **OPT**: a play runs on its card's once-per-turn resource, so a
second copy of the same card — or a functional equivalent (Noble for Eldam; Tenki for Swen) —
cannot run the play again this turn. So **Noble + Eldam = one Eldam-play**: two names, one play.

**Not plays:**
- **Digs** (Pot; Vision's draw mode) are play-*finders*, not plays — a dig raises P(≥1 play) and
  can find more plays, but is not itself a play.
- **Payoffs / components** — Fonix, Varuroon, Mandate, and usually MST: engine, but they don't
  initiate. "Eldam + MST + Mandate" is one play, not three pieces. (MST flips going 2nd — see §4.)

### Plays, lines, and tiers
The **play** and the end-board **tier** (`end-board-tiers.md`) are *abstractions*; the **line**
(combo-line) and the concrete end-board are the *particulars* that connect them. A line is a path
— the sequence of actions executing a play to a board — so "play P reaches tier T" ⟺ a line
exists from P to a board satisfying T (the reachability model, `probability-toolkit.md`).

A play affords a **choice-set of lines**, not one, with different interruption trade-offs (a
draw-phase Krosea line dodges Droll; a bait-first Krosea line eats Droll but dodges other hand
traps). The **optimal line** maximizes reached tier *over the opponent's interruption
distribution*, not against a fixed target.

**Consequence for the metric (important).** Because one play can dodge different interruptions by
choosing the line — yet usually no single line dodges all of them — true resilience is a
**coverage** problem over (interruptions × lines), chosen under a read. The distinct-play count is
therefore a **breadth proxy** for resilience, *agnostic to which interruption* — useful for
opening-hand quality, but it is not the resilience number. Don't over-read small play-count gaps
as resilience verdicts. (True resilience = line-coverage + going-second → deferred, §7.)

### Structure of quality
- **Engine is paramount; ≥1 play is the gate.** You cannot play without it.
- Above the gate:
  - distinct **engine plays** → resilience-breadth (independent routes that survive a point of
    negation) + ceiling. Saturating past ~3-4 (you can only do so much/turn).
  - distinct **non-engine pieces**, on a solid engine core → the **good -> great** step
    (interruption going 1st, board-breaking going 2nd).
- **Stellar hand ~= 3 distinct engine plays + 2 distinct non-engine pieces.**

---

## 3. Redundancy — collapses into "adds no play"

Redundancy = cards held that **add no new distinct play**. The mechanism is OPT: a duplicate (or
functional equivalent) of an OPT-gated card can't run the play again this turn.

- **No same-turn insurance from same-card duplicates.** If your Eldam is interrupted, the shared
  OPT is already spent, so the second Eldam can't pick up the play. Genuine same-turn insurance
  comes *only* from **distinct** plays (independent OPTs — Eldam + Swen). So a duplicate's residual
  value is minor and secondary: **cross-turn** (a play saved for next turn, OPT reset) and
  **non-play utility** (a body for material, fodder to pitch). *(This replaces the old "hard vs
  soft" split — the real axis is just "adds a play or not," with residual value as a footnote.)*
- **The actionable redundancy here is the 3rd Pot** — a duplicate dig that can't fire (the
  draw-lock is the OPT made visible): a dead extra copy in **3.6%** of hands vs **1.3%** at 2x.
- **Digs find plays** (so they lift the whole play distribution — consistency *and* resilience),
  but the draw is OPT-capped at one event/turn, so extra dig copies (the 3rd Pot) are
  **consistency-weighted**: they rescue low-play hands up to ≥1 more than they push good hands higher.
- **Don't** use deck-total duplicate *name* count: near its floor here (~0.35/hand) and it
  undercounts — it misses functional equivalents (Noble+Eldam) and dead conditionals. Redundancy
  is captured by the play-count: redundancy = cards held − (distinct plays + useful non-engine).

---

## 4. Direction — a per-card tag, not a structural axis

Going first, maindeck non-engine is **not dead**. It is either *interruption backup* (Crown,
Droplet, F&V, Shiina — fired on the opponent's turn) or *protection* (Called, TTT — fired during
your turn to push the combo through a hand trap). The only going-1st-dead non-engine is the
*purely going-2nd* set (Mulcharmy, Ra, Lightning Storm) — which is **exactly why those are sided**.
"Dead going first" is a side-deck property, not a maindeck clunk.

Direction is therefore a **per-card tag**:
- **bidirectional** — most maindeck non-engine. *Shiina* is the premium case: near-always-live
  going 1st (you almost always control a WIND monster if you played) and a board-breaker going 2nd.
- **first-skewed** — *Meghala*: strong going 1st, weak going 2nd.
- **second-only** — *Mulcharmy, Ra*: sided.

Engine can be direction-tagged too: **MST** is usually a non-play going 1st but near-essential
going 2nd (MST-in-GY is what lets Eldam/Swen/Meghala self-SS into an opposing board). So "is X a
play" can flip on the die roll.

(Caveat for §2's metrics: the current model is **going-first only**, so it *overvalues*
first-skewed cards like Meghala and *undervalues* premium bidirectional cards like Shiina. A
going-second model is needed to close this — §7.)

---

## 5. Metrics

All play metrics below are **post-dig, going first** (digs resolve first — Vision in the draw
phase, then Pot at MP1-start — then count distinct plays).

| Metric | Definition | Use |
|---|---|---|
| **Consistency (floor)** | P(≥1 play) | Hold ≥ ~90% |
| **Resilience (breadth)** | P(≥2 distinct plays) | ~ survives 1 interruption (breadth proxy — §2) |
| **Good-hand rate** | P(≥3 distinct plays) | engine depth / ceiling |
| **Great-hand rate** | P(≥3 engine plays AND ≥2 distinct non-engine) | the stellar 3+2 |
| **Actionable redundancy** | P(≥2 copies of a no-play duplicate) | in RT: the 3rd Pot |
| **Power-card access** | P(see ≥1 of a key card) | matchup coverage |
| **Premium dilution** | P(open a given 1-of) at deck size N (= 5/N) | cost of going >40 |

**Note — the joint objective.** "Maximize consistency AND minimize redundancy" is *not* a separate
goal: it equals the **distinct-play count** (a play requires presence *and* non-duplication at
once), so the good/great-hand rates score both in one number.

---

## 6. Established results (current deck)

**Consistency landscape** (P(F) with digs):

| Config | Cards | P(F) |
|---|---|---|
| keep all | 42 | 91.4% |
| cut 3rd Shiina only | 41 | **92.4%** (consistency max) |
| cut 3rd Pot only | 41 | 91.2% |
| cut 3rd Pot + 3rd Shiina | 40 | 92.2% |
| cut 2nd Meghala + 3rd Shiina | 40 | 91.9% |

All 40s clear the 90% floor; consistency favors 41 -> treat as constraint.

**Distinct plays, post-dig, going first** (P(≥1) doubles as the consistency cross-check):

| Config | E[plays] | P(≥1) | P(≥2) | P(≥3) |
|---|---|---|---|---|
| 42 keep all | 1.67 | 91.5% | 56.0% | 17.1% |
| 40 cut Pot + Shiina | 1.71 | 92.4% | **57.9%** | 18.3% |
| 40 cut Pot + Meghala | 1.60 | 90.9% | 53.1% | 14.6% |

(Pre-dig, for reference: E[plays] 1.30 / 1.37 / 1.29; P(≥2) 38.4 / 41.9 / 37.7%. Digs lift P(≥2)
by ~16 pts — they find second plays.)

**Actionable redundancy:** 3rd Pot = 3.6% dead-extra-copy vs 1.3% at 2x.

### Standing decisions
- **3rd Pot = the actionable-redundancy cut.** Cut it. (Consistency tie above the floor; loses on
  redundancy + draw-lock/Droll rigidity + random ED-banish risk. = Felix's "too clunky".)
- **Second cut to reach 40: a real trade on opposite axes.**
  - cut Shiina (keep 2nd Meghala): **+5 pts P(≥2) play-breadth going first** — more distinct plays.
  - cut Meghala (keep 3rd Shiina): a premium bidirectional non-engine piece + Shiina access.
  - Going-first plays favor **cut Shiina / keep Meghala** (consistent across consistency, pre- and
    post-dig plays). This *reverses* under going-second weighting (Meghala dead, Shiina a
    board-breaker) and Shiina's premium-ness (off the play-count axis). **Deferred to gut** for
    Nationals — it is the only contested slot whose value flips on the die roll; weight it by your
    die-roll / meta expectation.

---

## 7. Open / deferred
- **Going-second model** — the deciding axis for Meghala-vs-Shiina; closes the §4 caveat.
  Genuinely harder (board states, stacked interruption, line-choice vs an established board). Out
  of scope for Nationals prep.
- **True resilience = line-coverage** — over (interruptions × lines), chosen under a read (§2).
  The distinct-play count is the breadth proxy until this is built.
- **Document specific lines** — e.g. the optimal Eldam one-card line, the two Krosea lines —
  needed for the coverage / resilience model, not for opening consistency.
- **Lock the great-hand rate post-dig** (engine plays ∧ non-engine pieces) and the residual-value
  weighting before treating these as final rather than v1.