#!/usr/bin/env python3
"""
Analiza align/bub1b.bam (extraccion dirigida). Responde:
  1. cobertura exon por exon -> hay delecion heterocigota? (exon a ~50% de sus vecinos)
  2. confirmacion de las 2 variantes desde lecturas crudas (conteo por alelo y hebra,
     MAPQ, BASEQ)
  3. lecturas con soft-clip grande / pares discordantes -> senal de SV local
Requiere: pysam. Uso:  venv/bin/python align/05_analisis_bam.py
"""
import json, os, statistics, collections
import pysam

HERE = os.path.dirname(__file__)
BAM = os.path.join(HERE, "bub1b.bam")
EX = json.load(open(os.path.join(HERE, "bub1b_exones.json")))
CHROM = "15"

VARS = [
    ("p.Leu737Ter  c.2210T>G  (nonsense, exon 17, ClinVar Patogenica)", 40209701, "T", "G"),
    ("p.Asn1002Lys c.3006T>G  (missense, exon 23, novel)",              40220612, "T", "G"),
]

bam = pysam.AlignmentFile(BAM, "rb")

# ---------- 1. cobertura por exon ----------
print("=" * 70)
print("1. COBERTURA EXON POR EXON  (delecion het -> exon a ~0.5x de la mediana)")
print("=" * 70)
exon_med = []
rows = []
for e in EX["exons"]:
    depths = []
    for col in bam.pileup(CHROM, e["start"] - 1, e["end"], truncate=True, min_base_quality=0, stepper="nofilter"):
        depths.append(col.nsegments)
    # rellenar posiciones sin cobertura
    covered = len(depths)
    total = e["end"] - e["start"] + 1
    depths += [0] * (total - covered)
    med = statistics.median(depths) if depths else 0
    mn = min(depths) if depths else 0
    exon_med.append(med)
    rows.append((e["n"], e["start"], e["end"], total, med, mn, covered / total))

gene_med = statistics.median([m for m in exon_med if m > 0]) or 1
print(f"\nmediana de cobertura del gen (exones): {gene_med:.0f}x\n")
print(f" {'exon':>4} {'rango':>22} {'bp':>4} {'cob.med':>8} {'min':>5} {'%cubierto':>10} {'ratio':>6}  flag")
for (n, s, en, total, med, mn, frac) in rows:
    ratio = med / gene_med
    flag = ""
    if ratio < 0.60: flag = "<<< POSIBLE DELECION HET"
    elif ratio > 1.75: flag = "<<< posible duplicacion"
    elif frac < 0.80: flag = "(baja cobertura - repeat/mapa)"
    print(f" {n:>4} {s:>10}-{en:<10} {total:>4} {med:>8.0f} {mn:>5} {frac*100:>9.0f}% {ratio:>6.2f}  {flag}")

# ---------- 2. confirmacion de variantes ----------
print("\n" + "=" * 70)
print("2. CONFIRMACION DE VARIANTES  (desde lecturas crudas)")
print("=" * 70)
for label, pos, ref, alt in VARS:
    print(f"\n--- {label}")
    print(f"    15:{pos}  {ref}>{alt}")
    counts = collections.Counter()
    strand = {"ref_fwd": 0, "ref_rev": 0, "alt_fwd": 0, "alt_rev": 0}
    mapqs = {"ref": [], "alt": []}
    baseqs = {"ref": [], "alt": []}
    for col in bam.pileup(CHROM, pos - 1, pos, truncate=True, min_base_quality=0, stepper="samtools",
                          ignore_orphans=False):
        if col.reference_pos != pos - 1:
            continue
        for pr in col.pileups:
            if pr.is_del or pr.is_refskip or pr.query_position is None:
                counts["indel/skip"] += 1
                continue
            b = pr.alignment.query_sequence[pr.query_position].upper()
            bq = pr.alignment.query_qualities[pr.query_position]
            mq = pr.alignment.mapping_quality
            rev = pr.alignment.is_reverse
            counts[b] += 1
            if b == ref:
                strand["ref_rev" if rev else "ref_fwd"] += 1
                mapqs["ref"].append(mq); baseqs["ref"].append(bq)
            elif b == alt:
                strand["alt_rev" if rev else "alt_fwd"] += 1
                mapqs["alt"].append(mq); baseqs["alt"].append(bq)
    tot = sum(v for k, v in counts.items() if k in "ACGT")
    nref = counts.get(ref, 0); nalt = counts.get(alt, 0)
    print(f"    profundidad (ACGT): {tot}   |   conteo: " +
          ", ".join(f"{k}={counts[k]}" for k in "ACGT" if counts[k]))
    if tot:
        print(f"    REF {ref}: {nref} ({nref/tot*100:.0f}%)  [fwd {strand['ref_fwd']} / rev {strand['ref_rev']}]  "
              f"MAPQ~{statistics.median(mapqs['ref']) if mapqs['ref'] else '-'}  BASEQ~{statistics.median(baseqs['ref']) if baseqs['ref'] else '-'}")
        print(f"    ALT {alt}: {nalt} ({nalt/tot*100:.0f}%)  [fwd {strand['alt_fwd']} / rev {strand['alt_rev']}]  "
              f"MAPQ~{statistics.median(mapqs['alt']) if mapqs['alt'] else '-'}  BASEQ~{statistics.median(baseqs['alt']) if baseqs['alt'] else '-'}")
        vaf = nalt / tot
        verdict = "HETEROCIGOTA confirmada" if 0.30 <= vaf <= 0.70 else (
                  "homocigota alt" if vaf > 0.85 else (
                  "posible mosaico / artefacto" if vaf < 0.30 else "revisar"))
        print(f"    VAF = {vaf:.2f}  ->  {verdict}")
    if counts["indel/skip"]:
        print(f"    (+{counts['indel/skip']} lecturas con del/skip en el sitio)")

# ---------- 3. soft-clips y discordantes ----------
print("\n" + "=" * 70)
print("3. SEÑAL DE SV LOCAL  (soft-clips grandes, pares discordantes)")
print("=" * 70)
clip_pos = collections.Counter()
disc = 0
big_clips = 0
for r in bam.fetch(CHROM, EX["exons"][0]["start"] - 2000, EX["exons"][-1]["end"] + 2000):
    if r.is_unmapped or r.is_secondary or r.is_supplementary:
        continue
    if r.cigartuples:
        for op, ln in r.cigartuples:
            if op == 4 and ln >= 20:  # soft-clip >=20bp
                big_clips += 1
                clip_pos[r.reference_start // 100 * 100] += 1
    if r.is_paired and not r.mate_is_unmapped:
        if r.reference_id != r.next_reference_id:
            disc += 1
        elif abs(r.template_length) > 1000:
            disc += 1
        elif r.is_reverse == r.mate_is_reverse:  # misma orientacion
            disc += 1
print(f"\nlecturas con soft-clip >=20bp: {big_clips}")
if clip_pos:
    print("posiciones con clips agrupados (bin 100bp, top 8):")
    for p, c in clip_pos.most_common(8):
        if c >= 3:
            print(f"  ~15:{p}  {c} clips")
print(f"pares discordantes (trans / >1kb / mala orientacion): {disc}")
print("\n(clips agrupados en 1-2 posiciones + discordantes -> mirar con IGV / re-alinear esa zona)")
