# Glossary

Shared vocabulary for the Radiant Typhoon probability / deck-building project.
Game-meaning definitions are Agnes's domain — correct any that don't match your usage.
Entries marked **[convention]** are project conventions we agreed on, not standard terms.

---

## Deck & game basics

- **Deck sizes.** Main Deck 40–60 cards (40 is standard; minimising size maximises the density of any one card). Extra Deck ≤ 15, Side Deck ≤ 15.
- **Opening hand.** 5 cards going first, 6 going second — the project default for the hypergeometric model unless stated otherwise. Note that, when going second, the sixth card is technically drawn as the draw-for-turn once your opponent passes the turn to you. Matters in niche game play scenarios but not for consistency calculations.
- **Going first / going second.** A "Starter" classification carries an implicit going-first assumption: on turn 1 the opponent controls no Spells/Traps, a condition several Radiant Typhoon cards lean on.
- **GY.** Graveyard.
- **OPT / "once per turn."** A hard once-per-turn gate on an effect. Several card conditions depend on whether an OPT has already been spent.
- **Set.** Placing a card face-down (a Spell/Trap, or a monster in face-down Defense).
- **Special / Normal / Tribute Summon.** The summon modes. A Tribute Summon consumes the turn's Normal Summon and requires tributing monster(s).
- **Banish.** Remove a card from play (distinct from sending it to the GY).
- **Mill.** Move a card from Deck to GY without drawing it.
- **Search / add.** Move a specific card from Deck to hand.
- **WIND-lock.** A recurring Radiant Typhoon restriction: "cannot Special Summon for the rest of this turn, except WIND monsters."
- **One-card combo.** A starter that, alone in the opening hand (going first), reaches ≥ T2 — a singleton sufficient hand-subset. Coincides with the unconditional Starter role here; conditional starters reach T2 but aren't one-card combos (they need their enabler). (In play terms: a 1-card *play* — see **Plays, lines, and end-boards**.)

## Engine classification — the `Engine class` field

A **main-deck-only** partition of a card's primary purpose. N/A for Extra Deck cards: they're never drawn, so the opening-hand axis does not apply to them.

- **Engine.** A card that advances the deck's game plan *independently of the opponent* — under your own agency. Includes off-archetype enablers (Shield-Bearer, Tenki, Pot of Extravagance), not just Radiant Typhoon cards.
- **Non-Engine.** A card whose function is *contingent on the opponent* — reactive interaction, protection, or disruption.
- **[convention] The opponent-independence test** resolves boundary cases: does the card advance your plan regardless of the opponent (Engine), or does its function only fire because of what the opponent does/has (Non-Engine)? Pot draws unconditionally → Engine; Triple Tactics Talent draws only if the opponent interrupts → Non-Engine.

## Functional roles — the `Role` field

A card carries **every** role it can fill; which one is "live" depends on the line and game state. Roles are context-dependent functions, not a single intrinsic label.

### Proactive (plan-advancing) roles
- **Starter.** Begins a combo toward your endboard on its own (implicit going-first assumption — see above).
- **[convention] Conditional Starter.** Starts a combo only when a stated `Condition` holds. The condition is expressed as a precondition over game states, not as a list of partner cards.
- **Extender.** Continues a line after interruption by *adding resources*, without itself starting. Noted for completeness, but in Radiant Typhoon (and most modern decks) starters and extenders largely coincide, so we rarely use it.
- **[convention] Requirement.** A card the deck must include, at some minimum count, to fulfil its game plan; the count lives in a `Requirement` field.
- **Boss Monster.** A primary payoff monster the plan aims to resolve.
- **Consistency.** Improves the reliability of reaching a functional hand / game plan. NB: *opening* consistency — P(functional opener) — is a different quantity from *resilience* (P(line resolves | interrupted)); both are called "consistency" colloquially. In real games you should almost always expect to meet interruption, so while the opening consistency is very relevant, resilience is also critical. The distinct-**play** count is a *breadth* proxy for resilience; true resilience is line-coverage (see **Plays, lines, and end-boards** and `decision-axes.md`).
- **Card Advantage.** Nets more cards than it costs. Also referred to as "plussing". For example, Pot of Extravagance goes +1 (i.e. "plus one") since the end result of its effect is you ending up with one more card in your hand than you had before.

