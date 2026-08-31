#!/usr/bin/env python3
"""
Analisis de aneuploidia/CNV SOLO con lo ya extraido (out/baf_pos/*, out/cobertura_bin.tsv).
Sin dependencias, sin red. Rigor:
  - cobertura: MEDIANA de medianas de bins 1Mb, descartando bins pericentromericos
    y outliers (MAD). Ratio vs baseline autosomico.
  - BAF: por cromosoma y por ventana de 5 Mb, mira la distribucion de |BAF-0.5|
    de het SNPs. En region disomica normal la moda esta en ~0 (todos ~0.5).
    Aneuploidia mosaico / CNV / CN-LOH => aparece una segunda moda (banda) a
    |BAF-0.5| > 0.08, y la fraccion de sitios "corridos" sube de forma
    espacialmente coherente (ventanas contiguas).
"""
import os, statistics, math
from collections import defaultdict

OUT = os.path.join(os.path.dirname(__file__), "out")

CHRS = [str(i) for i in range(1, 23)] + ["X", "Y"]
# regiones a enmascarar para cobertura (GRCh38, Mb) -> pericentromero/acrocentrico/seg-dup groseros
MASK = {
    "1": [(120, 149)], "2": [(90, 96)], "3": [(90, 94)], "4": [(49, 52)], "5": [(46, 50)],
    "6": [(58, 62)], "7": [(58, 62)], "8": [(43, 47)], "9": [(38, 66)], "10": [(38, 43)],
    "11": [(50, 55)], "12": [(34, 38)], "13": [(0, 18)], "14": [(0, 18)], "15": [(0, 20)],
    "16": [(35, 47)], "17": [(22, 27)], "18": [(15, 21)], "19": [(24, 29)], "20": [(26, 32)],
    "21": [(0, 13)], "22": [(0, 16)], "X": [(58, 63)], "Y": [(10, 45)],
}
def masked(chrom, b):
    for a, z in MASK.get(chrom, []):
        if a <= b < z:
            return True
    return False

# ---------- COBERTURA ----------
bins = defaultdict(dict)  # chrom -> {binMb: DP_median}
with open(f"{OUT}/cobertura_bin.tsv") as fh:
    next(fh)
    for ln in fh:
        c, b, n, dp = ln.split("\t")
        bins[c][int(b)] = float(dp)

def robust_chr_dp(chrom):
    vals = [dp for b, dp in bins.get(chrom, {}).items() if not masked(chrom, b)]
    if len(vals) < 5:
        return None, 0
    med = statistics.median(vals)
    mad = statistics.median([abs(v - med) for v in vals]) or 1e-9
    clean = [v for v in vals if abs(v - med) <= 5 * 1.4826 * mad]
    return statistics.median(clean), len(clean)

auto_dp = []
chr_dp = {}
for c in [str(i) for i in range(1, 23)]:
    d, nb = robust_chr_dp(c)
    chr_dp[c] = d
    if d:
        auto_dp.append(d)
baseline = statistics.median(auto_dp)

print(f"# COBERTURA  (mediana robusta de bins 1Mb, pericentromero enmascarado)")
print(f"# baseline autosomico DP = {baseline:.1f}")
print(f"# {'chr':>4} {'DP':>7} {'ratio':>7}   interpretacion")
for c in CHRS:
    d, nb = robust_chr_dp(c)
    if not d:
        print(f"  {c:>4}   {'-':>7}   sin datos")
        continue
    r = d / baseline
    tag = ""
    if c not in ("X", "Y"):
        if r > 1.10: tag = f"<<< ganancia (mosaico f~{2*(r-1):.2f} si trisomia)"
        elif r < 0.90: tag = f"<<< perdida (mosaico f~{2*(1-r):.2f} si monosomia)"
    print(f"  {c:>4} {d:>7.1f} {r:>7.3f}   {tag}")

# ---------- BAF por posicion ----------
print(f"\n# BAF  (het SNP PASS DP>=20)  -- por ventana 5 Mb:")
print(f"#   n, mediana|BAF-.5|, y fraccion con |BAF-.5| en bandas:")
print(f"#   [.05,.10) [.10,.15) [.15,.22) [.22,.35)   (region sana: casi todo <.05)")

def analyze_chr_baf(chrom):
    path = f"{OUT}/baf_pos/{chrom}.tsv"
    if not os.path.exists(path):
        return
    win = defaultdict(list)
    with open(path) as fh:
        for ln in fh:
            p, b = ln.split("\t")
            win[int(p) // 5_000_000].append(abs(float(b) - 0.5))
    rows = []
    for w in sorted(win):
        d = win[w]
        if len(d) < 100:
            continue
        n = len(d)
        med = statistics.median(d)
        f1 = sum(1 for x in d if 0.05 <= x < 0.10) / n
        f2 = sum(1 for x in d if 0.10 <= x < 0.15) / n
        f3 = sum(1 for x in d if 0.15 <= x < 0.22) / n
        f4 = sum(1 for x in d if 0.22 <= x < 0.35) / n
        shifted = f2 + f3 + f4  # |BAF-.5| >= .10
        rows.append((w, n, med, f1, f2, f3, f4, shifted))
    if not rows:
        return
    base_shift = statistics.median([r[7] for r in rows])
    flagged = [r for r in rows if r[7] > 0.22 and r[7] > base_shift + 0.06]
    mark = "   <<<<<< REVISAR" if len(flagged) >= 2 else ""
    print(f"\n chr{chrom}  (mediana 'shifted'={base_shift:.3f}){mark}")
    for (w, n, med, f1, f2, f3, f4, sh) in rows:
        fl = " *" if (sh > 0.22 and sh > base_shift + 0.06) else ""
        print(f"   {w*5:3d}-{w*5+5:3d}Mb  n={n:6d}  med={med:.3f}  {f1:.2f} {f2:.2f} {f3:.2f} {f4:.2f}  shift={sh:.2f}{fl}")

for c in CHRS:
    analyze_chr_baf(c)
