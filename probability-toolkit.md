# Probability Toolkit

## OPT consumption under negation  (resilience modeling)
Each effect carries a "mark OPT used" postcondition. When it fires depends on the
card's OPT clause:
- "can only be USED once per turn"      → marks on attempt (activation); negation of
  the activation OR the effect does NOT restore it. (RT + most modern engine cards.)
- "can only be ACTIVATED once per turn" → marks only on successful activation;
  negating the activation leaves it unspent, negating the effect spends it.
Companion input (also game-knowledge): which interruptions negate the *activation*
vs the *effect* — pair with the OPT clause to decide if an interrupted card recycles.

## Opening-hand consistency: the live-starter reduction  (opening-consistency regime)
Setup. Going first, hand of n (default 5) drawn without replacement from N (default 40).
Want P(functional opener) := P(hand can execute the plan to the target tier).

Reduction. When every starter is a one-card combo (alone reaches the tier — see glossary),
plan-execution collapses to a *presence* predicate; no combo tree need be traced:

    F(hand) ⟺ hand contains ≥1 *live* starter,

  live(unconditional s) ⟺ s ∈ hand                          (modulo going-first)
  live(conditional s)   ⟺ s ∈ hand ∧ (Enab(s) ∩ hand ≠ ∅)

Enab(s) is read off card text + turn-1 game state (e.g. which Quick-Plays are activatable
on an empty board). Mutually-enabling pairs (each dead alone, live together) appear as a
conjunction s₁ ∈ hand ∧ s₂ ∈ hand.

Computation. Partition the deck into the categories the predicate references (unconditional
starters; each conditional starter; each enabler class; blanks). P(F) is an exact multivariate-
hypergeometric sum over category-count vectors summing to n — closed under exact enumeration,
no Monte Carlo. Floor (clause-1 only): 1 − C(N−K, n)/C(N, n),  K = #unconditional starters.

Marginal value (the yardstick). A consistency/redundancy candidate X is valued by its marginal
contribution to the *full* P(F), against the *complete* baseline:
    ΔP_X = P(F | deck+X) − P(F | deck∖X) = P(X ∈ hand ∧ ¬F_without).
This is strictly below X's contribution to any *partial* metric (e.g. unconditional-only),
because ¬F_without ⊊ {no unconditional starter}: conditional starters and digs already rescue
a subset. Compare competing candidates only on this same full yardstick. To fill k slots from a
candidate pool: rank by ΔP, keep the top k (≡ drop the smallest) — exact when marginals don't
overlap, robust as a ranking otherwise; confirm by direct P(F) of the finalist configs.

Digs (draw effects), second layer. A draw effect is a conditional extra draw:
    P(F with digs) = P(F in opening n) + P(¬F ∧ dig source in hand ∧ post-draw hand functional),
re-evaluating F on the post-draw hand (dig card consumed; account for any discard).
OPT caps repetition: a hard OPT on the *draw effect* (spanning all copies of the name) caps that
draw at one use/turn — extra copies don't stack draws, only raise P(≥1 in hand) and serve other
roles. But model the *timing window* of each draw, not just OPT: a Quick-Play draw usable in the
Draw/Standby Phase precedes a start-of-MP1 draw, so two OPT draws can *sequence* — and the earlier
can dig into the later card — even when one imposes a "no draws rest of turn" lock; the lock only
forbids the *reverse* order. So digs are bounded by phase-ordering + locks, not mutual exclusion.
Conditional re-evaluation ⇒ Monte Carlo, with phase-ordering, OPT, and lock structure stated.
(Cf. "OPT consumption under negation" for the resilience-side OPT bookkeeping.)

## Post-dig play-counting  (opening-hand QUALITY regime, Monte Carlo)
Beyond consistency, hand QUALITY = the distinct-**play** count (glossary / decision-axes).
Computed by Monte Carlo (closed form is unwieldy: digs branch the hand, conditional enablers,
discard choice):
- Draw n (5 going first). Resolve digs in **phase order**: Vision (draw phase) draws 2 and
  discards 1 (discard rule below); then Pot (start of MP1) draws 2. Evaluate the play predicate
  on the post-dig hand ("post-dig convention").
- Predicate = the 6 play-types (Eldam-line{Eldam∨Noble}, Swen, Chant, Krosea[enabler],
  Meghala[enabler], Asc+Mani[both]); enabler sets per card text (see methodology-assumptions.md
  for the exact conditions — they are CHOICES).
- Metrics: P(≥1) = consistency floor; P(≥2) = resilience-breadth proxy; P(≥3) = good-hand;
  great-hand = P(≥3 engine plays ∧ ≥2 distinct non-engine).
- Discard heuristic (SIMPLIFICATION, not optimal): junk (Fonix/VVV/Mandate) → a duplicate →
  spare enabler/non-engine (MST/FV/Droplet/Crown/Called) → a unique piece last.

## Monte Carlo uncertainty  (how to read the numbers)
Two kinds of project numbers:
- **Exact hypergeometric enumeration = DETERMINISTIC** (no CI; true to the digits). E.g. the
  no-dig consistency figures.
- **Post-dig play numbers = MONTE CARLO ESTIMATES** (have a CI). For a proportion p over N
  trials, SE = √(p(1−p)/N); error shrinks like 1/√N. At N = 2–3 M: SE ≈ ±0.02–0.03 pts,
  95% CI ≈ ±0.05 pts. So a difference ≳0.2 pt is real; ≲0.1 pt is noise. (Demonstrated: same
  build, 8 seeds — N=2M spreads 0.03 pts, N=10k spreads ~1.0 pt.)
- **Statistical ≠ practical significance.** A real ~1 pt MODEL difference is still dominated by
  MODEL uncertainty (the model's distance from the real game, esp. going-second). Don't let a
  ~1 pt model edge drive a real-deck decision; treat anything within a point or two as "the model
  is indifferent — decide on axes it doesn't capture."

## Going-second model  (v0 — board-BUILDING only)
n = 6 (extra draw). MST flips from a near-dead card (going 1st) to the gate the engine runs
through: Eldam/Swen/Meghala SELF-SS needs MST in GY going 2nd. **Krosea** (SS off any Quick-Play)
and the **Asc+Mani play** (GY-revive) are MST-INDEPENDENT.
- Blanket MST gate: hand can build a board only if an MST source was seen this turn, sourced
  ONLY from {drawn MST, RT Quick-Plays' add-MST mode, Krosea's free MST-on-summon}. NOT from
  Eldam/Swen searches (game-knowledge: a losing line — their searches are needed for board pieces).
- Result: MST-access is high (~93–96%; the deck is dense in sources), so the gate is mild and the
  going-2nd board-rate (~65%) EXCEEDS going-first (~54%) — the extra card beats the gate. Package
  premium = two channels above.
- **LIMITATION (key):** models board-BUILDING, not board-BREAKING. The essence of going 2nd —
  clearing an established board first (Shiina/Droplet/Crown/Mulcharmy/Ra) — is NOT captured. So
  Meghala's going-2nd weakness (builds, can't break) and Shiina's strength (breaks) are unmodeled.
  This is the remaining hard problem.