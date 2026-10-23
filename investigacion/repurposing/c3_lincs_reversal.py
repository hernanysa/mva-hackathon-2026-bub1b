#!/usr/bin/env python3
"""C3 — Reversión de firma transcripcional (estilo Connectivity Map, vía L1000CDS2).

Tercer método independiente. Pregunta: ¿qué perturbágenos (fármacos/compuestos) del catálogo
LINCS L1000 producen el perfil transcripcional OPUESTO a los estados patológicos relevantes para
MVA1 — senescencia, respuesta a aneuploidía, inestabilidad cromosómica?

API: https://maayanlab.cloud/L1000CDS2/query  (aggravate=false -> busca reversores).
Cruza los hits con la lista de aprobados (Broad hub / DGIdb).
"""
import os, json, time, urllib.request, csv
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_MD = os.path.join(HERE, "c3_RESULTADO.md")
OUT_JSON = os.path.join(HERE, "c3_hits.json")
URL = "https://maayanlab.cloud/L1000CDS2/query"

# ---------- firmas ----------
SIGS = {
 "senescencia": {
  "up": """CDKN1A CDKN2A CDKN2B SERPINE1 GLB1 IGFBP3 IGFBP7 IGFBP5 MDM2 GADD45A GADD45B
           TNFRSF10C CCND1 IL6 IL1A IL1B CXCL8 CXCL1 CXCL2 CCL2 MMP1 MMP3 MMP12 ICAM1
           STAT1 IRF1 B2M IFI16 NFKB1 PLAUR TIMP1 TIMP2 ANGPTL4 TNFRSF1B""".split(),
  "dn": """LMNB1 HMGB1 HMGB2 MKI67 PCNA TOP2A CCNB1 CCNA2 CDK1 CENPA FOXM1 E2F1 MCM2 MCM3
           MCM5 MCM6 RRM2 TYMS EZH2 CHEK1""".split(),
 },
 "resp_aneuploidia": {
  "up": """CDKN1A GDF15 TXNIP SESN1 SESN2 DDIT3 DDIT4 ATF3 TRIB3 PCK2 ASNS PSAT1 PHGDH SHMT2
           MTHFD2 SLC7A11 SLC7A5 SLC3A2 HERPUD1 HSPA5 DNAJB9 XBP1 ATF4 VEGFA BNIP3 NDRG1
           CTSL CTSD LAMP2 SQSTM1 GABARAPL1 MAP1LC3B HMOX1 NQO1 GCLM TXNRD1 SRXN1""".split(),
  "dn": """MKI67 CCNB1 CCNB2 CDK1 PLK1 AURKA AURKB BUB1 BUB1B CENPE CENPF TOP2A RRM2 TYMS
           MCM2 MCM4 MCM6 E2F1 FOXM1 PCNA""".split(),
 },
 "CIN": {   # firma CIN70 (Carter 2006) - inestabilidad cromosómica
  "up": """TPX2 PRC1 FOXM1 CDK1 TGIF2 MCM2 H2AFZ TOP2A CCNB1 UBE2C MELK TRIP13 NCAPD2 MCM7
           RAD51AP1 KIF20A CDC45 MAD2L1 ESPL1 CCNB2 FEN1 TTK CCT5 RFC4 ATAD2 CKAP5 NUP205
           CDC20 CKS2 RRM2 CCNE2 KIF11 KIF23 MCM10 AURKB CENPA CENPF PLK1 NDC80 KIF2C""".split(),
  "dn": [],
 },
}

