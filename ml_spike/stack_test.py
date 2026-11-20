"""Weighted stacking vs simple mean (nested CV, honest).
Outer: 10-fold random CV x 3 seeds (headline) + GroupKFold by paper (new lab).
Inside each outer training set: 5-fold OOF predictions of each base model -> non-negative weights summing to 1
(least squares), then base models refit on the whole training set and combined with those weights.
"""
import os, sys, json, time
import numpy as np
from scipy.optimize import nnls
from sklearn.model_selection import KFold, GroupKFold
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from catboost import CatBoostRegressor
from web_data import load, TARGET_FEATURES

X, Y, groups = load()
POWDER = ("SF", "MK", "LP")

def nan1(a): return np.where(np.isnan(a), -1.0, a)
def et(n=100): return ExtraTreesRegressor(n_estimators=n, min_samples_leaf=2, max_features=0.5, n_jobs=-1, random_state=0)
def cb(): return CatBoostRegressor(iterations=800, depth=4, learning_rate=0.05, l2_leaf_reg=3, verbose=0,
                                   random_seed=0, thread_count=8, allow_writing_files=False)
def rf(): return RandomForestRegressor(n_estimators=150, min_samples_leaf=3, max_features=0.5, n_jobs=-1, random_state=0)

class Abr:   # Extra Trees x Abrams curve (= model A on the web)
    def __init__(s, wi): s.wi = wi
    def wp(s, A): return A[:, s.wi[0]] / (1 + A[:, s.wi[1:]].sum(axis=1))
    def fit(s, A, y):
        s.k, s.a = np.polyfit(s.wp(A), np.log(y), 1)
        s.m = et().fit(nan1(A), np.log(y) - s.a - s.k * s.wp(A)); return s
    def predict(s, A): return np.exp(s.m.predict(nan1(A)) + s.a + s.k * s.wp(A))

class Wrap:
    def __init__(s, m, nan=True): s.m, s.nan = m, nan
    def fit(s, A, y): s.m.fit(nan1(A) if s.nan else A, y); return s
    def predict(s, A): return s.m.predict(nan1(A) if s.nan else A)

def weights(P, y):
    w, _ = nnls(P, y); return w / w.sum() if w.sum() > 0 else np.ones(P.shape[1]) / P.shape[1]

def run(key, bases):
    m = Y[key].notna().values; feats = TARGET_FEATURES[key]
    A = X.loc[m, feats].values.astype(float); y = Y[key][m].values; g = groups[m].values
    wi = [feats.index(f) for f in ("Water",) + POWDER]
    mk = {n: (lambda f=f: f(wi)) for n, f in bases.items()}
    names = list(bases)

    def outer(splits):
        P = np.zeros((len(y), len(names))); S = np.zeros(len(y)); W = []
        for tr, te in splits:
            inner = np.zeros((len(tr), len(names)))
            for itr, ite in KFold(5, shuffle=True, random_state=0).split(tr):
                for j, n in enumerate(names):
                    inner[ite, j] = mk[n]().fit(A[tr[itr]], y[tr[itr]]).predict(A[tr[ite]])
            w = weights(inner, y[tr]); W.append(w)
            for j, n in enumerate(names):
                P[te, j] = mk[n]().fit(A[tr], y[tr]).predict(A[te])
            S[te] = P[te] @ w
        return P, S, np.array(W)

    res = {"bases": names, "random": [], "paper": None}
    for sd in range(3):
        P, S, W = outer(KFold(10, shuffle=True, random_state=sd).split(A))
        r = {n: r2_score(y, P[:, j]) for j, n in enumerate(names)}
        r["mean_A_B"] = r2_score(y, P[:, :2].mean(1)); r["mean_all"] = r2_score(y, P.mean(1)); r["stack"] = r2_score(y, S)
        r["mae_mean_A_B"] = mean_absolute_error(y, P[:, :2].mean(1)); r["mae_stack"] = mean_absolute_error(y, S)
        r["w"] = W.mean(0).round(3).tolist(); res["random"].append(r); print(key, sd, r, flush=True)
    P, S, W = outer(GroupKFold(10, shuffle=True, random_state=0).split(A, y, g))
    res["paper"] = {**{n: r2_score(y, P[:, j]) for j, n in enumerate(names)}, "mean_A_B": r2_score(y, P[:, :2].mean(1)),
                    "mean_all": r2_score(y, P.mean(1)), "stack": r2_score(y, S), "w": W.mean(0).round(3).tolist()}
    print(key, "paper", res["paper"], flush=True)
    return res

t = time.time(); out = {}
out["fc"] = run("fc", {"ETxAbrams": lambda wi: Abr(wi), "CatBoost": lambda wi: Wrap(cb(), nan=False),
                       "ET": lambda wi: Wrap(et()), "RF": lambda wi: Wrap(rf())})
out["eps"] = run("eps", {"ET": lambda wi: Wrap(et(300)), "CatBoost": lambda wi: Wrap(cb(), nan=False),
                         "RF": lambda wi: Wrap(rf())})
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "model", "stack_test.json"), "w"), indent=1)
print("done", round(time.time() - t), "s")
