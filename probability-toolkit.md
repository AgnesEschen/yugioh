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