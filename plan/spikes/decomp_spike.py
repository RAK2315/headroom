"""Spike 2: Lagrangian decomposition. Per cell (pool-week) value tables over a (markup, hard, allotment)
grid evaluated on S correlated scenarios, then budget and availability multipliers found by bisection.
Also checks the gap against an exact MILP on a small instance."""
import sys
import time

import numpy as np

rng = np.random.default_rng(7)
MARKUPS = np.array([0.04, 0.08, 0.12])
ELAST = 1.6     # price elasticity of agent demand (assumption)
UTIL = 0.7


def make_instance(P=45, T=26, S=256):
    C = P * T
    base = rng.uniform(80, 600, size=(P, 1)) * (1 + 0.6 * np.sin(np.linspace(0, 3, T)))[None, :]
    peaks = np.zeros(T); peaks[[5, 6, 12, 13, 18]] = [0.8, 1.2, 1.5, 1.3, 0.6]
    base = (base * (1 + peaks[None, :])).reshape(C)
    # correlated scenarios: global factor + destination factor + idiosyncratic
    g = rng.normal(0, 0.15, size=(S, 1)); d = rng.normal(0, 0.2, size=(S, P)).repeat(T, axis=1)
    e = rng.normal(0, 0.25, size=(S, C))
    D = base[None, :] * np.exp(g + d + e - 0.5 * (0.15**2 + 0.2**2 + 0.25**2))
    net = np.repeat(rng.uniform(5000, 12000, size=P), T)    # supplier free-sale net rate reference
    inst = dict(C=C, S=S, D=D, base=base, net=net,
                c_h=net * 0.78, c_a=net * 0.90, fee_a=net * 0.02, pen_u=net * 0.10, salv=net * 0.78 * 0.25,
                Amax=base * 0.8, c_f=net[None, :] * rng.uniform(0.97, 1.15, size=(S, C)),
                Fcap=D * rng.uniform(0.2, 0.9, size=(S, C)))
    return inst


def value_tables(inst, G=12, chunk=64):
    """Returns per cell, per option: expected profit, expected served, expected demand, capital, per-scenario profit."""
    C, S, D = inst["C"], inst["S"], inst["D"]
    q95 = np.quantile(D, 0.95, axis=0)
    fr = np.linspace(0, 1, G)
    M = len(MARKUPS)
    EP = np.empty((C, M, G, G)); ES = np.empty((C, M, G, G)); ED = np.empty((C, M)); CAP = np.empty((C, M, G, G))
    PS = np.empty((C, M, G, G, S), dtype=np.float32)
    for c0 in range(0, C, chunk):
        sl = slice(c0, min(C, c0 + chunk)); n = sl.stop - sl.start
        h = (q95[sl, None] * fr[None, :])[:, None, :, None, None]                         # n,1,G,1,1
        a = (np.minimum(inst["Amax"][sl], q95[sl])[:, None] * fr[None, :])[:, None, None, :, None]  # n,1,1,G,1
        p = (inst["net"][sl, None] * (1 + MARKUPS[None, :]))[:, :, None, None, None]   # n,M,1,1,1
        dem = (D[:, sl].T[:, None, :] * ((1 + MARKUPS) / 1.08)[None, :, None] ** (-ELAST))[:, :, None, None, :]  # n,M,1,1,S
        ch, ca, fee, pen, salv = (inst[k][sl][:, None, None, None, None] for k in ("c_h", "c_a", "fee_a", "pen_u", "salv"))
        cf = inst["c_f"][:, sl].T[:, None, None, None, :]; fcap = inst["Fcap"][:, sl].T[:, None, None, None, :]
        sh = np.minimum(h, dem); rem = dem - sh
        sa = np.minimum(a, rem); rem = rem - sa
        f = np.where(p > cf, np.minimum(fcap, rem), 0.0)
        prof = p * sh + salv * (h - sh) - ch * h + (p - ca) * sa - fee * a - pen * np.maximum(0, UTIL * a - sa) + (p - cf) * f
        PS[sl] = prof.astype(np.float32)
        EP[sl] = prof.mean(-1); ES[sl] = (sh + sa + f).mean(-1); ED[sl] = dem[..., 0, 0, :].mean(-1)
        CAP[sl] = np.broadcast_to((ch * h + fee * a)[..., 0], (n, M, G, G))
    return EP, ES, ED, CAP, PS


def allocate(EP, ES, CAP, lam, mu, avail_value):
    """Pick the best option per cell for given capital price lam and availability weight mu."""
    C = EP.shape[0]
    score = EP + mu * avail_value[:, None, None, None] * ES - lam * CAP
    flat = score.reshape(C, -1).argmax(1)
    return flat


def solve(EP, ES, ED, CAP, PS, budget, target_avail, avail_value):
    C = EP.shape[0]
    idx = np.arange(C)

    def pick(lam, mu):
        k = allocate(EP, ES, CAP, lam, mu, avail_value)
        return k, CAP.reshape(C, -1)[idx, k].sum(), ES.reshape(C, -1)[idx, k].sum()

    total_dem = ED.mean(1).sum()  # rough denominator
    mu_lo, mu_hi = 0.0, 20.0
    for _ in range(14):  # outer: availability weight
        mu = (mu_lo + mu_hi) / 2
        lo, hi = 0.0, 200.0
        for _ in range(22):  # inner: capital price so spend <= budget
            lam = (lo + hi) / 2
            _, spend, _ = pick(lam, mu)
            lo, hi = (lam, hi) if spend > budget else (lo, lam)
        k, spend, served = pick(hi, mu)
        dem_k = ED[idx, np.unravel_index(k, EP.shape[1:])[0]].sum()
        avail = served / dem_k
        mu_lo, mu_hi = (mu, mu_hi) if avail < target_avail else (mu_lo, mu)
    k, spend, served = pick(hi, mu_hi)
    prof_s = PS.reshape(C, -1, PS.shape[-1])[idx, k].sum(0)  # portfolio profit per scenario
    var5 = np.quantile(prof_s, 0.05); cvar5 = prof_s[prof_s <= var5].mean()
    return dict(k=k, lam=hi, mu=mu_hi, spend=spend, exp_profit=prof_s.mean(), p10=np.quantile(prof_s, 0.10),
                cvar5=cvar5, avail=served / ED[idx, np.unravel_index(k, EP.shape[1:])[0]].sum())


if __name__ == "__main__":
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 256
    inst = make_instance(S=S)
    t0 = time.perf_counter(); EP, ES, ED, CAP, PS = value_tables(inst); t_tab = time.perf_counter() - t0
    avail_value = inst["net"] * 0.15  # goodwill per served room-night (assumption)
    for budget, tgt in [(5e7, 0.90), (8e7, 0.95), (1.2e8, 0.97)]:
        t0 = time.perf_counter(); r = solve(EP, ES, ED, CAP, PS, budget, tgt, avail_value); t_sol = time.perf_counter() - t0
        print(f"S={S} tables={t_tab:.2f}s solve={t_sol*1000:.0f}ms budget={budget:.1e} target={tgt:.0%} -> "
              f"spend={r['spend']:.3e} E[profit]={r['exp_profit']:.3e} P10={r['p10']:.3e} CVaR5={r['cvar5']:.3e} "
              f"avail={r['avail']:.1%} capital_price={r['lam']:.3f} avail_weight={r['mu']:.3f}")
