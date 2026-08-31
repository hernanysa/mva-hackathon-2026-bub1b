#!/usr/bin/env python3
"""
Inspeccion en UNA pasada del VCF del probando (stdin = zcat del .vcf.gz).
No necesita dependencias (solo stdlib). Saca:
  - conteo de variantes por cromosoma y por FILTER
  - BAF (B-allele frequency) de SNPs heterocigotas PASS por cromosoma
    -> preview de aneuploidia en mosaico: en un cromosoma diploide sano
       los het estan centrados en 0.5; una trisomia/monosomia en mosaico
       parte esa distribucion (bimodal, corrida) segun la fraccion de celulas.
  - dump de TODAS las variantes en las ventanas de los genes candidatos
    (BUB1B / CEP57 / TRIP13, coordenadas GRCh38, contigs estilo Ensembl "15" no "chr15")

Uso:
  zcat data/WGS_EX2312012_HGWCNDSX7.vcf.gz | python3 analisis/inspeccion_vcf.py analisis/out
"""
import sys
from collections import defaultdict

OUTDIR = sys.argv[1] if len(sys.argv) > 1 else "."

# Ventanas GENEROSAS (GRCh38). Se refinan despues con coords exactas de Ensembl.
GENES = {
    "BUB1B":  ("15", 40_140_000, 40_240_000),
    "CEP57":  ("11", 95_760_000, 95_840_000),
    "TRIP13": ("5",     480_000,   580_000),
}
gene_fh = {g: open(f"{OUTDIR}/variantes_{g}.tsv", "w") for g in GENES}
for g, fh in gene_fh.items():
    fh.write("CHROM\tPOS\tREF\tALT\tQUAL\tFILTER\tGT\tAD\tDP\tINFO\n")

per_chr = defaultdict(lambda: {"n": 0, "pass": 0, "het_snp": 0})
filt_counts = defaultdict(int)
# histograma de BAF por cromosoma (bins de 0.05)
baf_hist = defaultdict(lambda: [0] * 20)
baf_vals = defaultdict(list)  # guardo algunos para percentiles (cap para no explotar RAM)

n = 0
for line in sys.stdin:
    if line.startswith("#"):
        continue
    n += 1
    if n % 500_000 == 0:
        print(f"  ... {n:,} variantes", file=sys.stderr)
    f = line.rstrip("\n").split("\t")
    if len(f) < 10:
        continue
    chrom, pos, _id, ref, alt, qual, filt, info, fmt, sample = f[:10]
    pos = int(pos)
    c = per_chr[chrom]
    c["n"] += 1
    filt_counts[filt] += 1
    is_pass = filt in ("PASS", ".")
    if is_pass:
        c["pass"] += 1

    # parse sample
    fmt_keys = fmt.split(":")
    sv = dict(zip(fmt_keys, sample.split(":")))
    gt = sv.get("GT", "./.")
    ad = sv.get("AD", "")
    dp = sv.get("DP", "")

    # dump genes candidatos (sin filtrar por calidad: queremos ver todo)
    for g, (gc, g0, g1) in GENES.items():
        if chrom == gc and g0 <= pos <= g1:
            gene_fh[g].write(f"{chrom}\t{pos}\t{ref}\t{alt}\t{qual}\t{filt}\t{gt}\t{ad}\t{dp}\t{info}\n")

    # BAF de het SNP PASS, bialelicas, DP decente
    if not is_pass:
        continue
    if gt not in ("0/1", "0|1", "1|0"):
        continue
    if len(ref) != 1 or len(alt) != 1 or alt == "*":
        continue
    try:
        ad_ref, ad_alt = (int(x) for x in ad.split(",")[:2])
    except ValueError:
        continue
    tot = ad_ref + ad_alt
    if tot < 10:
        continue
    baf = ad_alt / tot
    c["het_snp"] += 1
    b = min(int(baf / 0.05), 19)
    baf_hist[chrom][b] += 1
    if len(baf_vals[chrom]) < 20000:
        baf_vals[chrom].append(baf)

# ---- reporte ----
def median(xs):
    xs = sorted(xs)
    m = len(xs)
    return None if m == 0 else (xs[m // 2] if m % 2 else (xs[m // 2 - 1] + xs[m // 2]) / 2)

CHR_ORDER = [str(i) for i in range(1, 23)] + ["X", "Y", "MT"]
def chrkey(c):
    cc = c.replace("chr", "")
    return CHR_ORDER.index(cc) if cc in CHR_ORDER else 99

rep = open(f"{OUTDIR}/resumen.txt", "w")
def out(*a):
    print(*a); print(*a, file=rep)

out(f"# Total variantes: {n:,}")
out(f"\n# FILTER (top):")
for k, v in sorted(filt_counts.items(), key=lambda x: -x[1])[:15]:
    out(f"  {v:>10,}  {k}")

out(f"\n# Por cromosoma:  variantes / PASS / het-SNP(DP>=10) / BAF mediana / % het en bandas 0.30-0.42 & 0.58-0.70 (senal mosaico)")
for chrom in sorted(per_chr, key=chrkey):
    c = per_chr[chrom]
    bv = baf_vals[chrom]
    med = median(bv)
    h = baf_hist[chrom]
    tot_h = sum(h) or 1
    # bandas: [0.30,0.42) -> bins 6,7,8 ; [0.58,0.70) -> bins 11,12,13
    side = (h[6] + h[7] + h[8] + h[11] + h[12] + h[13]) / tot_h
    center = (h[9] + h[10]) / tot_h  # [0.45,0.55)
    flag = "  <<< revisar" if (c["het_snp"] > 500 and side > 0.55 and side > center) else ""
    med_s = f"{med:.3f}" if med is not None else "  -  "
    out(f"  {chrom:>3}  {c['n']:>9,} {c['pass']:>9,} {c['het_snp']:>9,}   {med_s}   side={side:.2f} center={center:.2f}{flag}")

out(f"\n# Variantes en genes candidatos -> {OUTDIR}/variantes_<GEN>.tsv")
for g in GENES:
    gene_fh[g].close()
import os
for g in GENES:
    nl = sum(1 for _ in open(f"{OUTDIR}/variantes_{g}.tsv")) - 1
    out(f"  {g:8} ventana {GENES[g][0]}:{GENES[g][1]:,}-{GENES[g][2]:,}  -> {nl} variantes")
rep.close()
print(f"\nescrito: {OUTDIR}/resumen.txt", file=sys.stderr)
