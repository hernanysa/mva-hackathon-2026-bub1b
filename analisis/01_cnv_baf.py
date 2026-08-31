#!/usr/bin/env python3
"""
01 - CNV genome-wide + BAF / aneuploidia en mosaico, DIRECTO del VCF (no necesita BAM).

Metodo:
  - Recorre el VCF con pysam. Para cada het SNP bialelica PASS con MQ alto y DP
    en rango normal calcula BAF = AD_alt / (AD_ref + AD_alt).
  - Cobertura: mediana de DP en bins (default 1 Mb), normalizada al baseline
    autosomico, con enmascarado de centromeros/gaps (tabla GRCh38 embebida).
  - Aneuploidia en mosaico: en una region disomica los het estan en BAF~0.5.
    Una trisomia/monosomia/CN-LOH en fraccion f de celulas parte los het en dos
    bandas simetricas |BAF-0.5| = d. Se estima d por ventana (mediana de |BAF-.5|
    de sitios "informativos") y se segmenta. f se deriva de d y del delta de dosis.
  - Salidas: out/cnv_baf/segmentos.tsv, resumen.txt, y figura genome-wide PNG.

Requiere: pysam, numpy, matplotlib.
Uso:  venv/bin/python analisis/01_cnv_baf.py data/WGS_EX2312012_HGWCNDSX7.vcf.gz analisis/out/cnv_baf
"""
import sys, os
import numpy as np
import pysam

VCF = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else "analisis/out/cnv_baf"
os.makedirs(OUT, exist_ok=True)
BIN = 1_000_000

# Centromero (start,end) GRCh38, contigs Ensembl. Fuente: UCSC gap/centromere + brazos acrocentricos.
CENTRO = {
    "1": (121.7, 125.1), "2": (91.8, 96.0), "3": (87.8, 94.1), "4": (48.2, 51.8),
    "5": (46.1, 51.4), "6": (58.5, 62.6), "7": (58.1, 62.1), "8": (43.2, 47.2),
    "9": (42.2, 45.5), "10": (38.8, 42.1), "11": (51.0, 54.4), "12": (33.2, 37.9),
    "13": (0, 18.4), "14": (0, 18.2), "15": (0, 20.5), "16": (35.3, 47.0),
    "17": (22.0, 26.9), "18": (15.4, 21.5), "19": (24.2, 28.7), "20": (26.4, 30.1),
    "21": (0, 13.0), "22": (0, 16.3), "X": (58.1, 63.8), "Y": (10.1, 45.0),
}
CHRS = [str(i) for i in range(1, 23)] + ["X", "Y"]

def in_centro(chrom, pos):
    c = CENTRO.get(chrom)
    if not c:
        return False
    return c[0] * 1e6 <= pos <= c[1] * 1e6

# ---- pasada unica ----
cov = {c: {} for c in CHRS}          # bin -> list DP
baf = {c: {} for c in CHRS}          # bin -> list BAF
het_pos = {c: [] for c in CHRS}      # (pos, baf)

vf = pysam.VariantFile(VCF)
samp = list(vf.header.samples)[0]
print(f"muestra: {samp}", file=sys.stderr)
n = 0
for rec in vf:
    n += 1
    if n % 1_000_000 == 0:
        print(f"  ...{n:,}", file=sys.stderr)
    chrom = rec.chrom
    if chrom not in cov:
        continue
    if rec.filter.keys() and "PASS" not in rec.filter.keys():
        continue
    b = rec.pos // BIN
    g = rec.samples[samp]
    dp = g.get("DP")
    if dp:
        cov[chrom].setdefault(b, []).append(dp)
    # BAF
    if len(rec.alleles) != 2 or len(rec.ref) != 1 or len(rec.alts[0]) != 1:
        continue
    gt = g.get("GT")
    if gt is None or set(gt) != {0, 1}:
        continue
    mq = rec.info.get("MQ", 0)
    if mq < 59:
        continue
    ad = g.get("AD")
    if not ad or len(ad) < 2:
        continue
    tot = ad[0] + ad[1]
    if tot < 20:
        continue
    if in_centro(chrom, rec.pos):
        continue
    v = ad[1] / tot
    baf[chrom].setdefault(b, []).append(v)
    het_pos[chrom].append((rec.pos, v))

