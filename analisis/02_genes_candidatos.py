#!/usr/bin/env python3
"""
02 - Busqueda dirigida de variante causal en un panel de genes.

Panel: MVA / inestabilidad cromosomica + diferenciales de rabdomiosarcoma+renal.
Para cada gen: coords GRCh38 desde Ensembl REST (cacheadas en out/genes_coords.json),
extrae variantes PASS del VCF (pysam), las anota con Ensembl VEP REST
(consecuencia, gnomAD AF, ClinVar, SIFT/PolyPhen) y arma un shortlist priorizado.

Prioriza:
  - LoF (stop/frameshift/splice) homocigota  -> recesivo, 1 evento
  - 2+ variantes raras dañinas en el mismo gen -> posible het compuesta
  - ClinVar pathogenic / likely_pathogenic
  - missense raro (gnomAD AF < 1e-3) con SIFT del / PolyPhen damaging

Requiere: pysam + red (rest.ensembl.org). Uso:
  venv/bin/python analisis/02_genes_candidatos.py data/WGS_EX2312012_HGWCNDSX7.vcf.gz analisis/out/genes
"""
import sys, os, json, time, urllib.request, urllib.error

VCF = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else "analisis/out/genes"
os.makedirs(OUT, exist_ok=True)

# gen -> por que esta en el panel
PANEL = {
    "BUB1B": "MVA1 (~50%): rabdomiosarcoma + Wilms, la mas probable",
    "CEP57": "MVA2: forma mas leve",
    "TRIP13": "MVA3: tumores renales / Wilms de inicio muy temprano",
    "CENATAC": "MVA por splicing (CCDC84)",
    "TP53": "Li-Fraumeni: rabdomiosarcoma, dominante",
    "DICER1": "sindrome DICER1: RMS embrionario + nefroma quistico / Wilms",
    "SMARCB1": "tumor rabdoide",
    "SMARCA4": "tumor rabdoide",
    "FANCA": "anemia de Fanconi (inestabilidad cromosomica)",
    "FANCC": "anemia de Fanconi",
    "FANCG": "anemia de Fanconi",
    "BRCA2": "FANCD1: Wilms, meduloblastoma, inestabilidad",
    "PALB2": "FANCN",
    "NBN": "sindrome de rotura de Nijmegen: microcefalia, cancer, inestabilidad",
    "MRE11": "trastorno tipo ataxia-telangiectasia",
    "RAD50": "sindrome tipo NBS",
    "BLM": "sindrome de Bloom: talla baja, cancer, SCE elevado",
    "RECQL4": "sindrome de Rothmund-Thomson: talla baja, osteosarcoma",
    "PCNT": "MOPD II: enanismo microcefalico primordial (RCIU severo)",
    "ATR": "sindrome de Seckel: enanismo microcefalico primordial",
}

EP = "https://rest.ensembl.org"
HDR = {"Content-Type": "application/json", "Accept": "application/json"}

def get(url):
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=HDR), timeout=30))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2 + 2 * i); continue
            raise
        except Exception:
            time.sleep(2); continue
    raise RuntimeError(f"fallo GET {url}")

def post(path, payload):
    for i in range(5):
        try:
            req = urllib.request.Request(EP + path, data=json.dumps(payload).encode(), headers=HDR, method="POST")
            return json.load(urllib.request.urlopen(req, timeout=60))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(3 + 3 * i); continue
            print(f"  HTTP {e.code}: {e.read()[:200]}", file=sys.stderr); raise
        except Exception as ex:
            print(f"  retry POST ({ex})", file=sys.stderr); time.sleep(3)
    raise RuntimeError("fallo POST")

# --- 1. coords (cache) ---
cf = f"{OUT}/genes_coords.json"
coords = json.load(open(cf)) if os.path.exists(cf) else {}
for g in PANEL:
    if g in coords:
        continue
    try:
        d = get(f"{EP}/lookup/symbol/homo_sapiens/{g}?content-type=application/json")
        coords[g] = {"chr": d["seq_region_name"], "start": d["start"], "end": d["end"],
                     "canonical": d.get("canonical_transcript")}
        print(f"  {g}: {d['seq_region_name']}:{d['start']}-{d['end']}", file=sys.stderr)
        time.sleep(0.15)
    except Exception as e:
        print(f"  !! {g}: {e}", file=sys.stderr)
json.dump(coords, open(cf, "w"), indent=1)

# --- 2. extraer variantes PASS del VCF ---
import pysam
vf = pysam.VariantFile(VCF)
samp = list(vf.header.samples)[0]
PAD = 200
variants = []   # (gene, "chr pos . ref alt . . .", rec_info)
for g, c in coords.items():
    ch = c["chr"]
    try:
        it = vf.fetch(ch, max(0, c["start"] - PAD), c["end"] + PAD)
    except ValueError:
        print(f"  (sin indice para {ch}?)", file=sys.stderr); continue
    for rec in it:
        if rec.filter.keys() and "PASS" not in rec.filter.keys():
            continue
        gt = rec.samples[samp].get("GT")
        if gt is None or set(gt) == {0}:
            continue
        ad = rec.samples[samp].get("AD")
        dp = rec.samples[samp].get("DP")
        zyg = "hom" if set(gt) == {1} else ("het" if 0 in gt and 1 in gt else str(gt))
        for alt in rec.alts:
            variants.append({
                "gene": g, "chr": ch, "pos": rec.pos, "ref": rec.ref, "alt": alt,
                "zyg": zyg, "AD": list(ad) if ad else None, "DP": dp,
                "vep": f"{ch} {rec.pos} . {rec.ref} {alt} . . .",
            })
