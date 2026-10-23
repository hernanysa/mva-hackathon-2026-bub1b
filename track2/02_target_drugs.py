#!/usr/bin/env python3
"""Etapa 2 - fármacos (con foco en APROBADOS) que apuntan a genes del spindle
assembly checkpoint / kinetocoro / APC-C y dianas de la respuesta a la aneuploidía.
Fuentes: DGIdb GraphQL + ChEMBL (target -> mechanism -> molecule)."""
import os, sys, csv
sys.path.insert(0, os.path.dirname(__file__))
from lib import get, post_json, save, eprint

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)
if os.path.exists(f"{OUT}/02_target_drugs.tsv"):
    eprint("02 ya hecho, skip"); sys.exit(0)

PANEL = ["BUB1B","BUB1","BUB3","MAD1L1","MAD2L1","MAD2L1BP","CDC20","TTK","AURKB","AURKA",
         "PLK1","CENPE","KNL1","NDC80","ZW10","CDK1","CCNB1","ESPL1","PTTG1","FZR1",
         "CEP57","TRIP13","CENATAC","KIF11","KIF2C","BIRC5","UBE2C","TOP2A",
         # dianas de vulnerabilidad de células aneuploides / senescencia
         "HSP90AA1","PRKAA1","PRKAA2","MTOR","HDAC1","HDAC6","BCL2L1","BCL2","TP53","MDM2",
         "SQSTM1","ATG7","NAMPT","SIRT1","CDKN2A"]

rows = []

# --- DGIdb ---
eprint("DGIdb (batch)...")
Q = """query($n:[String!]){ genes(names:$n){ nodes{ name interactions{
  interactionScore drug{ name approved conceptId }
  interactionTypes{ type } sources{ sourceDbName } } } } }"""
for i in range(0, len(PANEL), 12):
    chunk = PANEL[i:i+12]
    d = post_json("https://dgidb.org/api/graphql", {"query": Q, "variables": {"n": chunk}})
    for g in ((d or {}).get("data", {}).get("genes", {}) or {}).get("nodes", []):
        for it in g.get("interactions", []):
            dr = it["drug"]
            rows.append({"target_gene": g["name"], "drug": dr["name"], "chembl_id": dr.get("conceptId", ""),
                         "approved": bool(dr.get("approved")), "max_phase": "" ,
                         "drug_type": "", "moa": "|".join(t["type"] for t in it.get("interactionTypes", [])),
                         "score": round(it.get("interactionScore") or 0, 2),
                         "sources": "|".join(s["sourceDbName"] for s in it.get("sources", [])),
                         "source": "dgidb"})

# --- ChEMBL (target -> mechanism -> molecule) para los targets druggables clave ---
CHEMBL_TARGETS = ["TTK","AURKB","AURKA","PLK1","CENPE","KIF11","CDK1","BUB1","HSP90AA1",
                  "HDAC1","HDAC6","MTOR","BCL2L1","NAMPT","TOP2A","KIF2C","BIRC5"]
for sym in CHEMBL_TARGETS:
    eprint(f"ChEMBL {sym} ...")
    ts = get(f"https://www.ebi.ac.uk/chembl/api/data/target/search?q={sym}&format=json&limit=8")
    tid = None
    for t in (ts or {}).get("targets", []):
        if t.get("organism") == "Homo sapiens" and t.get("target_type") == "SINGLE PROTEIN":
            tid = t["target_chembl_id"]; break
    if not tid:
        continue
    mech = get(f"https://www.ebi.ac.uk/chembl/api/data/mechanism?target_chembl_id={tid}&format=json&limit=60")
    for m in (mech or {}).get("mechanisms", []):
        mol = get(f"https://www.ebi.ac.uk/chembl/api/data/molecule/{m['molecule_chembl_id']}?format=json")
        if not mol:
            continue
        mp = mol.get("max_phase")
        try: mpv = float(mp)
        except (TypeError, ValueError): mpv = 0
        rows.append({"target_gene": sym, "drug": (mol.get("pref_name") or m["molecule_chembl_id"]),
                     "chembl_id": m["molecule_chembl_id"],
                     "approved": mpv >= 4, "max_phase": mp,
                     "drug_type": mol.get("molecule_type"), "moa": m.get("mechanism_of_action"),
                     "score": "", "sources": "chembl_mechanism",
                     "source": "chembl"})

# dedup por (drug, target_gene, source)
seen, uniq = set(), []
for r in rows:
    k = (str(r["drug"]).lower(), r["target_gene"], r["source"])
    if k in seen: continue
    seen.add(k); uniq.append(r)

fn = ["target_gene","drug","chembl_id","approved","max_phase","drug_type","moa","score","sources","source"]
with open(f"{OUT}/02_target_drugs.tsv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fn, delimiter="\t"); w.writeheader()
    for r in uniq: w.writerow({k: r.get(k, "") for k in fn})
napp = sum(1 for r in uniq if r["approved"])
eprint(f"02 OK — {len(uniq)} filas, {napp} aprobados. NOTA: BUB1B/SAC core no tienen fármacos aprobados directos.")
