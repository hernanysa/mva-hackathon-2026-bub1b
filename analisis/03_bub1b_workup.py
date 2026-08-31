#!/usr/bin/env python3
"""
03 - Workup de BUB1B + contexto genomico.
  a) perfil de cobertura (DP) exon-por-exon de BUB1B  -> descarta delecion het como 2do alelo
  b) ROH / homocigosidad: tramos largos sin het SNP (consanguinidad / UPD / delecion)
  c) todas las variantes raras (no-DB) en BUB1B con su VEP
  d) ClinVar detallado (via VEP colocated) de los candidatos
"""
import sys, os, json, urllib.request
import numpy as np
import pysam

VCF = sys.argv[1]
vf = pysam.VariantFile(VCF)
S = list(vf.header.samples)[0]

BUB1B = ("15", 40160984, 40221137)

# --- a) cobertura exon-por-exon: transcript canonical ENST00000287598 desde Ensembl ---
def ensembl(path):
    req = urllib.request.Request("https://rest.ensembl.org" + path,
                                 headers={"Accept": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=30))

try:
    tr = ensembl("/overlap/region/human/15:40160984-40221137?feature=exon;content-type=application/json")
    exons = sorted({(e["start"], e["end"]) for e in tr if e.get("Parent") == "ENST00000287598"})
    if not exons:
        exons = sorted({(e["start"], e["end"]) for e in tr})
except Exception as e:
    print(f"(sin exones Ensembl: {e})")
    exons = []

print(f"# COBERTURA BUB1B por exon (canonical ENST00000287598, {len(exons)} exones)")
print(f"# {'exon':>4} {'start':>10} {'end':>10} {'DP_medio':>9} {'DP_min':>7}   (het delecion -> ~0.5x del entorno)")
alldp = []
for i, (a, b) in enumerate(exons, 1):
    dps = []
    for rec in vf.fetch("15", a - 1, b):
        g = rec.samples[S]
        if g.get("DP"):
            dps.append(g["DP"])
    if dps:
        alldp += dps
        print(f"  {i:>4} {a:>10} {b:>10} {np.mean(dps):>9.1f} {min(dps):>7}")
if alldp:
    print(f"  --> BUB1B DP global: media {np.mean(alldp):.1f}, mediana {np.median(alldp):.0f}")

# --- b) ROH genome-wide: bins de 1 Mb, fraccion de sitios que son het ---
print(f"\n# ROH / homocigosidad (bins 1 Mb: si %het << normal -> tramo homocigoto)")
from collections import defaultdict
binstat = defaultdict(lambda: [0, 0])  # (chrom,bin) -> [n_var_bialelica, n_het]
CH = set(str(i) for i in range(1, 23))
vf2 = pysam.VariantFile(VCF)
n = 0
for rec in vf2:
    if rec.chrom not in CH:
        continue
    if rec.filter.keys() and "PASS" not in rec.filter.keys():
        continue
    if len(rec.alleles) != 2 or len(rec.ref) != 1 or len(rec.alts[0]) != 1:
        continue
    g = rec.samples[S]
    gt = g.get("GT")
    if gt is None or 1 not in gt:
        continue
    k = (rec.chrom, rec.pos // 1_000_000)
    binstat[k][0] += 1
    if set(gt) == {0, 1}:
        binstat[k][1] += 1

# fraccion het tipica
fr = [h / t for (t, h) in binstat.values() if t >= 20]
med_fr = float(np.median(fr))
roh = []
cur = None
for (chrom, b) in sorted(binstat, key=lambda x: ([str(i) for i in range(1,23)].index(x[0]), x[1])):
    t, h = binstat[(chrom, b)]
    if t < 20:
        continue
    f = h / t
    is_roh = f < 0.25 * med_fr
    if is_roh:
        if cur and cur[0] == chrom and b - cur[2] <= 2:
            cur[2] = b
        else:
            if cur and cur[2] - cur[1] >= 2:
                roh.append(tuple(cur))
            cur = [chrom, b, b]
if cur and cur[2] - cur[1] >= 2:
    roh.append(tuple(cur))

print(f"  fraccion het mediana genome-wide: {med_fr:.3f}")
if roh:
    tot = 0
    for (c, a, z) in roh:
        mb = z - a + 1
        tot += mb
        print(f"  ROH  chr{c}:{a}-{z+1} Mb  (~{mb} Mb)")
    print(f"  --> total en ROH: ~{tot} Mb  {'(consanguinidad probable)' if tot > 50 else '(bajo; sin consanguinidad marcada)'}")
else:
    print(f"  sin tramos ROH significativos -> sin consanguinidad; het compuesta es el modelo esperado")

# --- c) variantes raras en BUB1B ---
print(f"\n# Variantes NO-dbSNP (raras/novel) en BUB1B:")
vf3 = pysam.VariantFile(VCF)
for rec in vf3.fetch(*BUB1B):
    if rec.filter.keys() and "PASS" not in rec.filter.keys():
        continue
    g = rec.samples[S]
    gt = g.get("GT")
    if gt is None or set(gt) == {0}:
        continue
    if "DB" in rec.info:
        continue
    print(f"  15:{rec.pos} {rec.ref}>{rec.alts[0]}  GT={gt} AD={g.get('AD')} DP={g.get('DP')}")
