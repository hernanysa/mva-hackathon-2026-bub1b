#!/usr/bin/env python3
"""
UNA pasada por el VCF (stdin = zcat). Sin dependencias. Extrae y guarda a disco
todo lo necesario para el analisis offline posterior (sin re-escanear):

  out/genes/<GEN>.tsv        : variantes crudas en la ventana del gen (coords GRCh38 exactas)
  out/baf/<CHR>.txt          : una BAF por linea (het SNP PASS, DP>=20) -> para plots/segmentacion
  out/baf_pos/<CHR>.tsv      : POS<TAB>BAF (mismos sitios) -> BAF vs posicion
  out/cobertura_bin.tsv      : CHR, bin_1Mb, n_var, DP_mediana  -> senal de dosis por region
  out/resumen_cromosomas.tsv : CHR, n, n_pass, n_het, BAF_mediana, BAF_MAD, frac_split
  out/meta.txt               : totales

Ventanas de genes: canonical GRCh38 (Ensembl), padding +-5 kb.
"""
import sys, os, statistics
from collections import defaultdict

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
for d in ("genes", "baf", "baf_pos"):
    os.makedirs(f"{OUT}/{d}", exist_ok=True)

PAD = 5000
GENES = {
    # gen: (chrom, start, end)  -- transcripto canonical GRCh38, verificado via Ensembl REST
    "BUB1B":  ("15", 40160984 - PAD, 40221137 + PAD),
    "CEP57":  ("11", 95789965 - PAD, 95837070 + PAD),
    "TRIP13": ("5",    892849 - PAD,   919357 + PAD),
    # (otros genes del panel -> extraccion targeted con tabix despues de la descarga,
    #  verificando coords una por una; no meto coords de memoria aca)
}
gfh = {g: open(f"{OUT}/genes/{g}.tsv", "w") for g in GENES}
for fh in gfh.values():
    fh.write("CHROM\tPOS\tREF\tALT\tQUAL\tFILTER\tGT\tAD\tDP\tGQ\tINFO\n")

baffh = {}       # chrom -> file handle (baf/<chr>.txt)
bafposfh = {}
def bh(chrom):
    if chrom not in baffh:
        baffh[chrom] = open(f"{OUT}/baf/{chrom}.txt", "w")
        bafposfh[chrom] = open(f"{OUT}/baf_pos/{chrom}.tsv", "w")
    return baffh[chrom], bafposfh[chrom]

per_chr = defaultdict(lambda: {"n": 0, "pass": 0, "het": 0, "baf": []})
covbin = defaultdict(list)   # (chrom, bin) -> [DP,...]
n = 0
MAIN = set(str(i) for i in range(1, 23)) | {"X", "Y"}

for line in sys.stdin:
    if line[0] == "#":
        continue
    n += 1
    if n % 1_000_000 == 0:
        print(f"  ...{n:,}", file=sys.stderr)
    f = line.rstrip("\n").split("\t")
    if len(f) < 10:
        continue
    chrom, pos, ref, alt, qual, filt, info, fmt, sample = f[0], int(f[1]), f[3], f[4], f[5], f[6], f[7], f[8], f[9]
    sv = dict(zip(fmt.split(":"), sample.split(":")))
    gt = sv.get("GT", "./."); ad = sv.get("AD", ""); dp = sv.get("DP", ""); gq = sv.get("GQ", "")

    for g, (gc, g0, g1) in GENES.items():
        if chrom == gc and g0 <= pos <= g1:
            gfh[g].write(f"{chrom}\t{pos}\t{ref}\t{alt}\t{qual}\t{filt}\t{gt}\t{ad}\t{dp}\t{gq}\t{info}\n")

    if chrom not in MAIN:
        continue
    c = per_chr[chrom]; c["n"] += 1
    is_pass = filt in ("PASS", ".")
    if not is_pass:
        continue
    c["pass"] += 1
    try:
        dpi = int(dp)
        covbin[(chrom, pos // 1_000_000)].append(dpi)
    except ValueError:
        pass
    # BAF de het SNP bialelica PASS, DP alto
    if gt not in ("0/1", "0|1", "1|0"):
        continue
    if len(ref) != 1 or len(alt) != 1 or alt == "*":
        continue
    try:
        a0, a1 = (int(x) for x in ad.split(",")[:2])
    except ValueError:
        continue
    tot = a0 + a1
    if tot < 20:
        continue
    baf = a1 / tot
    c["het"] += 1
    if len(c["baf"]) < 200000:
        c["baf"].append(baf)
    b1, b2 = bh(chrom)
    b1.write(f"{baf:.4f}\n")
    b2.write(f"{pos}\t{baf:.4f}\n")

for fh in list(gfh.values()) + list(baffh.values()) + list(bafposfh.values()):
    fh.close()

# resumen por cromosoma
def mad(xs, med):
    return statistics.median([abs(x - med) for x in xs]) if xs else 0.0

rc = open(f"{OUT}/resumen_cromosomas.tsv", "w")
rc.write("CHROM\tn\tn_pass\tn_het\tBAF_mediana\tBAF_MAD\tfrac_split_0.60_0.75\n")
CHR_ORDER = [str(i) for i in range(1, 23)] + ["X", "Y"]
for chrom in sorted(per_chr, key=lambda c: CHR_ORDER.index(c) if c in CHR_ORDER else 99):
    c = per_chr[chrom]; bafs = c["baf"]
    if bafs:
        med = statistics.median(bafs)
        m = mad(bafs, med)
        # fraccion de het con |BAF-0.5| en [0.10,0.25]  -> tipico de aneuploidia mosaico
        split = sum(1 for x in bafs if 0.10 <= abs(x - 0.5) <= 0.25) / len(bafs)
    else:
        med = m = split = 0.0
    rc.write(f"{chrom}\t{c['n']}\t{c['pass']}\t{c['het']}\t{med:.4f}\t{m:.4f}\t{split:.4f}\n")
rc.close()

cb = open(f"{OUT}/cobertura_bin.tsv", "w")
cb.write("CHROM\tbin_Mb\tn_var\tDP_mediana\n")
for (chrom, b), dps in sorted(covbin.items(), key=lambda kv: (CHR_ORDER.index(kv[0][0]) if kv[0][0] in CHR_ORDER else 99, kv[0][1])):
    cb.write(f"{chrom}\t{b}\t{len(dps)}\t{statistics.median(dps):.1f}\n")
cb.close()

open(f"{OUT}/meta.txt", "w").write(f"total_variantes\t{n}\n")
print(f"OK  {n:,} variantes procesadas  ->  {OUT}/", file=sys.stderr)
