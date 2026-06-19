"""
RADIANT TYPHOON — OPENING-HAND SIMULATION (reference implementation)
====================================================================
This consolidates the ad-hoc /tmp scripts from our sessions into ONE inspectable
file. It is NOT a validated, polished artifact — it is "the actual logic we ran,
organized so you can scrutinize it." Every modeling CHOICE is flagged with  # CHOICE:
or  # SIMPLIFICATION:  — those flags are the validation agenda (see
methodology-assumptions.md). Where a number came from exact math vs Monte Carlo is
noted too.

Two regimes (kept deliberately separate — see project instructions):
  - opening CONSISTENCY / quality  -> ignore OPT availability (constant turn 1)
  - resilience                     -> OPT is a state variable (NOT modeled here yet)

Nothing here models board-BREAKING or true line-coverage resilience. It is an
opening-hand, board-BUILDING model.
"""

import random, math

# ---------------------------------------------------------------------------
# DECK REPRESENTATION
# Cards are bucketed into the 20 categories the predicates actually reference.
# A deck is a multiset over these (a list of indices). We never model individual
# Extra-Deck cards (never drawn) except as the Pot banish-cost, which we ignore
# for draw math.  # CHOICE: 20 categories is the minimal set the play predicate needs.
# ---------------------------------------------------------------------------
CARDS = ['SWEN','ELDAM','CHANT','NOBLE','KROSEA','MEGHALA','ASC','MANIF','VISION',
         'POT','MST','FONIX','VVV','MANDATE','SHIINA','FV','DROPLET','CROWN','CALLED','TTT']
ix = {n: i for i, n in enumerate(CARDS)}
I  = lambda s: ix[s]
NC = len(CARDS)

# Total Spell/Trap count in hand (used by the MST-activation enabler test).
# CHOICE: this is the set of S/T cards a turn-1 hand could hold that count toward
# "set one S/T, MST it" enabling Krosea/Meghala. Monsters (Swen/Eldam/...) excluded.
ST_FOR_MST = [ix[x] for x in ['CHANT','ASC','MANIF','VISION','MST','POT','FV',
                              'DROPLET','CROWN','CALLED','TTT','MANDATE']]

# Cards Vision may discard (RT cards OR Quick-Plays). NOT: Shiina/Noble (non-RT
# monsters), Pot/TTT (Normal spells).  # CHOICE: from Vision's discard clause.
DISCARDABLE = [ix[x] for x in ['SWEN','ELDAM','KROSEA','MEGHALA','FONIX','VVV',
                               'CHANT','ASC','MANIF','MANDATE','MST','FV','DROPLET','CROWN','CALLED']]

# Going-SECOND MST sources: drawn MST, an RT Quick-Play's add-MST mode, or Krosea's
# free MST-on-summon. NOT Eldam/Swen searches (game-knowledge: spending their search
# on MST is a losing line). See methodology-assumptions.md item 4b.
MST_SRC = [ix[x] for x in ['MST','VISION','CHANT','ASC','MANIF','KROSEA']]


# ---------------------------------------------------------------------------
# DISCARD HEURISTIC  (Vision's draw mode discards 1)
# SIMPLIFICATION: greedy, not provably optimal. Junk first, then a duplicate,
# then spare enablers / non-engine, then a unique piece as last resort. Chosen so
# it does not gratuitously discard a play-piece, and is symmetric across configs.
# ---------------------------------------------------------------------------
def discard(c):
    for cat in [I('FONIX'), I('VVV'), I('MANDATE')]:          # pure non-plays
        if c[cat] > 0: c[cat] -= 1; return
    for cat in DISCARDABLE:                                    # a redundant duplicate
        if c[cat] >= 2: c[cat] -= 1; return
    for cat in [I('MST'), I('FV'), I('DROPLET'), I('CROWN'), I('CALLED')]:  # spare enabler / non-engine
        if c[cat] > 0: c[cat] -= 1; return
    for cat in [I('MEGHALA'), I('KROSEA'), I('SWEN'), I('ELDAM'), I('CHANT'), I('ASC'), I('MANIF')]:
        if c[cat] > 0: c[cat] -= 1; return                    # last resort: a unique piece


