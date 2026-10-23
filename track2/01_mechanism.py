#!/usr/bin/env python3
"""Etapa 1 - anclaje del mecanismo de BUB1B / BUBR1 (LoF -> MVA1)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import get, post_json, save, eprint

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)
if os.path.exists(f"{OUT}/01_mechanism.json"):
    eprint("01 ya hecho, skip"); sys.exit(0)

M = {"gene": "BUB1B", "protein": "BUBR1", "uniprot": "O60566",
     "ensembl": "ENSG00000156970", "entrez": "701",
     "disease": "Mosaic Variegated Aneuploidy syndrome 1 (MVA1, MIM 257300)",
     "mechanism": "biallelic loss-of-function -> weakened spindle assembly checkpoint (SAC)"}

# --- UniProt: funcion, dominios, interacciones ---
eprint("UniProt O60566 ...")
u = get("https://rest.uniprot.org/uniprotkb/O60566.json")
if u:
    M["uniprot_function"] = " ".join(
        c["texts"][0]["value"] for c in u.get("comments", [])
        if c["commentType"] == "FUNCTION" and c.get("texts"))
    M["uniprot_domains"] = sorted({f["description"] for f in u.get("features", [])
                                   if f["type"] in ("Domain", "Region") and f.get("description")})
    M["uniprot_pathway_keywords"] = [k["name"] for k in u.get("keywords", [])
                                     if k.get("category") in ("Biological process", "Molecular function")]

# --- KEGG: vias que contienen BUB1B ---
eprint("KEGG hsa:701 ...")
k = get("https://rest.kegg.jp/link/pathway/hsa:701", min_gap=0.4, raw=True)
if k:
    paths = [ln.split("\t")[1] for ln in k.decode().splitlines() if "\t" in ln]
    named = {}
    for p in paths[:25]:
        nm = get(f"https://rest.kegg.jp/list/{p}", min_gap=0.4, raw=True)
        if nm: named[p] = nm.decode().strip().split("\t")[-1]
    M["kegg_pathways"] = named

# --- Reactome: via UniProt ---
eprint("Reactome ...")
r = get("https://reactome.org/ContentService/data/mapping/UniProt/O60566/pathways?species=9606")
if isinstance(r, list):
    M["reactome_pathways"] = sorted({p.get("displayName") for p in r if p.get("displayName")})

# --- STRING: interactores de alta confianza (la red del SAC) ---
eprint("STRING interactors ...")
s = get("https://string-db.org/api/json/interaction_partners?identifiers=BUB1B&species=9606&required_score=700&limit=60")
if isinstance(s, list):
    M["string_partners"] = sorted({p["preferredName_B"]: round(p["score"], 3)
                                   for p in s}.items(), key=lambda x: -x[1])
    M["string_partner_genes"] = [g for g, _ in M["string_partners"]]

# --- OpenTargets: BUB1B -> enfermedades, drogas conocidas, tractability ---
eprint("OpenTargets GraphQL ...")
q = """query($id:String!){ target(ensemblId:$id){
  approvedSymbol biotype
  tractability{ modality label value }
  knownDrugs{ count rows{ drug{ name maximumClinicalTrialPhase isApproved } mechanismOfAction phase status disease{ name } } }
  associatedDiseases(page:{index:0,size:15}){ rows{ disease{ name } score } }
} }"""
ot = post_json("https://api.platform.opentargets.org/api/v4/graphql",
               {"query": q, "variables": {"id": M["ensembl"]}})
if ot and ot.get("data", {}).get("target"):
    t = ot["data"]["target"]
    M["opentargets_tractability"] = [x for x in t.get("tractability", []) if x.get("value")]
    M["opentargets_known_drugs"] = [
        {"drug": row["drug"]["name"], "approved": row["drug"]["isApproved"],
         "max_phase": row["drug"]["maximumClinicalTrialPhase"],
         "moa": row.get("mechanismOfAction"), "status": row.get("status"),
         "disease": (row.get("disease") or {}).get("name")}
        for row in (t.get("knownDrugs") or {}).get("rows", [])]
    M["opentargets_assoc_diseases"] = [
        {"disease": r["disease"]["name"], "score": round(r["score"], 3)}
        for r in (t.get("associatedDiseases") or {}).get("rows", [])]

save(f"{OUT}/01_mechanism.json", M)

# resumen legible
lines = [f"# Etapa 1 — mecanismo de {M['gene']} / {M['protein']}", "",
         f"- Enfermedad: {M['disease']}", f"- Mecanismo: {M['mechanism']}",
         f"- UniProt {M['uniprot']}, Ensembl {M['ensembl']}, Entrez {M['entrez']}", ""]
if M.get("uniprot_function"): lines += ["## Función (UniProt)", M["uniprot_function"], ""]
if M.get("uniprot_domains"): lines += ["## Dominios", ", ".join(M["uniprot_domains"]), ""]
if M.get("reactome_pathways"): lines += ["## Vías (Reactome)", *[f"- {p}" for p in M["reactome_pathways"]], ""]
if M.get("kegg_pathways"): lines += ["## Vías (KEGG)", *[f"- {v}" for v in M["kegg_pathways"].values()], ""]
if M.get("string_partner_genes"): lines += ["## Red del SAC — interactores STRING (score>=0.7)",
                                            ", ".join(M["string_partner_genes"]), ""]
if M.get("opentargets_known_drugs"):
    lines += ["## Drogas conocidas vs BUB1B (OpenTargets)"]
    for d in M["opentargets_known_drugs"][:20]:
        lines.append(f"- {d['drug']} (aprobado={d['approved']}, fase {d['max_phase']}) — {d['moa']} — {d['disease']}")
    lines.append("")
save(f"{OUT}/01_mechanism.md", "\n".join(lines))
eprint("01 OK")
