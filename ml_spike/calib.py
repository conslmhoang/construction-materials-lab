import sys
src=open('spike.py',encoding='utf-8').read()
exec(src.split("lines, curves = [], {}")[0])
rng=np.random.default_rng(1)
for tname,(y,mask) in targets.items():
    m=mask&y.notna(); Xm=X[m].values.astype(float); ym=y[m].values; gm=groups_all[m].values
    pred=np.zeros(len(ym))
    for tr,te in GroupKFold(10).split(Xm,ym,gm): pred[te]=fp(Xm[tr],ym[tr],Xm[te])
    res=ym-pred
    out={0:[],1:[],2:[],3:[]}
    for g in np.unique(gm):
        idx=np.where(gm==g)[0]
        if len(idx)<5: continue
        for rep in range(20):
            p=rng.permutation(idx)
            for k in out:
                cal,ev=p[:k],p[3:]          # always evaluate on same rows (all except first 3)
                corr=res[cal].mean() if k else 0
                out[k].append(np.mean(np.abs(ym[ev]-(pred[ev]+corr))/ym[ev]))
    print(tname, '  '.join(f'{k} own-lab mixes→{np.mean(v)*100:.0f}%' for k,v in out.items()))
