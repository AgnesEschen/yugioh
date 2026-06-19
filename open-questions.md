# Open Questions

## Q1 — Pot of Extravagance: 3x vs 2x  [in progress]
Reframed as flex-slot allocation: the candidate configs differ only in {Noble, 2nd Manifestation,
3rd Pot}, with 1 Manifestation common to all. Opening-consistency predicate (live-starter, going
first, n=5), turn-1 activatable-Quick-Play set on an empty board:

  Q_act = {Vision, Chant, Ascendance, Manifestation}            (always-on modes)
        ∪ {MST}  if hand has ≥2 total S/T (set one, MST it)     → enables Krosea AND Meghala
        ∪ {F&V}  if hand has Pot (Pot resolves face-up = target) → enables Krosea ONLY

  Enab(Krosea)  = any of Q_act.   Enab(Meghala) = RT Quick-Play or MST in Q_act (F&V excluded).
  Ascendance is a live *starter* only with Manifestation (mill→revive); Manifestation is itself a
  Quick-Play, so it also sits in Q_act (enables Krosea/Meghala).

No-dig P(F), exact enumeration:
  C1 (Noble, Manif2, Pot2): 84.06%   — drops 3rd Pot
  C3 (Noble, Manif1, Pot3): 82.97%   — drops 2nd Manifestation
  C2 (Manif2, Pot3, no Noble): 80.70% — drops Noble  [weakest; dominated on this metric]

Marginals (full yardstick): Noble +3.37, 2nd Manifestation +1.09, 3rd Pot ≈0 (dig-only).
⇒ Decision reduces to C1 vs C3: 3rd Pot wins its slot iff its marginal *dig* value > +1.09 pts.
Digs: Vision-draw (Draw/Standby Phase) precedes Pot-draw (start of MP1) ⇒ up to 2 draw-2 events/turn
when both held; only Pot→Vision is blocked (draw-lock). So the 3rd Pot stacks a *second* dig on top
of Vision (not redundant), raising its marginal dig value above a mutual-exclusion estimate.
Pending: Monte Carlo for the 3rd Pot's marginal dig vs the +1.09 bar.

RESOLUTION: Dig MC (Vision→Pot, 2M trials, validated vs exact no-dig):
  C1 90.69% | C3 90.76% | C2 89.29%.  2nd Manif marginal +1.23 / 3rd Pot marginal +1.30,
  diff +0.07 ±0.06 ⇒ statistical tie on opening consistency. 2x-vs-3x-Pot does NOT resolve
  on opening hands. Decision → deferred axes: 3rd Pot's ED-banish / Droll-rigidity costs vs
  Manifestation's Droll/going-2nd utility both favor C1. PICK: Config 1 (Noble + 2 Manif + 2 Pot),
  = Felix's profile. Q1 answer: 2x Pot. (Resilience tiebreak qualitative; rigorous resilience = later.)


## Q2 — The Manifestation + Ascendance package  [opening-hand axis RESOLVED; full-vs-trim + going-2nd OPEN] 
Engine-lineup analysis. Non-engine locked at 13; cut 2 of the 6 flex engine copies
{2nd Meghala, 2nd Ascendance, Manif×2, 3rd Pot, Noble} → 11 builds, scored on post-dig
plays going first (engine.py / rt_simulation_reference.engine_sweep).
 
Findings:
- **Noble + 2nd Meghala are keepers.** Cutting either is worst: cutting the 2nd Meghala
  drops good-hand ~2.5 pts (it's a distinct play); cutting Noble drops ~1 pt AND risks the
  90% floor (cut-Noble+2ndMegh = 89.5%, cut-3rdPot+Noble ≈ 89.9%).
- **The Asc+Mani package is internally redundant for opening hands.** Trimmable from 2+2
  to 3-total at ~0.8 pt; even 0 Manif (Ascendance as pure enabler) costs only ~0.8 pt. Cause:
  the Asc+Mani play needs only 1 of each in hand, and the enablers are already saturated
  (3 Vision + Chant + the package ≫ what Krosea/Meghala need).
- **3rd Pot scores FINE on opening plays** — its dig beats a redundant package copy, so the
  top build keeps Pot3 and cuts 2 package pieces (P≥3 17.4%). Cutting the 3rd Pot rests on
  out-of-metric clunk (draw-lock, Droll-rigidity, random ED-banish vs the 3× Marine Eidolon
  requirement), NOT on plays. ⇒ mild evidence FOR 3rd Pot on the plays axis (feeds Q1's open
  general 2x-vs-3x question).
- **Cutting 2nd Asc vs a Manif is identical on opening plays** (the play is bottlenecked by
  whichever is the singleton). Tiebreak → keep the 2nd Ascendance for its post-side value.
Recommended engine cut (opening-hand axis): **cut 3rd Pot + 1 Manifestation** (→ 2 Pot,
2 Asc, 1 Manif, 2 Megh, Noble; P≥1 91.2 / P≥2 55.0 / P≥3 16.7). Honest alternative if valuing
the dig: keep Pot3, cut 2nd Asc + 1 Manif (the 17.4% top build). The ~0.7 pt gap = the size of
the 3rd-Pot-clunk judgment call.
 
Going-second follow-up (v0 model — see probability-toolkit "Going-second model"). The package
has a measured going-2nd premium via TWO channels: (1) the Asc+Mani play is MST-INDEPENDENT
(board-maker worth ~1.5× its going-first value), (2) Asc/Manif are themselves MST-sources
(full package = highest MST-access, ~95.7%). BUT the value is concentrated in the FIRST copy of
each; full 2+2 over a trim is still not vindicated, even going second.
 
STATUS: opening-hand axis resolved (trim is correct on plays; running full 2+2 is a defensible
comfort/Felix/going-2nd call the model can't overturn). **Full-vs-trim and the board-BREAKING
dimension remain open** (the latter is the going-2nd hard problem).