print(f"{len(variants)} variantes PASS no-ref en el panel", file=sys.stderr)

# --- 3. VEP REST en lotes ---
def vep_batch(vs):
    r = post("/vep/human/region?content-type=application/json&canonical=1&numbers=1&hgvs=1"
             "&SpliceRegion=1&AlphaMissense=1&mane=1",
             {"variants": [v["vep"] for v in vs]})
    return {x["input"]: x for x in r}

ann = {}
B = 190
for i in range(0, len(variants), B):
    chunk = variants[i:i + B]
    try:
        ann.update(vep_batch(chunk))
    except Exception as e:
        print(f"  lote {i}: {e}", file=sys.stderr)
    time.sleep(1)

CODING = {"stop_gained", "stop_lost", "start_lost", "frameshift_variant",
          "splice_acceptor_variant", "splice_donor_variant", "missense_variant",
          "inframe_deletion", "inframe_insertion", "protein_altering_variant",
          "splice_region_variant", "transcript_ablation", "coding_sequence_variant"}
LOF = {"stop_gained", "frameshift_variant", "splice_acceptor_variant",
       "splice_donor_variant", "start_lost", "transcript_ablation"}

rows = []
for v in variants:
    a = ann.get(v["vep"])
    if not a:
        continue
    cons = a.get("most_severe_consequence", "")
    gnomad = 0.0
    clin = []
    for col in a.get("colocated_variants", []) or []:
        for k, val in (col.get("frequencies", {}) or {}).items():
            for kk, fv in val.items():
                if "gnomad" in kk.lower() or kk in ("af",):
                    try: gnomad = max(gnomad, float(fv))
                    except: pass
        cs = col.get("clin_sig") or []
        clin += cs
    tcons = [t for t in (a.get("transcript_consequences") or []) if t.get("gene_symbol") == v["gene"]]
    tcanon = next((t for t in tcons if t.get("canonical")), tcons[0] if tcons else {})
    hgvsp = tcanon.get("hgvsp", "")
    sift = tcanon.get("sift_prediction", "")
    pp = tcanon.get("polyphen_prediction", "")
    am = tcanon.get("alphamissense", {}).get("am_class", "") if isinstance(tcanon.get("alphamissense"), dict) else ""
    is_lof = cons in LOF
    is_coding = cons in CODING or any(t.get("consequence_terms", [None])[0] in CODING for t in tcons)
    path_clin = any("pathogenic" in c for c in clin)
    rare = gnomad < 1e-3
    keep = (is_coding and rare) or path_clin or is_lof
    if not keep:
        continue
    score = 0
    score += 50 if is_lof else 0
    score += 40 if path_clin else 0
    score += 20 if (cons == "missense_variant" and (sift == "deleterious" or pp.startswith("probably") or am == "likely_pathogenic")) else 0
    score += 15 if v["zyg"] == "hom" else 0
    score += 10 if gnomad == 0 else (5 if rare else 0)
    rows.append({**v, "cons": cons, "hgvsp": hgvsp, "gnomad": gnomad,
                 "clin": ";".join(sorted(set(clin))) or "-", "sift": sift, "pp": pp,
                 "alphamissense": am, "score": score})

# het compuesta: +25 a genes con >=2 hits raros
from collections import Counter
gc = Counter(r["gene"] for r in rows)
for r in rows:
    if gc[r["gene"]] >= 2:
        r["score"] += 25

rows.sort(key=lambda r: -r["score"])
with open(f"{OUT}/shortlist.tsv", "w") as fh:
    fh.write("score\tgene\tchr\tpos\tref\talt\tzyg\tconsecuencia\tHGVSp\tgnomAD_AF\tClinVar\tSIFT\tPolyPhen\tAlphaMissense\tAD\tDP\tmotivo_panel\n")
    for r in rows:
        fh.write(f"{r['score']}\t{r['gene']}\t{r['chr']}\t{r['pos']}\t{r['ref']}\t{r['alt']}\t{r['zyg']}\t"
                 f"{r['cons']}\t{r['hgvsp']}\t{r['gnomad']:.2e}\t{r['clin']}\t{r['sift']}\t{r['pp']}\t"
                 f"{r['alphamissense']}\t{r['AD']}\t{r['DP']}\t{PANEL[r['gene']]}\n")

print(f"\n=== TOP 15 ===", file=sys.stderr)
for r in rows[:15]:
    print(f"  [{r['score']:3d}] {r['gene']:8} {r['chr']}:{r['pos']} {r['ref']}>{r['alt']} {r['zyg']:3} "
          f"{r['cons']:24} {r['hgvsp']:22} gnomAD={r['gnomad']:.1e} clin={r['clin']}", file=sys.stderr)
print(f"\n-> {OUT}/shortlist.tsv", file=sys.stderr)
