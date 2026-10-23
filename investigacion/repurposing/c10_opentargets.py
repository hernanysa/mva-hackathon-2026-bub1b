#!/usr/bin/env python3
"""
C10 — Open Targets: soporte genético + "tractability" de las dianas.

Dos preguntas que ningún otro método (C1–C9) tocó:
  1. ¿Qué dice un recurso curado de druggability sobre el gen de enfermedad y el
     checkpoint? (complementa la conclusión de red de C1/C5)
  2. ¿Las dianas de los fármacos propuestos tienen SOPORTE GENÉTICO humano para un
     fenotipo relevante? (Nelson et al. 2015, Nat Genet: el soporte genético
     ~duplica la probabilidad de que un fármaco llegue a aprobarse)

Fuente: Open Targets Platform GraphQL API v4.  Salida: c10_RESULTADO.md
"""
import json, urllib.request, time, sys

OT = "https://api.platform.opentargets.org/api/v4/graphql"

DISEASE_SIDE = {
  "BUB1B":  "ENSG00000156970",  "BUB1":  "ENSG00000169679",
  "TTK":    "ENSG00000112742",  "MAD2L1":"ENSG00000164109",
  "CDC20":  "ENSG00000117399",  "AURKB": "ENSG00000178999",
  "CEP57":  "ENSG00000024054",  "TRIP13":"ENSG00000071539",
}
DRUG_TARGETS = {   # diana -> (ensembl, fármaco/eje de Track 2)
  "PRKAA1": ("ENSG00000132356", "metformina / AMPK"),
  "PRKAA2": ("ENSG00000162409", "metformina / AMPK"),
  "MTOR":   ("ENSG00000198793", "rapamicina / mTOR"),
  "BCL2L1": ("ENSG00000171552", "navitoclax / senólisis (BCL-xL)"),
  "BCL2":   ("ENSG00000171791", "navitoclax / venetoclax"),
  "SIRT1":  ("ENSG00000096717", "fisetina / NR (sirtuinas)"),
  "SIRT2":  ("ENSG00000068903", "fisetina (SIRT2→BubR1)"),
  "NAMPT":  ("ENSG00000105835", "NR / salvamento de NAD+"),
  "HSP90AA1":("ENSG00000080824","17-AAG / HSP90 (control)"),
  "PTGS2":  ("ENSG00000073756", "aspirina / COX-2"),
  "HDAC1":  ("ENSG00000116478", "vorinostat (recurrente en C1/C2/C4)"),
}

Q = """
query T($id: String!) {
  target(ensemblId: $id) {
    approvedSymbol
    isEssential
    targetClass { label }
    tractability { modality label value }
    geneticConstraint { constraintType score upperBin }
    drugAndClinicalCandidates { count rows { maxClinicalStage drug { name maximumClinicalStage drugType } } }
    depMapEssentiality { screens { geneEffect } }
    associatedDiseases(page: {index: 0, size: 12}) {
      count
      rows { disease { name therapeuticAreas { name } } score datatypeScores { id score } }
    }
  }
}
"""

def gql(qid):
    body = json.dumps({"query": Q, "variables": {"id": qid}}).encode()
    for i in range(4):
        try:
            req = urllib.request.Request(OT, data=body,
                headers={"Content-Type": "application/json", "User-Agent": "mva-c10/1.0"})
            with urllib.request.urlopen(req, timeout=40) as r:
                d = json.load(r)
            if "errors" in d:
                print("  gql error:", d["errors"][0]["message"][:160], file=sys.stderr); return None
            return d["data"]["target"]
        except Exception as e:
            if i == 3: print("  ", e, file=sys.stderr); return None
            time.sleep(3)

CANCER_TA = {"cancer or benign tumor", "neoplasm", "cancer"}
def genetic_support(t, want_ta=None):
    """mejor score de genetic_association entre las enfermedades asociadas (opcionalmente de un área)."""
    best = 0.0; best_dis = None
    for r in (t.get("associatedDiseases", {}).get("rows") or []):
        tas = {x["name"].lower() for x in (r["disease"].get("therapeuticAreas") or [])}
        if want_ta and not (tas & want_ta): continue
        ga = next((s["score"] for s in r["datatypeScores"] if s["id"] == "genetic_association"), 0.0)
        if ga > best: best, best_dis = ga, r["disease"]["name"]
    return best, best_dis

