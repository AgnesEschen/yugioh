# Methodology — Assumptions & Simplifications Inventory

The explicit list of everything baked into our models. **This list IS the validation
agenda**: validating the methodology = scrutinizing each item. Each is tagged:

- **[derived]** — follows from card text / rules (low risk, but check the derivation).
- **[game-knowledge]** — Agnes's gameplay fact (Claude is NOT a reliable authority here;
  these are the items to defend from experience).
- **[choice]** — a modeling decision that could reasonably be made differently.
- **[simplification]** — a known approximation we accepted for tractability.
- **[scope]** — a deliberate boundary on what the model covers.

A claim in the paper should trace to one of: a derivation, an item below, or an empirical
(MC) result with its CI. Anything else is a **conjecture** and should be labelled so.

---

## 1. Opening-hand model
- **1a [derived]** Hypergeometric (draw without replacement). n = 5 going first, 6 going
  second (the 6th = the draw-for-turn). Matters only as hand size for these purposes.

## 2. Play predicate (the 6 play-types)
- **2a [choice]** A "play" is identified by OUTCOME, not card; the count is of *distinct*
  plays. (The whole quality framework rests on this definition — glossary/decision-axes.)
- **2b [derived]** OPT-collapse: same-card duplicates and functional equivalents collapse to
  one play (a play runs on its card's once-per-turn resource).
- **2c [game-knowledge]** Functional-equivalence collapses: Noble → Eldam, Tenki → Swen (a
  searcher that only ever fetches one starter = that starter, for play-counting). *Assumes the
  searcher is always spent on that target.*
- **2d [choice]** Krosea enabler set = {a Quick-Play already activated} ∪ {an RT Quick-Play in
  hand} ∪ {MST in hand AND ≥2 total S/T in hand} ∪ {F&V in hand AND Pot present}.
- **2e [choice]** Meghala enabler set = same as Krosea **minus F&V** (F&V resolves face-up = a
  target, enabling Krosea only; Meghala needs an RT Quick-Play or MST activation).
- **2f [choice]** MST-activation enabler test = "MST in hand AND ≥2 total S/T in hand" (set one
  S/T, MST it). The ≥2 threshold and the S/T set (ST_FOR_MST) are the modeling knobs.
- **2g [choice]** The Asc+Mani play requires Ascendance AND Manifestation BOTH in hand
  (mill → revive). A lone Ascendance reviving a Vision-discarded monster is **deliberately not
  counted** (discarding a starter to revive it is judged a loss).

## 3. Dig model
- **3a [derived]** Phase ordering: Vision (draw phase) resolves before Pot (start of MP1);
  the earlier dig can find the later card; a draw-lock only forbids the reverse order.
- **3b [derived]** Vision draw mode = draw 2, discard 1 (per its text).
- **3c [simplification]** Discard heuristic: junk (Fonix/VVV/Mandate) → a duplicate → spare
  enabler/non-engine → a unique piece last. Greedy, **not provably optimal**; chosen to avoid
  gratuitously discarding a play-piece and to be symmetric across configs.
- **3d [choice]** "Post-dig convention": digs resolve, then plays are counted on the resulting
  hand. (The quality metric is defined post-dig.)
- **3e [simplification]** Pot always draws (banish-6 → draw-2). Its going-second strategic
  liabilities (must fire at MP1 start, can't react to the board, ED-banish hurts Super Poly) are
  **not modeled** → Pot is overvalued going second.

## 4. Going-second model (v0)
- **4a [derived]** Going 2nd the opponent controls S/T, so Eldam/Swen/Meghala SELF-SS needs MST
  in GY; Krosea (SS off any Quick-Play) and the Asc+Mani play (direct GY-revive) do not.
- **4b [game-knowledge]** MST sources = {drawn MST, RT Quick-Plays' add-MST mode, Krosea's free
  MST-on-summon}. Eldam/Swen searching MST is a **losing line** (their searches are needed for
  board pieces) and is excluded.
- **4c [simplification]** "Find MST at some point" = an MST source appeared anywhere this turn
  (opening or dig). Vision is counted as both a dig AND an MST source (it can only do one) — a
  small over-credit.
- **4d [simplification]** Krosea-in-hand counts as an MST source unconditionally, though it must
  actually be summonable — a small over-credit.
- **4e [scope]** Models board-BUILDING only. **Board-BREAKING** (clearing an established board —
  Shiina, Droplet, Crown, the Mulcharmies, Ra) is entirely absent. This is the biggest single
  gap and the reason the Meghala-vs-Shiina going-2nd question is still open.

## 5. Numerics
- **5a [choice]** Recent quality/play numbers are **Monte Carlo** (CI ≈ ±0.05 pt at N = 2–3 M),
  not exact. The early consistency figures are **exact hypergeometric**. Always know which a
  given number is before reading a small gap as meaningful.

## 6. Scope of "consistency" vs "resilience"
- **6a [scope]** "Consistency" = opening P(functional / ≥1 play). It is held as a **constraint**
  (≥~90% floor), not maximized (maximizing it bloats the deck — the consistency-max of the
  contested deck is 41 cards). See decision-axes §1.
- **6b [scope]** True **resilience** = P(a line resolves | interrupted) = a coverage problem over
  (interruptions × lines), chosen under a read. We approximate it only by the **breadth proxy**
  (distinct-play count). The real line-coverage model is **unbuilt**. Don't over-read small
  play-count gaps as resilience verdicts.
- **6c [scope]** OPT is treated as constant (ignored) in the consistency/quality regime; it
  becomes a state variable only in the resilience regime (probability-toolkit "OPT consumption
  under negation"), which we have not yet simulated.

## 7. Card-data dependency
- **7a [game-knowledge]** All card text is from the KB (RT is post-cutoff; Claude's recall is not
  authoritative). Any model behavior that hinges on a card's text should be re-checked against
  card-reference.md, and any place Claude "corrected" an interaction should be treated with
  suspicion.