# ---------------------------------------------------------------------------
# PLAY PREDICATE — GOING FIRST  (opponent controls no S/T)
# Returns the number of DISTINCT plays in the hand. A play = an independent
# board-establishing action, identified by outcome not card; same-card duplicates
# and functional equivalents collapse (OPT). The 6 play-types:
# ---------------------------------------------------------------------------
def plays_g1(c, qpu, pa):
    # qpu = a Quick-Play was already activated this turn (e.g. Vision dig) -> Krosea/Meghala live
    # pa  = Pot was activated this turn (its face-up resolution is the F&V target for Krosea)
    tst = sum(c[i] for i in ST_FOR_MST)
    qp  = (c[I('CHANT')] + c[I('ASC')] + c[I('MANIF')] + c[I('VISION')]) >= 1   # an RT Quick-Play in hand
    mst = c[I('MST')] >= 1 and tst >= 2     # CHOICE: MST + >=2 total S/T  => set one S/T, MST it (enables Krosea AND Meghala)
    fv  = c[I('FV')] >= 1 and (pa or c[I('POT')] >= 1)   # CHOICE: F&V enables KROSEA ONLY (resolves face-up = target)
    kro = qpu or qp or mst or fv            # Krosea enabler set
    meg = qpu or qp or mst                  # Meghala enabler set (F&V excluded)
    n = 0
    if c[I('ELDAM')] or c[I('NOBLE')]: n += 1   # Eldam-line (Noble collapses to Eldam)
    if c[I('SWEN')]:                   n += 1   # Swen-line
    if c[I('CHANT')]:                  n += 1   # Chant
    if c[I('KROSEA')]  and kro:        n += 1   # Krosea (conditional on enabler)
    if c[I('MEGHALA')] and meg:        n += 1   # Meghala (conditional on enabler)
    if c[I('ASC')] and c[I('MANIF')]:  n += 1   # Asc+Mani 2-card combo = ONE play (mill -> revive)
    return n                                     # CHOICE: lone Asc (no Manif) is NOT a play (Vision-discard revival excluded)


# ---------------------------------------------------------------------------
# PLAY PREDICATE — GOING SECOND (v0, blanket MST gate)
# Going 2nd the opponent has S/T, so Eldam/Swen/Meghala SELF-SS needs MST in GY.
# Krosea (SS off any Quick-Play) and Asc+Mani (GY-revive) are MST-INDEPENDENT.
# We model MST as a BLANKET requirement: the hand can build a board only if an
# MST source was seen this turn (mst_access, computed by the caller over MST_SRC).
# SIMPLIFICATION: this washes the per-play structure (Agnes's call) and models
# board-BUILDING only — board-BREAKING is absent.
# ---------------------------------------------------------------------------
def plays_g2(c, qpu, pa, mst_access):
    if not mst_access:
        # No MST findable -> at most the one free Normal Summon + MST-independent plays.
        # In practice MST-independent plays need RT Quick-Plays (which ARE MST sources),
        # so this branch collapses to ~1 (a bare Eldam/Swen NS).  # SIMPLIFICATION
        return min(1, 1 if (c[I('ELDAM')] or c[I('NOBLE')] or c[I('SWEN')] or c[I('MEGHALA')]) else 0) \
               + (1 if (c[I('ASC')] and c[I('MANIF')]) else 0)
    return plays_g1(c, qpu, pa)   # MST available -> all self-SS unlocked, count as going first


# ---------------------------------------------------------------------------
# MONTE CARLO HARNESS
# Draw -> resolve digs in phase order (Vision draw-phase, then Pot at MP1) -> count.
# mode 'g1' (n=5, no MST gate) or 'g2' (n=6, blanket MST gate).
# Returns (P>=1, P>=2, P>=3, E[plays], P(mst_access)).
# Numbers are ESTIMATES: SE = sqrt(p(1-p)/N); at N=2-3M, ~+/-0.03 pts (95% CI ~+/-0.05).
# ---------------------------------------------------------------------------
def build(cnt):
    d = []
    for nm, k in cnt.items():
        d += [ix[nm]] * k
    return d

def run(cnt, mode='g1', N=2_000_000, seed=5):
    d = build(cnt); rng = random.Random(seed); sm = rng.sample
    ndraw = 9 if mode == 'g1' else 10      # 5 + 2(Vision) + 2(Pot)  /  6 + 2 + 2
    h0    = 5 if mode == 'g1' else 6
    p1 = p2 = p3 = tot = acc = 0
    for _ in range(N):
        s = sm(d, ndraw); c = [0]*NC; seen = [0]*NC
        for i in range(h0):
            c[s[i]] += 1; seen[s[i]] += 1
        qpu = False; pa = False; p = h0
        if c[I('VISION')] >= 1:            # Vision dig (draw phase): draw 2, discard 1
            qpu = True; c[I('VISION')] -= 1
            c[s[p]] += 1; seen[s[p]] += 1; c[s[p+1]] += 1; seen[s[p+1]] += 1; p += 2
            discard(c)                     # NB: 'seen' keeps the dug cards for mst_access ("seen this turn")
        if c[I('POT')] >= 1:               # Pot dig (start of MP1): draw 2
            pa = True; c[I('POT')] -= 1
            c[s[p]] += 1; seen[s[p]] += 1; c[s[p+1]] += 1; seen[s[p+1]] += 1; p += 2
        mst_access = any(seen[i] >= 1 for i in MST_SRC)   # SIMPLIFICATION: Vision double-counts as dig + MST source
        pl  = plays_g1(c, qpu, pa) if mode == 'g1' else plays_g2(c, qpu, pa, mst_access)
        ok  = True if mode == 'g1' else mst_access
        if ok: acc += 1
        if pl >= 1 and ok: p1 += 1
        if pl >= 2 and ok: p2 += 1
        if pl >= 3 and ok: p3 += 1
        tot += pl if ok else 0
    return p1/N, p2/N, p3/N, tot/N, acc/N