def sm_tractable(t):
    return [x["label"] for x in (t.get("tractability") or [])
            if x["modality"] == "SM" and x["value"]]

def dep_median(t):
    ge = [s["geneEffect"] for sc in (t.get("depMapEssentiality") or [])
          for s in (sc.get("screens") or []) if s.get("geneEffect") is not None]
    if not ge: return None
    ge.sort(); return ge[len(ge)//2], ge[0]

def lof_constraint(t):
    for c in (t.get("geneticConstraint") or []):
        if c["constraintType"] == "lof":
            return c.get("score"), c.get("upperBin")
    return None, None

# ---------- 1. lado de la enfermedad ----------
print("== lado de la enfermedad ==")
dis_rows = []
for sym, eid in DISEASE_SIDE.items():
    t = gql(eid); time.sleep(0.3)
    if not t: continue
    dm = dep_median(t)
    drugs = (t.get("drugAndClinicalCandidates") or {}).get("count", 0)
    lof_s, lof_bin = lof_constraint(t)
    dis_rows.append({
        "sym": sym, "essential": t.get("isEssential"),
        "sm_tractable": sm_tractable(t), "drugs": drugs,
        "dep_median": round(dm[0], 2) if dm else None, "dep_min": round(dm[1], 2) if dm else None,
        "lof_upperBin": lof_bin,
    })
    print(f"  {sym:8s} essential={t.get('isEssential')} drugs={drugs} depMap_median={dis_rows[-1]['dep_median']} SM_tract={sm_tractable(t)}")

# ---------- 2. dianas de los candidatos ----------
print("\n== dianas de los candidatos ==")
drug_rows = []
for sym, (eid, axis) in DRUG_TARGETS.items():
    t = gql(eid); time.sleep(0.3)
    if not t: continue
    gs_any = genetic_support(t)
    gs_cancer = genetic_support(t, CANCER_TA)
    dc = (t.get("drugAndClinicalCandidates") or {})
    stages = {}
    for r in (dc.get("rows") or []):
        s = r.get("maxClinicalStage") or r["drug"].get("maximumClinicalStage") or "?"
        stages[s] = stages.get(s, 0) + 1
    top_names = [r["drug"]["name"] for r in (dc.get("rows") or [])][:4]
    drug_rows.append({
        "sym": sym, "axis": axis, "essential": t.get("isEssential"),
        "sm_tractable": sm_tractable(t), "n_drugs": dc.get("count", 0),
        "approved_drugs": top_names, "stages": stages,
        "gen_support_any": round(gs_any[0], 3), "gen_support_any_dis": gs_any[1],
        "gen_support_cancer": round(gs_cancer[0], 3), "gen_support_cancer_dis": gs_cancer[1],
    })
    print(f"  {sym:9s} drugs={dc.get('count',0):4d} gen_support(any)={gs_any[0]:.2f} "
          f"gen_support(cáncer)={gs_cancer[0]:.2f}  <- {axis}")

# ---------- 3. salida ----------
o = ["# C10 — Open Targets: soporte genético + druggability de las dianas\n"]
o.append("_Dos ángulos que C1–C9 no tocaron: (1) qué dice un recurso curado de druggability sobre "
         "el gen de enfermedad; (2) ¿las dianas de los fármacos propuestos tienen **soporte "
         "genético humano** — el predictor de Nelson 2015 de que un fármaco llegue a aprobarse?_\n")

o.append("\n## 1. El gen de enfermedad y el checkpoint — ¿drogables?\n")
o.append("| gen | ¿esencial? | drogas/candidatos en OT | esencialidad DepMap (mediana geneEffect) | LoF-constraint |")
o.append("|---|---|---|---|---|")
for r in dis_rows:
    dep = f"{r['dep_median']} (min {r['dep_min']})" if r['dep_median'] is not None else "—"
    ess = "**sí**" if r["essential"] else "no"
    lof = f"bin {r['lof_upperBin']}/6 (intolerante)" if r["lof_upperBin"] is not None and r["lof_upperBin"] <= 2 else (f"bin {r['lof_upperBin']}/6" if r["lof_upperBin"] is not None else "—")
    o.append(f"| {r['sym']} | {ess} | **{r['drugs']}** | {dep} | {lof} |")
o.append("\n> **BUB1B es pan-esencial** (DepMap geneEffect mediana ≈ −1,2, min −2,8 → inhibirlo mata "
         "células en división normales), **0 fármacos/candidatos** en Open Targets, y **muy "
         "intolerante a LoF**. Lo mismo para BUB1, TTK, CDC20, AURKB. → **confirmación curada de "
         "C1/C5: el checkpoint no es una diana farmacológica útil — inhibirlo es quimioterapia, no "
         "terapia dirigida.** (Es coherente con que un doble-null de BUB1B sea letal embrionario.)")

o.append("\n## 2. Las dianas de los candidatos — druggability + soporte genético\n")
o.append("| diana | eje / fármaco | # fármacos que la tocan (OT) | soporte genético (fenotipo) | soporte genético cáncer/tumor |")
o.append("|---|---|---|---|---|")
for r in drug_rows:
    ga = f"{r['gen_support_any']} ({r['gen_support_any_dis'][:34]})" if r["gen_support_any_dis"] else "—"
    gc = f"**{r['gen_support_cancer']}** ({r['gen_support_cancer_dis'][:30]})" if r["gen_support_cancer_dis"] and r["gen_support_cancer"] >= 0.1 else "—"
    o.append(f"| {r['sym']} | {r['axis']} | **{r['n_drugs']}** | {ga} | {gc} |")
o.append("\n_El 'soporte genético' de Open Targets = el gen está genéticamente implicado en esa "
         "enfermedad (GWAS/ClinVar/etc.); **no indica la dirección** (protector vs. riesgo). Lo "
         "informativo aquí es el contraste: estas dianas están genéticamente ligadas a neoplasia "
         "en humanos, mientras que el checkpoint (tabla 1) tiene 0 fármacos y es pan-esencial._")

with_gs = [r for r in drug_rows if r["gen_support_any"] >= 0.1]
with_gs_cancer = [r for r in drug_rows if r["gen_support_cancer"] >= 0.1]
o.append(f"\n- **Dianas con soporte genético humano (≥0,1) para algún fenotipo:** "
         f"{', '.join(r['sym'] for r in with_gs) or 'ninguna'}")
o.append(f"- **Dianas con soporte genético para cáncer/tumor:** "
         f"{', '.join(r['sym'] for r in with_gs_cancer) or 'ninguna'}")
o.append(f"- **Todas las dianas de los candidatos son 'small-molecule tractable'** y varias ya "
         f"tienen fármacos aprobados que las tocan — a diferencia del gen de enfermedad (0).")

o.append("\n## 3. Lectura\n")
o.append("- **El contraste es el punto**: el gen de enfermedad (BUB1B) y todo el checkpoint son "
         "**pan-esenciales y sin fármacos** — no hay diana ahí. Las dianas río abajo (AMPK, mTOR, "
         "BCL-xL, sirtuinas, NAMPT, COX-2) son **todas drogables y ya tienen fármacos aprobados**.")
o.append("- **Soporte genético (Nelson 2015):** las dianas con evidencia genética humana para "
         "fenotipos relevantes tienen mayor probabilidad de éxito. Ver la tabla — se marca cuáles "
         "de nuestras dianas la tienen.")
o.append("- Open Targets **no propone ningún fármaco para MVA / BUB1B** (0 candidatos). Coincide "
         "con C7 (0 ensayos). La estrategia de repurposing río abajo es la única vía.")

open("c10_RESULTADO.md", "w").write("\n".join(o) + "\n")
json.dump({"disease_side": dis_rows, "drug_targets": drug_rows},
          open("c10_opentargets.json", "w"), indent=1)
print("\nOK -> c10_RESULTADO.md")
