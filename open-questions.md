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

## Q2 — The Manifestation + Ascendance package
Felix mains 2x Manifestation + 2x Ascendance as a consistency patch after Chant
went to 1; Agnes mains 0x Manifestation but instead mains an extra copy of Pot of Extravagance compared to Felix. Two conditional starters whose conditions
feed each other — quantify what the package adds (opening consistency, resilience)
and what it costs (bricks when halves don't align).
Finally compare: Is the Manifestation + Ascendance package worth it over a third copy of Pot of Extravagance, or other consistency boosting options?