def query(up, dn, tries=4):
    body = json.dumps({"data": {"upGenes": up, "dnGenes": dn},
                       "config": {"aggravate": False, "searchMethod": "geneSet",
                                  "share": False, "combination": False, "db-version": "latest"},
                       "metadata": []}).encode()
    for i in range(tries):
        try:
            req = urllib.request.Request(URL, data=body,
                headers={"Content-Type": "application/json", "User-Agent": "mva-hackathon-c3/1.0"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except Exception as e:
            print(f"   retry {i}: {e}", flush=True); time.sleep(5 + 5*i)
    return None

# ---------- lista de aprobados (Broad hub + DGIdb) ----------
approved = {}
hub = os.path.join(HERE, "data", "repurposing_drugs_20200324.txt")
with open(hub, encoding="latin-1") as f:
    for line in f:
        if line.startswith(("!", "pert_iname")):
            continue
        p = line.rstrip("\n").split("\t")
        if len(p) >= 3:
            approved[p[0].lower()] = (p[1], p[2])   # phase, moa
try:
    with open(os.path.join(HERE, "data", "dgidb_interactions.tsv")) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if (row.get("approved") or "").upper() == "TRUE":
                approved.setdefault((row.get("drug_name") or "").lower(), ("Launched", ""))
except FileNotFoundError:
    pass

# ---------- correr ----------
agg = defaultdict(lambda: {"n": 0, "best": 0.0, "sigs": set(), "cells": set(), "doses": set()})
raw = {}
for name, s in SIGS.items():
    print(f"== firma {name}  (up {len(s['up'])}, dn {len(s['dn'])})", flush=True)
    d = query(s["up"], s["dn"])
    raw[name] = d
    if not d:
        print("   sin respuesta"); continue
    tm = d.get("topMeta", [])
    print(f"   {len(tm)} perturbágenos reversores", flush=True)
    for m in tm:
        pert = (m.get("pert_desc") or m.get("pert_id") or "").strip()
        if not pert or pert in ("-666", "unannotated"):
            continue
        sc = float(m.get("score", 0))          # 0..2, mayor = mejor reversión en L1000CDS2
        a = agg[pert]
        a["n"] += 1
        a["best"] = max(a["best"], sc)
        a["sigs"].add(name)
        a["cells"].add(m.get("cell_id", ""))
        a["doses"].add(f"{m.get('pert_dose','?')}{m.get('pert_dose_unit','')}")
    time.sleep(1)

rows = []
for pert, a in agg.items():
    ap = approved.get(pert.lower())
    rows.append({"pert": pert, "n_sigs": len(a["sigs"]), "n_hits": a["n"],
                 "best_score": round(a["best"], 3), "sigs": ",".join(sorted(a["sigs"])),
                 "approved": "sí" if ap else "", "phase": ap[0] if ap else "",
                 "moa": ap[1] if ap else "", "cells": ";".join(sorted(c for c in a["cells"] if c))})
rows.sort(key=lambda x: (-x["n_sigs"], -x["best_score"], -x["n_hits"]))

with open(OUT_JSON, "w") as f:
    json.dump({"rows": rows, "raw": raw}, f, indent=1)

md = ["# C3 — Reversión de firma transcripcional (L1000CDS2 / Connectivity Map)\n",
      "Tercer método independiente (ni literatura ni topología de red: **datos de expresión**).",
      f"3 firmas: senescencia, respuesta a aneuploidía (Dürrbaum/Sheltzer), CIN70 (Carter 2006). "
      f"Se pide a L1000CDS2 los perturbágenos que producen el perfil **opuesto**.\n",
      "## Perturbágenos que revierten ≥2 de las 3 firmas\n",
      "| perturbágeno | # firmas | firmas | score | aprobado | fase | MOA |",
      "|--|--|--|--|--|--|--|"]
for r in rows:
    if r["n_sigs"] >= 2:
        md.append(f"| **{r['pert']}** | {r['n_sigs']} | {r['sigs']} | {r['best_score']} | "
                  f"{r['approved']} | {r['phase']} | {r['moa'][:45]} |")
md.append("\n## Top 25 (todos)\n")
md.append("| perturbágeno | #f | score | aprobado | MOA |")
md.append("|--|--|--|--|--|")
for r in rows[:25]:
    md.append(f"| {r['pert']} | {r['n_sigs']} | {r['best_score']} | {r['approved']} | {r['moa'][:50]} |")
md.append("\n_score L1000CDS2: 0–2, mayor = mejor reversión de la firma._\n")
open(OUT_MD, "w").write("\n".join(md))
print(f"\n-> {OUT_MD}")
print("\nreversores multi-firma:")
for r in rows:
    if r["n_sigs"] >= 2:
        print(f"  {r['pert']:26} firmas={r['sigs']:30} score={r['best_score']} aprob={r['approved']} {r['moa'][:40]}")