# ---- baseline de cobertura ----
def chr_dp(c):
    vals = []
    for b, dps in cov[c].items():
        if in_centro(c, b * BIN + BIN // 2):
            continue
        vals.append(np.median(dps))
    if len(vals) < 5:
        return None
    vals = np.array(vals)
    med = np.median(vals)
    mad = np.median(np.abs(vals - med)) or 1e-9
    vals = vals[np.abs(vals - med) <= 5 * 1.4826 * mad]
    return float(np.median(vals))

autos = [chr_dp(c) for c in CHRS if c not in ("X", "Y")]
baseline = float(np.median([x for x in autos if x]))

# ---- reporte + segmentos ----
seg = open(f"{OUT}/segmentos.tsv", "w")
seg.write("chrom\tinicio_Mb\tfin_Mb\tn_het\tDP_ratio\tBAF_dev_mediana\tf_estimada\tllamado\n")
rep = open(f"{OUT}/resumen.txt", "w")
def out(*a):
    print(*a); print(*a, file=rep)

out(f"# muestra {samp} | {n:,} variantes | baseline DP autosomico = {baseline:.1f}")
out(f"# sexo: chrX ratio={ (chr_dp('X') or 0)/baseline:.2f}  chrY ratio={ (chr_dp('Y') or 0)/baseline:.2f}"
    f"  -> {'XY (masculino)' if (chr_dp('Y') or 0)/baseline > 0.25 else 'XX (femenino)'}")
out("")
out(f"# {'chr':>4} {'DP_ratio':>9} {'BAFdev_med':>11} {'BAFdev_p90':>11} {'n_het':>8}   nota")

WIN = 5_000_000
for c in CHRS:
    dr = (chr_dp(c) or 0) / baseline
    hp = sorted(het_pos[c])
    if not hp:
        out(f"  {c:>4} {dr:>9.3f} {'-':>11} {'-':>11} {0:>8}")
        continue
    devs = np.array([abs(v - 0.5) for _, v in hp])
    dev_med = float(np.median(devs))
    dev_p90 = float(np.percentile(devs, 90))
    note = ""
    if c not in ("X", "Y") and (dr > 1.08 or dr < 0.92):
        note += f" DOSIS alterada (f~{2*abs(dr-1):.2f})"
    # ventanas con desviacion BAF coherente
    pos = np.array([p for p, _ in hp]); vv = np.array([v for _, v in hp])
    flagged = []
    for w0 in range(0, int(pos.max()) + WIN, WIN):
        m = (pos >= w0) & (pos < w0 + WIN)
        if m.sum() < 200:
            continue
        d = np.median(np.abs(vv[m] - 0.5))
        if d > 0.07:  # ~mosaico >8-10%
            flagged.append((w0, w0 + WIN, int(m.sum()), float(d)))
    if len(flagged) >= 2:
        note += f" BAF-split en {len(flagged)} ventanas"
        for (a, z, nh, d) in flagged:
            fest = 2 * d / (1 - 2 * d) if d < 0.49 else 1.0
            seg.write(f"{c}\t{a/1e6:.0f}\t{z/1e6:.0f}\t{nh}\t{dr:.3f}\t{d:.3f}\t{fest:.2f}\tBAF-shift\n")
    out(f"  {c:>4} {dr:>9.3f} {dev_med:>11.3f} {dev_p90:>11.3f} {len(hp):>8}  {note}")

seg.close(); rep.close()

# ---- figura genome-wide ----
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 1, figsize=(16, 7), sharex=True)
    offset = 0
    xticks, xlabels = [], []
    for c in CHRS:
        hp = sorted(het_pos[c])
        if not hp:
            continue
        P = np.array([p for p, _ in hp]) + offset
        V = np.array([v for _, v in hp])
        axes[0].plot(P[::7], V[::7], ",", alpha=0.3)
        # cobertura
        bs = sorted(cov[c])
        cx = [b * BIN + offset for b in bs]
        cy = [np.median(cov[c][b]) / baseline for b in bs]
        axes[1].plot(cx, cy, ".", ms=1)
        span = max(p for p, _ in hp)
        xticks.append(offset + span / 2); xlabels.append(c)
        offset += span + 5e6
    axes[0].set_ylabel("BAF (het SNP)"); axes[0].set_ylim(0, 1)
    axes[0].axhline(0.5, color="k", lw=0.5)
    axes[1].set_ylabel("cobertura / baseline"); axes[1].set_ylim(0, 2)
    axes[1].axhline(1.0, color="k", lw=0.5)
    axes[1].set_xticks(xticks); axes[1].set_xticklabels(xlabels)
    axes[0].set_title(f"{samp}  -  BAF y dosis genome-wide")
    fig.tight_layout()
    fig.savefig(f"{OUT}/genome_wide.png", dpi=110)
    print(f"figura -> {OUT}/genome_wide.png", file=sys.stderr)
except Exception as e:
    print(f"(sin figura: {e})", file=sys.stderr)

print(f"OK -> {OUT}/", file=sys.stderr)
