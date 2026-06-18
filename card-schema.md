# Card Schema

The data dictionary for `card-reference.md`: the structure of a card entry, every field,
and its allowed values. Locked by inference from the populated card reference — adding new
cards should be mechanical against this spec.

Field *meanings* for the Role / Engine class vocabularies live in `glossary.md`; this file
defines the *structure* — which fields exist, in which zone, required-when, and allowed values.

---

## Entry structure

Each card is one entry, in two zones:

    ## <Card Name>
    ### Card data            ← objective, from the card; authoritative over Claude's recall
    - Type: ...
    - ...
    - Text: <verbatim official text>
    ### Annotations (Agnes)  ← Agnes's interpretation; not authoritative card text
    - Engine class: ...
    - Role: ...
    - ...

- `## ` for the card name; `### ` for each zone heading.
- **Card data** holds objective card facts; `Text` is verbatim and overrides Claude's own recall.
- **Annotations (Agnes)** holds classification and notes — interpretation, not card text.

---

## Field summary

| Field                    | Zone        | Required                          | Type                          |
|--------------------------|-------------|-----------------------------------|-------------------------------|
| Type                     | Card data   | Always                            | enum (card type)              |
| Typing                   | Card data   | Always                            | enum (domain depends on Type) |
| Attribute                | Card data   | If monster                        | enum                          |
| Level/Rank               | Card data   | If a monster with a Level or Rank | integer                       |
| Link                     | Card data   | If a Link monster                 | integer                       |
| Archetype                | Card data   | If the card belongs to one        | text                          |
| Forbidden & limited list | Card data   | If currently restricted           | enum + date                   |
| Text                     | Card data   | Always                            | verbatim text                 |
| Engine class             | Annotations | If a main-deck card               | enum {Engine, Non-Engine}     |
| Role                     | Annotations | Always                            | list of role tags             |
| Condition                | Annotations | If a Conditional <Role> is tagged | precondition text             |
| Requirement              | Annotations | If the Requirement role is tagged | count + rationale             |
| Key notes                | Annotations | Optional                          | free text                     |
| Background notes         | Annotations | Optional                          | free text                     |

---

## Card data fields

### Type
- **Required:** always. **Type:** enum.
- The card type / frame: Effect Monster, Normal Monster, Ritual Monster, Fusion Monster,
  Synchro Monster, XYZ Monster, Link Monster (+ Pendulum variants), Spell, Trap.

### Typing
- **Required:** always. **Type:** enum; allowed values depend on `Type`.
- Monster → the monster Type (Aqua, Beast, Beast-Warrior, Dragon, Fairy, Fiend, Insect,
  Machine, Pyro, Spellcaster, Warrior, Winged Beast, Wyrm, Zombie, …).
- Spell → Normal, Field, Equip, Continuous, Quick-Play, Ritual.
- Trap → Normal, Continuous, Counter.
- (This is the field YGOPRODeck calls `race`.)

### Attribute
- **Required:** if monster (N/A for Spell/Trap). **Type:** enum.
- WIND, LIGHT, DARK, FIRE, WATER, EARTH, DIVINE.

### Level/Rank
- **Required:** if a monster that has a Level or Rank — i.e. non-Link monsters (Xyz record
  their Rank here). N/A for Link monsters and Spell/Trap. **Type:** integer.

### Link
- **Required:** if a Link monster (used in place of Level/Rank). N/A otherwise.
  **Type:** integer (the Link rating).

### Archetype
- **Required:** only if the card belongs to an archetype; omit otherwise. **Type:** text.
- e.g. Radiant Typhoon, Branded, Bystial.

### Forbidden & limited list
- **Required:** only if the card is currently restricted; **omit ⇒ Unlimited (max 3).**
  **Type:** enum + date stamp.
- Values and legal max: Forbidden (0), Limited (max 1), Semi-limited (max 2).
- Date-stamped, since it is volatile: `Limited (as of YYYY-MM-DD)`. The KB value is
  authoritative over Claude's recall; a stamp older than today is a prompt to re-verify.

### Text
- **Required:** always. **Type:** verbatim official card text.
- The single source of truth for what the card does; overrides Claude's recall. Annotations
  should reference, not restate, this field.

*(ATK/DEF are deliberately omitted — not relevant to opening-hand draw math. They can be added
later as conditional-if-monster fields if combat math is ever needed.)*

---

## Annotations (Agnes) fields

### Engine class
- **Required:** if a main-deck card; **N/A for Extra Deck cards** (never drawn, so the
  opening-hand axis does not apply). **Type:** enum {Engine, Non-Engine}.
- Definition and the opponent-independence test live in `glossary.md`.

### Role
- **Required:** always (≥ 1 tag). **Type:** comma-separated list of tags from the controlled
  vocabulary below. A card carries *every* role it can fill.

  - **Proactive:** Starter, Conditional Starter, Extender, Requirement, Boss Monster,
    Consistency, Card Advantage.
  - **Disruption (by deployment mode):** Hand Trap, End-Board Piece, Board Breaker,
    GY Board Breaker, Floodgate, Protection.
  - **Extra-deck purpose:** Extra Deck Toolbox, Super Polymerization Target,
    The Fallen & The Virtuous Target.
  - **[convention]** Any role may take a `Conditional ` prefix (Conditional Starter,
    Conditional Board Breaker, Conditional Consistency, …) when it is gated on a `Condition`.

  Definitions live in `glossary.md`.

### Condition
- **Required:** if any Role carries the `Conditional` prefix; absent otherwise.
  **Type:** precondition text.
- States the precondition under which the conditional role(s) hold, expressed as a predicate
  over game states / capabilities — **not** a list of partner cards.

### Requirement
- **Required:** if the `Requirement` role is tagged; absent otherwise. **Type:** text.
- The minimum count of this card the deck must include to fulfil its game plan, plus rationale.

### Functional equivalence
- **Optional:** names the card this one functionally reduces to, when a searcher only ever fetches one starter.

### Key notes
- **Optional.** Short-form, decision-relevant annotation (typical usage, a modeling-relevant fact).

### Background notes
- **Optional.** Lower-priority context — meta colour, naming, deeper combo exposition — not
  load-bearing for the math.

---

*Future code integration: a field → YGOPRODeck API-key mapping (Type/Typing → `type`/`race`,
Text → `desc`, Forbidden & limited list → `banlist_info`, etc.) can be added here if/when the
data is pulled programmatically — deferred for now, as discussed.*
