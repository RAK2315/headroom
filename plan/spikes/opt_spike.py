"""Spike: two-stage stochastic MILP (hard pre-buy + allotment + free-sale recourse, supplier
integration binaries, CVaR, availability penalty). Measures build + solve time at demo sizes."""
import sys
import time

import numpy as np
import scipy.sparse as sp
from scipy.optimize import Bounds, LinearConstraint, milp

rng = np.random.default_rng(7)


def build_and_solve(P=45, T=26, S=100, K=6, budget=8e7, beta=0.3, alpha=0.95,
                    avail_pen=1500.0, util=0.7, time_limit=60):
    C = P * T
    # demand scenarios (room-nights per pool-week), seasonal with peaks, lognormal noise
    base = rng.uniform(80, 600, size=(P, 1)) * (1 + 0.6 * np.sin(np.linspace(0, 3, T)))[None, :]
    peaks = np.zeros(T); peaks[[5, 6, 12, 13, 18]] = [0.8, 1.2, 1.5, 1.3, 0.6]
    base = base * (1 + peaks[None, :])
    D = base.reshape(C)[None, :] * rng.lognormal(0, 0.35, size=(S, C))
    price = np.repeat(rng.uniform(5500, 14000, size=P), T)
    c_h = price * 0.70            # hard pre-buy net rate (cheapest, paid upfront)
    c_a = price * 0.82            # allotment net rate, paid only when sold
    fee_a = price * 0.02          # allotment holding fee per room
    pen_u = price * 0.10          # under-utilisation penalty per room below util share
    salv = c_h * 0.25             # resale salvage of unsold hard rooms
    Amax = base.reshape(C) * 0.8  # hotel willingness to give allotment
    c_f = price[None, :] * rng.uniform(0.88, 1.02, size=(S, C))   # free-sale rate
    Fcap = D * rng.uniform(0.2, 0.9, size=(S, C))                 # free-sale availability (close-outs)
    boost = (rng.random((K, C)) < 0.25) * rng.uniform(20, 120, size=(K, C))  # capacity added by supplier k
    int_cost = rng.uniform(2e6, 6e6, size=K)

    # variable layout: h[C], a[C], u[K], eta, then per scenario: sh[C], sa[C], f[C], w[C], z
    n1 = 2 * C + K + 1
    per = 4 * C + 1
    n = n1 + S * per
    ih, ia, iu, ieta = 0, C, 2 * C, 2 * C + K

    def off(s):
        return n1 + s * per

    c = np.zeros(n)  # minimise negative objective
    # expected profit pieces
    c[ih:ih + C] = c_h - salv          # each hard room costs c_h, salvage if unsold handled via sh coeff
    c[ia:ia + C] = fee_a
    c[iu:iu + K] = int_cost
    for s in range(S):
        o = off(s)
        # served from hard: revenue price, recover salvage loss (sold rooms don't get salvaged)
        # hard cost (c_h - salv) is charged on every bought room; a sold room earns price but forgoes salvage
        c[o:o + C] = -(price - salv) / S
        c[o + C:o + 2 * C] = -(price - c_a) / S
        c[o + 2 * C:o + 3 * C] = -(price - c_f[s]) / S
        c[o + 3 * C:o + 4 * C] = pen_u / S
        # availability: penalise every unserved unit -> equivalent to reward avail_pen per served unit
        c[o:o + 3 * C] -= avail_pen / S
        c[o + 4 * C] = beta / ((1 - alpha) * S)
    c[ieta] = beta

    rows, cols, vals, lo, hi = [], [], [], [], []
    r = 0

    def add(rr, cc, vv):
        rows.extend(rr); cols.extend(cc); vals.extend(vv)

    I = np.arange(C)
    # budget: sum c_h*h + fee_a*a + int_cost*u <= budget
    add([r] * C, ih + I, c_h); add([r] * C, ia + I, fee_a); add([r] * K, iu + np.arange(K), int_cost)
    lo.append(-np.inf); hi.append(budget); r += 1
    for s in range(S):
        o = off(s)
        rr = r + I
        # served <= demand
        add(np.tile(rr, 3), np.concatenate([o + I, o + C + I, o + 2 * C + I]), np.ones(3 * C))
        lo.extend([-np.inf] * C); hi.extend(D[s]); r += C
        # sh <= h
        rr = r + I; add(np.tile(rr, 2), np.concatenate([o + I, ih + I]), np.concatenate([np.ones(C), -np.ones(C)]))
        lo.extend([-np.inf] * C); hi.extend([0] * C); r += C
        # sa <= a
        rr = r + I; add(np.tile(rr, 2), np.concatenate([o + C + I, ia + I]), np.concatenate([np.ones(C), -np.ones(C)]))
        lo.extend([-np.inf] * C); hi.extend([0] * C); r += C
        # f <= Fcap + sum_k boost*u
        rr = r + I; add(rr, o + 2 * C + I, np.ones(C))
        kk, cc = np.nonzero(boost)
        add(r + cc, iu + kk, -boost[kk, cc])
        lo.extend([-np.inf] * C); hi.extend(Fcap[s]); r += C
        # w >= util*a - sa  ->  util*a - sa - w <= 0
        rr = r + I
        add(np.tile(rr, 3), np.concatenate([ia + I, o + C + I, o + 3 * C + I]),
            np.concatenate([np.full(C, util), -np.ones(C), -np.ones(C)]))
        lo.extend([-np.inf] * C); hi.extend([0] * C); r += C
        # CVaR: z_s >= -profit_s - eta  ->  -profit_s - eta - z_s <= 0
        # profit_s = sum price*sh + (price-c_a)*sa + (price-c_f)*f - pen_u*w - (c_h-salv)*h - fee_a*a - int_cost*u
        add([r] * C, o + I, -(price - salv)); add([r] * C, o + C + I, -(price - c_a)); add([r] * C, o + 2 * C + I, -(price - c_f[s]))
        add([r] * C, o + 3 * C + I, pen_u); add([r] * C, ih + I, c_h - salv); add([r] * C, ia + I, fee_a)
        add([r] * K, iu + np.arange(K), int_cost); add([r], [ieta], [-1.0]); add([r], [o + 4 * C], [-1.0])
        lo.append(-np.inf); hi.append(0); r += 1

    t0 = time.perf_counter()
    A = sp.csr_matrix((vals, (rows, cols)), shape=(r, n))
    lb = np.zeros(n); ub = np.full(n, np.inf)
    ub[ia:ia + C] = Amax; ub[iu:iu + K] = 1; lb[ieta] = -np.inf
    integ = np.zeros(n); integ[iu:iu + K] = 1
    t_build = time.perf_counter() - t0
    t0 = time.perf_counter()
    res = milp(c, constraints=LinearConstraint(A, lo, hi), bounds=Bounds(lb, ub), integrality=integ,
               options={"time_limit": time_limit, "mip_rel_gap": 0.005, "disp": False})
    t_solve = time.perf_counter() - t0
    x = res.x
    served = 0; dem = D.sum()
    if x is not None:
        for s in range(S):
            o = off(s); served += x[o:o + 3 * C].sum()
    print(f"P={P} T={T} S={S} vars={n:,} rows={r:,} nnz={A.nnz:,} build={t_build:.2f}s solve={t_solve:.2f}s "
          f"status={res.status} obj={-res.fun if res.fun is not None else None:.3e} "
          f"hard={x[ih:ih+C].sum():,.0f} allot={x[ia:ia+C].sum():,.0f} suppliers={np.round(x[iu:iu+K]).astype(int).tolist()} "
          f"avail={served/dem:.1%}", flush=True)


if __name__ == "__main__":
    for S in [int(v) for v in sys.argv[1:]] or [32, 64, 128]:
        build_and_solve(S=S)
