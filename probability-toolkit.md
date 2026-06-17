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