#!/usr/bin/env python3
"""Etapa 4 - (a) fármacos aprobados a 1 salto de BUB1B (vecinos STRING no cubiertos
en la etapa 2) vía DGIdb; (b) ensayos clínicos relevantes (ClinicalTrials.gov v2)."""
import os, sys, json, csv, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
from lib import get, post_json, save, eprint

OUT = os.path.join(os.path.dirname(__file__), "out")
if os.path.exists(f"{OUT}/04_neighborhood_drugs.tsv") and os.path.exists(f"{OUT}/04_trials.json"):
    eprint("04 ya hecho, skip"); sys.exit(0)

mech = json.load(open(f"{OUT}/01_mechanism.json")) if os.path.exists(f"{OUT}/01_mechanism.json") else {}
neigh = mech.get("string_partner_genes", [])[:45]
covered = {"BUB1B","BUB1","BUB3","MAD1L1","MAD2L1","MAD2L1BP","CDC20","TTK","AURKB","AURKA",
           "PLK1","CENPE","KNL1","NDC80","ZW10","CDK1","CCNB1","ESPL1","PTTG1","FZR1","CEP57",
           "TRIP13","CENATAC","KIF11","KIF2C","BIRC5","UBE2C","TOP2A"}
todo = [g for g in neigh if g not in covered]
eprint(f"vecinos STRING nuevos: {todo}")

rows = []
Q = """query($n:[String!]){ genes(names:$n){ nodes{ name interactions{
  interactionScore drug{ name approved conceptId } interactionTypes{ type }
  sources{ sourceDbName } } } } }"""
for i in range(0, len(todo), 12):
    d = post_json("https://dgidb.org/api/graphql", {"query": Q, "variables": {"n": todo[i:i+12]}})
    for g in ((d or {}).get("data", {}).get("genes", {}) or {}).get("nodes", []):
        for it in g.get("interactions", []):
            dr = it["drug"]
            if not dr.get("approved"):
                continue          # solo aprobados para el vecindario
            rows.append({"neighbor_gene": g["name"], "drug": dr["name"],
                         "concept_id": dr.get("conceptId", ""), "approved": True,
                         "itype": "|".join(t["type"] for t in it.get("interactionTypes", [])),
                         "sources": "|".join(s["sourceDbName"] for s in it.get("sources", [])),
                         "score": round(it.get("interactionScore") or 0, 2)})

seen, uniq = set(), []
for r in rows:
    k = (r["drug"].lower(), r["neighbor_gene"])
    if k in seen: continue
    seen.add(k); uniq.append(r)
fn = ["neighbor_gene","drug","concept_id","approved","itype","sources","score"]
with open(f"{OUT}/04_neighborhood_drugs.tsv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fn, delimiter="\t"); w.writeheader(); w.writerows(uniq)
eprint(f"04a OK — {len(uniq)} drogas aprobadas en el vecindario STRING")

# --- (b) ClinicalTrials.gov v2 ---
terms = ['"mosaic variegated aneuploidy"', '"aneuploidy" AND "cancer predisposition"', 'BUB1B',
         '"chromosomal instability" AND treatment', '"premature chromatid separation"',
         '(dasatinib AND quercetin) AND senescent', 'fisetin AND senescence',
         'metformin AND "cancer prevention" AND (Li-Fraumeni OR "cancer predisposition")',
         '"spindle assembly checkpoint" AND inhibitor',
         'rhabdomyosarcoma AND surveillance']
trials = {}
for t in terms:
    eprint(f"CT.gov: {t}")
    d = get("https://clinicaltrials.gov/api/v2/studies?query.term=" + urllib.parse.quote(t) +
            "&pageSize=25", min_gap=0.6)
    for st in (d or {}).get("studies", []):
        p = st.get("protocolSection", {})
        nct = p.get("identificationModule", {}).get("nctId")
        if not nct or nct in trials:
            continue
        trials[nct] = {
            "nct": nct,
            "title": p.get("identificationModule", {}).get("briefTitle"),
            "status": p.get("statusModule", {}).get("overallStatus"),
            "phase": p.get("designModule", {}).get("phases"),
            "conditions": p.get("conditionsModule", {}).get("conditions"),
            "interventions": [i.get("name") for i in
                              p.get("armsInterventionsModule", {}).get("interventions", [])],
            "matched_term": t}
save(f"{OUT}/04_trials.json", list(trials.values()))
eprint(f"04b OK — {len(trials)} ensayos")