### Disruption roles (sorted by deployment mode)
- **Hand Trap.** Disruption used from the hand to interrupt your opponent's plays.
- **End-Board Piece.** Disruption you leave *established* on board going first, to interrupt the opponent's following turn (e.g. Solemn Judgment, Totem Bird).
- **Board Breaker.** Offence going second to clear the opponent's established board.
- **GY Board Breaker.** Board-breaking that operates on the opponent's GY.
- **Floodgate.** A persistent restriction on the opponent.
- **[convention] Protection.** Negates or removes the opponent's disruption so your own line resolves (e.g. Called by the Grave negating a hand trap). Distinct from Extender: it *subtracts* the opponent's interruption rather than *adding* your own resources.

### Extra-Deck purpose roles
- **Extra Deck Toolbox.** A situational Extra Deck monster summoned off the engine.
- **Super Polymerization Target.** The Fusion Monster *summoned* by Super Polymerization (typically out of the opponent's monsters, removing them). NB: the "target" is the card produced, not the material.
- **The Fallen & The Virtuous Target ("F&V Target").** An Extra Deck monster *sent* as cost to fuel The Fallen & The Virtuous. NB: the opposite sense to a Super Poly Target — the card fed *in*, not produced.

### The `Conditional <Role>` convention
- **[convention] Conditional &lt;Role&gt;.** The card fills `<Role>` only when its `Condition` holds; used wherever a role is gated on a precondition (Conditional Starter, Conditional Board Breaker, Conditional Consistency, …). Example: Pot of Extravagance = Consistency + Card Advantage (unconditional); Triple Tactics Talent = the same, but *Conditional*, since it needs the opponent to have activated a monster effect during your Main Phase. The prefix is exactly what distinguishes the two.

## Plays, lines, and end-boards — [convention]

The quality / resilience vocabulary, layered from abstract to concrete. (Formal reachability machinery lives in `probability-toolkit.md`; the framework that uses these lives in `decision-axes.md`.)

- **Play.** A distinct, *independent* action that establishes board presence or initiates the combo — identified by its **outcome, not the card** that triggers it. Same-card duplicates and functional equivalents collapse to one play (Noble + Eldam = one Eldam-play), because a play runs on its card's OPT and a duplicate can't run it again the same turn. The count of distinct plays in a hand is the **opening-hand quality / resilience-breadth** primitive. A Starter is the source of a play; a one-card combo is a 1-card play; a 2-card combo (Ascendance + Manifestation) is *one* play from two cards.
- **Not a play.** A **dig** is a *play-finder*, not a play (below). Pure payoffs / components — Fonix, Varuroon, Mandate, and usually MST — are engine but do not initiate, so they are not plays.
- **Dig.** A draw effect (Pot; Vision's draw mode). A dig is a *play-finder*: it raises P(≥1 play) and can find additional plays, but is not itself a play. Its value is **consistency-weighted** (the draw is OPT-capped at one event per turn, so extra copies mostly rescue low-play hands).
- **Line (combo-line).** The concrete, low-level sequence of actions that executes a play to a specific end-board — formally a *path* in the reachability model. A play generally affords **several** lines with different interruption trade-offs (a draw-phase Krosea line dodges Droll; a bait-first Krosea line eats Droll but dodges most other hand traps).
- **Optimal line.** Of a play's available lines, the one reaching the strongest end-board *while playing around the most opponent interruption* — i.e. the argmax over the opponent's interruption distribution, not against a fixed target.
- **Play vs end-board tier.** The **play** and the end-board **tier** (`end-board-tiers.md`) are the *abstractions*; the **line** and the concrete end-board are the *particulars* that connect them. "Play P reaches tier T" ⟺ a line exists from P to a board satisfying T.

## Abbreviations
- **MST** — Mystical Space Typhoon.
- **F&V** — The Fallen & The Virtuous.
- **droll** — Droll & Lock Bird.
- **super poly/spoly** - Super Polymerization.
- **Extrav** - Pot of Extravagance.

## Other terms
- **Half-board.** A reduced / incomplete end board, resulting from *any* disruption (e.g. several hand traps forcing the opponent to stop short) — not specifically a Mulcharmy.
- **End-board.** The board state you establish at the end of your combo turn.

---

*Modeling vocabulary (state, operator, precondition, reachability, enabler set) belongs in `probability-toolkit.md`, since it is method rather than game terminology.*