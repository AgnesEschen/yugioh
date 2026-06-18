# Decision Axes

The framework for evaluating a deck configuration **beyond raw consistency**. Consistency is
necessary but not sufficient: optimizing it alone bloats the deck, because it has no stop
signal (see proof below). This file defines the full objective — consistency as a *constraint*,
then **quality / redundancy / direction / coverage** as the things to actually optimize.

Companion files: `glossary.md` (vocabulary), `probability-toolkit.md` (methods), `open-questions.md`
(worklog), `card-reference.md` / `card-schema.md` (card data + the `Functional equivalence` field
this framework relies on).

---

## 1. The objective structure

**Consistency is a constraint, not a maximand.** Hold

    P(functional opener) = P(>=1 live starter, going first, 5-card hand)  >=  ~90%

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
1. **Hand quality** — distinct useful pieces (§2).
2. minimize **Redundancy** (§3).
3. respect **Direction** — the going-first / going-second split (§4).
4. **Matchup coverage** — the non-engine suite; evaluated on win-rate / playtesting, *not* draw math.

---

## 2. Hand quality — distinct useful pieces

The right primitive is not card count, nor consistency, but the number of **distinct useful
pieces** in the hand, split by category.

### The useful filter (what counts as a piece)
Two gates; a card is a piece iff it passes **both**:

1. **Liveness** — it does something in *this* game state (going first, empty board). Fails:
   dead conditionals (lone Ascendance with no Manifestation; lone Meghala/Krosea with no
   enabler), wrong-direction cards (a sided going-2nd card held going 1st).
2. **Distinct function** — it adds a *new* capability, not a duplicate of one already counted.
   Fails: functional equivalents (Noble = Eldam-line; Tenki = Swen-line — see
   `card-reference.md` `Functional equivalence`), and extra copies of a one-use card (2nd Pot).

=> **distinct useful pieces = distinct *live functional roles*, NOT unique card names.**
Noble + Eldam = two names, one role, one piece.

### Structure of quality
- **Engine is paramount; >=1 starter is the gate.** You cannot play without it.
- Above the gate:
  - distinct **engine** pieces -> **resilience** (independent routes that survive a point of
    negation) + **ceiling** (bigger board). Saturating past ~3-4 (you can only do so much/turn).
  - distinct **non-engine** pieces, on a solid engine core -> the **good -> great** step
    (interruption going 1st, board-breaking going 2nd).
- **Stellar hand ~= 3 distinct engine + 2 distinct non-engine.** Strong both ways: engine pushes
  through hand traps and raises the ceiling; non-engine breaks boards going 2nd and interrupts
  going 1st.

---

## 3. Redundancy — the core clunkiness axis

After the corrections in §4, "clunkiness" collapses to mostly **redundancy**:
`cards held − distinct useful pieces`.

- **Hard redundancy** — fully-dead duplicates (the extra copy does nothing this turn). In RT this
  is ~entirely a **Pot** effect (OPT + draw-lock + must-be-first action): a 3rd Pot puts a dead
  copy in **3.6%** of hands vs **1.3%** at 2x. *This is the actionable kind.*
- **Soft redundancy** — duplicates with residual insurance value: a 2nd starter (backup vs a hand
  trap), a 2nd Shiina (next-turn backup), functional equivalents (Noble + Eldam = a 2nd route).
  Not wasted, but not a distinct piece either.
- **Do not** use deck-total duplicate *name* count as the metric: it sits near its floor here
  (~0.35/hand, a poor discriminator) **and** undercounts — it misses functional equivalents
  (Noble+Eldam) and dead conditionals. Use **hard-redundancy + distinct-piece counting** instead.

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

(Caveat for §2's metrics: the current model is **going-first only**, so it *overvalues*
first-skewed cards like Meghala and *undervalues* premium bidirectional cards like Shiina. A
going-second model is needed to close this — see `open-questions.md`.)

---

## 5. Metrics

| Metric | Definition | Use |
|---|---|---|
| **Consistency (floor)** | P(>=1 live starter), going 1st, 5 cards | Hold >= ~90% |
| **Resilience** | P(>=2 distinct engine pieces) | ~ survives 1 hand trap |
| **Good-hand rate** | P(>=3 distinct engine pieces) | engine depth / ceiling |
| **Great-hand rate** | P(>=3 distinct engine AND >=2 distinct non-engine) | the stellar 3+2 |
| **Hard redundancy** | P(>=2 copies of a hard-redundant card) | in RT: the Pot |
| **Power-card access** | P(see >=1 of a key card) | matchup coverage |
| **Premium dilution** | P(open a given 1-of) at deck size N (= 5/N) | cost of going >40 |

**Note — the joint objective.** "Maximize consistency AND minimize redundancy" is *not* a separate
goal: it equals the **distinct-piece count**. A distinct piece requires presence (consistency) and
non-duplication (low redundancy) simultaneously, so the good/great-hand rates score both at once.

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

All 40s clear the 90% floor comfortably. Consistency favors 41 -> treat as constraint.

**Quality / piece metrics** (going first):

| Config | E[pieces] | P(>=2) | good P(>=3) | great |
|---|---|---|---|---|
| 42 keep all | 1.95 | 67.4% | 27.4% | 3.7% |
| 40 cut Pot + Shiina | 1.95 | 67.3% | 27.4% | 3.5% |
| 40 cut Pot + Meghala | 1.86 | 64.2% | 24.1% | 3.5% |

**Hard redundancy:** 3rd Pot = 3.6% dead-extra-copy vs 1.3% at 2x.

### Standing decisions
- **3rd Pot = the hard-redundancy cut.** Cut it. (Consistency tie above the floor; loses on
  hard-redundancy + draw-lock/Droll rigidity + random-ED-banish risk. = Felix's "too clunky".)
- **Second cut to reach 40: a real trade on opposite axes.**
  - cut Shiina (keep 2nd Meghala): +3 pts good-hand / resilience going first — more distinct engine.
  - cut Meghala (keep 3rd Shiina): more distinct non-engine + premium bidirectional access.
  - Going-first metrics favor **cut Shiina / keep Meghala**; this *reverses* once you weight going
    second (Meghala dead, Shiina a board-breaker) and Shiina's premium-ness (worth > generic
    non-engine). Decision hinges on matchup / die-roll expectation -> needs the going-2nd model.

---

## 7. Open
- Going-second quality model (the deciding axis for Meghala-vs-Shiina; closes the §4 caveat).
- Resilience under negation (OPT-consumption regime; `probability-toolkit.md`).
- Lock the §2 piece definition (which lone conditionals / enablers count; is MST a piece or only
  an enabler) before treating the good/great-hand rates as final rather than v1.