# ---------------------------------------------------------------------------
# DECK DEFINITIONS
# base = the 42-card test main. Each engine config = base with 2 flex copies cut.
# (Non-engine is locked at 13 for the engine analysis: 3 Shiina, 3 FV, 3 Droplet,
#  2 Crown, 1 Called, 1 TTT.)
# ---------------------------------------------------------------------------
BASE42 = {'SWEN':3,'ELDAM':3,'CHANT':1,'NOBLE':1,'KROSEA':3,'MEGHALA':2,'ASC':2,
          'MANIF':2,'VISION':3,'POT':3,'MST':3,'FONIX':1,'VVV':1,'MANDATE':1,
          'SHIINA':3,'FV':3,'DROPLET':3,'CROWN':2,'CALLED':1,'TTT':1}

def cfg(**mods):
    c = dict(BASE42); c.update(mods); return c


# ---------------------------------------------------------------------------
# ANALYSES (each reproduces a table from the sessions)
# ---------------------------------------------------------------------------
def engine_sweep():
    """11 engine builds (cut 2 of 6 flex copies), post-dig plays, going first."""
    builds = {
        'cut 3rdPot+Noble'  : cfg(POT=2, NOBLE=0),
        'cut 3rdPot+2ndMegh': cfg(POT=2, MEGHALA=1),
        'cut 3rdPot+2ndAsc' : cfg(POT=2, ASC=1),
        'cut 3rdPot+1Manif' : cfg(POT=2, MANIF=1),
        'cut Noble+2ndMegh' : cfg(NOBLE=0, MEGHALA=1),
        'cut Noble+2ndAsc'  : cfg(NOBLE=0, ASC=1),
        'cut Noble+1Manif'  : cfg(NOBLE=0, MANIF=1),
        'cut 2ndMegh+2ndAsc': cfg(MEGHALA=1, ASC=1),
        'cut 2ndMegh+1Manif': cfg(MEGHALA=1, MANIF=1),
        'cut 2ndAsc+1Manif' : cfg(ASC=1, MANIF=1),
        'cut both Manif'    : cfg(MANIF=0),
    }
    print("ENGINE SWEEP (post-dig, going first)   [P>=1 is the consistency floor; hold >=~90%]")
    print(f"{'cut':22s} {'P>=1':>7s} {'P>=2':>7s} {'P>=3':>7s}")
    rows = []
    for nm, c in builds.items():
        assert sum(c.values()) == 40, (nm, sum(c.values()))
        a = run(c, 'g1'); rows.append((nm, a))
    for nm, a in sorted(rows, key=lambda r: -r[1][2]):
        flag = '' if a[0] >= 0.90 else '  <FLOOR'
        print(f"{nm:22s} {a[0]*100:6.1f}% {a[1]*100:6.1f}% {a[2]*100:6.1f}%{flag}")

def great_hand():
    """great = P(>=3 engine plays AND >=2 distinct non-engine). Non-engine locked,
    so this ~tracks P(>=3 plays). (Reuses a separate counter; here we just print
    the play side — the non-engine side is in great.py.)"""
    for nm, c in {'42 keep all': BASE42,
                  '40 cut Pot+Shiina (keep Megh)': cfg(POT=2, SHIINA=2),
                  '40 cut Pot+Megh (keep Shiina)': cfg(POT=2, MEGHALA=1)}.items():
        a = run(c, 'g1')
        print(f"{nm:34s} P>=3 plays = {a[2]*100:.1f}%")

def uncertainty_demo(c=None):
    """Show Monte Carlo wobble: same build, 8 seeds, large vs small N."""
    if c is None: c = cfg(POT=2, MANIF=1)
    for N in [2_000_000, 10_000]:
        vals = [run(c, 'g1', N=N, seed=s)[2] for s in range(1, 9)]
        m = sum(vals)/len(vals); se = math.sqrt(m*(1-m)/N)
        print(f"N={N:>9,}: P>=3 in [{min(vals)*100:.2f},{max(vals)*100:.2f}]%  "
              f"mean {m*100:.3f}%  spread {(max(vals)-min(vals))*100:.3f}  "
              f"SE +/-{se*100:.4f}  95%CI +/-{1.96*se*100:.4f}")

def going_second():
    """Going first vs going second (blanket MST gate), 4 package configs."""
    builds = {'full pkg, M1': cfg(POT=2, MEGHALA=1),
              'trim pkg, M2' : cfg(POT=2, MANIF=1),
              'min pkg, Pot3': cfg(ASC=1, MANIF=1),
              'NO pkg, Pot3' : cfg(MANIF=0)}
    print(f"{'config':14s} | g1 P2/P3 | g2 P(MSTacc)/P2/P3")
    for nm, c in builds.items():
        a = run(c, 'g1'); b = run(c, 'g2')
        print(f"{nm:14s} | {a[1]*100:.1f}/{a[2]*100:.1f} | {b[4]*100:.1f}/{b[1]*100:.1f}/{b[2]*100:.1f}")


if __name__ == '__main__':
    engine_sweep();       print()
    great_hand();         print()
    uncertainty_demo();   print()
    going_second()
