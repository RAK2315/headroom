# Spike results (2026-11-07)

Machine: the owner's Windows 11 laptop, 16 logical cores, Python 3.12.15, numpy 2.5.4, scipy 1.18.1, highspy 1.15.1. Toy instance: 45 pools x 26 weeks = 1,170 cells, random but realistic magnitudes (net rates ₹5,000-12,000, demand 80-600 units per cell-week with 5 peak weeks).

## Spike 1: joint two-stage stochastic MILP (`opt_spike.py`, `hs_spike.py`)
Model: first stage hard and allotment per cell + 6 supplier binaries; per scenario recourse (served from hard, allotment, free sale; utilisation slack); CVaR (Rockafellar-Uryasev); availability reward; budget.

| S | vars | rows | solver | result |
|---|---|---|---|---|
| 32 | 152 k | 187 k | scipy milp (HiGHS MIP) | time limit 60 s, no useful incumbent |
| 64 | 302 k | 374 k | scipy milp | time limit 60 s, no useful incumbent |
| 128 | 602 k | 749 k | scipy milp | time limit 60 s, no useful incumbent |
| 32 | 152 k | 187 k | HiGHS LP relaxation, IPM | time limit 60 s |
| 32-64 | | | HiGHS LP simplex | time limit 60 s |
| 32-64 | | | HiGHS PDLP | stops early, inaccurate |

Conclusion: the monolithic model is not interactive at demo size. Do not build it as the main engine. Keep a tiny exact version (4 pools x 4 weeks x 32 scenarios) only as a test oracle for the decomposition.

## Spike 2: Lagrangian decomposition (`decomp_spike.py`)
Value tables over (3 markups x 12 hard x 12 allotment) per cell on S correlated scenarios; nested bisection on capital price and availability weight.

| S | tables | allocation (14 x 22 bisection steps) | budget hit | availability vs target |
|---|---|---|---|---|
| 128 | 2.16 s | 1.35 s | exact (5.000e7 for 5e7) | 94.2% for 95% at ₹8 Cr (best achievable) |
| 256 | 5.10 s | 1.6 s | exact | 92.7% for 95% |

Notes:
- When the target is out of reach at a budget, mu hits its cap and the engine returns the best achievable availability. This becomes the "Needs ₹X Cr more" feature: bisection on budget at fixed target gives X.
- Allocation can drop below 0.5 s: warm-start lambda from the previous solve, cut outer iterations to 10, use float32 tables, precompute each cell's upper concave hull of (capital, score) so allocation is a sorted sweep (see 04-architecture.md, engine notes).
- Next spike before building the simulator: in-season re-plan on remaining cells at S=64, G=10, target at most 0.6 s.

## How to re-run
```
uv venv -p 3.12 .venv && uv pip install -p .venv numpy scipy highspy
.venv/Scripts/python plan/spikes/decomp_spike.py 128
```
