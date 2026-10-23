#!/usr/bin/env python3
"""Etapa 5 - consolida todo en una tabla de candidatos con evidencia y tier preliminar.
NO decide la respuesta: es material para curar con el usuario."""
import os, sys, json, csv
sys.path.insert(0, os.path.dirname(__file__))

OUT = os.path.join(os.path.dirname(__file__), "out")

def load_tsv(p):
    if not os.path.exists(p): return []
    return list(csv.DictReader(open(p), delimiter="\t"))

def norm(name):
    return (name or "").strip().lower()

cand = {}  # drug -> dossier

def add(drug, **kw):
    d = norm(drug)
    if not d or d in ("nan", "none", ""): return
    c = cand.setdefault(d, {"drug": drug, "targets": set(), "approved": False,
                            "max_phase": 0, "moa": set(), "approved_indications": set(),
                            "lit_pmids": set(), "lit_queries": set(), "lit_relevant": 0,
                            "lit_titles": [], "methods": set(), "trials": set()})
    if kw.get("target"): c["targets"].add(kw["target"])
    if kw.get("approved"): c["approved"] = True
    try:
        c["max_phase"] = max(c["max_phase"], float(kw.get("max_phase") or 0))
    except (ValueError, TypeError): pass
    if kw.get("moa"): c["moa"].add(kw["moa"])
    if kw.get("ind"): c["approved_indications"].add(kw["ind"])
    if kw.get("method"): c["methods"].add(kw["method"])

# etapa 2 + 4a: drogas por target
for p, meth in [("02_target_drugs.tsv", "target(SAC panel)"), ("04_neighborhood_drugs.tsv", "target(STRING neighbor)")]:
    for r in load_tsv(f"{OUT}/{p}"):
        tg = r.get("target_gene") or r.get("neighbor_gene")
        add(r["drug"], target=tg, method=meth,
            approved=(str(r.get("approved")).lower() == "true"),
            max_phase=r.get("max_phase"), moa=r.get("moa"),
            ind=r.get("approved_indications"))

# etapa 3: menciones en literatura
for r in load_tsv(f"{OUT}/03_drug_mentions.tsv"):
    d = norm(r["drug"])
    c = cand.setdefault(d, {"drug": r["drug"], "targets": set(), "approved": False,
                            "max_phase": 0, "moa": set(), "approved_indications": set(),
                            "lit_pmids": set(), "lit_queries": set(), "lit_relevant": 0,
                            "lit_titles": [], "methods": set(), "trials": set()})
    c["lit_pmids"] |= set(filter(None, r["pmids"].split(",")))
    c["lit_queries"] |= set(filter(None, r["queries"].split(";")))
    c["lit_relevant"] = int(r["n_relevant_context"])
    c["lit_titles"] = [t for t in r["example_titles"].split(" || ") if t]
    c["methods"].add("literature")

# etapa 4b: ensayos
for tr in (json.load(open(f"{OUT}/04_trials.json")) if os.path.exists(f"{OUT}/04_trials.json") else []):
    for iv in (tr.get("interventions") or []):
        d = norm(iv)
        if d in cand:
            cand[d]["trials"].add(tr["nct"])
            cand[d]["methods"].add("clinicaltrials")

# --- tier heurístico (preliminar, para curar) ---
def tier(c):
    score = 0
    if c["approved"] or c["max_phase"] >= 4: score += 3
    score += min(c["lit_relevant"], 6)
    score += 2 * len([m for m in c["methods"] if m.startswith("target")])
    score += 2 if c["lit_relevant"] >= 3 and (c["approved"] or c["max_phase"] >= 4) else 0
    score += len(c["trials"])
    if score >= 9: return "A", score
    if score >= 5: return "B", score
    if score >= 2: return "C", score
    return "D", score

rows = []
for c in cand.values():
    t, sc = tier(c)
    rows.append({**c, "tier": t, "score": sc})
rows.sort(key=lambda r: (-r["score"], r["drug"]))

with open(f"{OUT}/candidatos_track2.json", "w") as f:
    json.dump([{k: (sorted(v) if isinstance(v, set) else v) for k, v in r.items()} for r in rows],
              f, indent=1, ensure_ascii=False)

L = ["# Track 2 — candidatos de reposicionamiento (BUB1B LoF / MVA1)",
     "",
     "**Material para curar, NO la respuesta final.** Generado por el pipeline nocturno "
     "(OpenTargets + ChEMBL + STRING + PubMed + ClinicalTrials.gov).",
     f"\nTotal fármacos: {len(rows)}  ·  tier A: {sum(1 for r in rows if r['tier']=='A')}  "
     f"B: {sum(1 for r in rows if r['tier']=='B')}  C: {sum(1 for r in rows if r['tier']=='C')}",
     ""]
for r in rows:
    if r["tier"] == "D" and r["score"] < 2:
        continue
    L.append(f"## [{r['tier']}] {r['drug']}  (score {r['score']})")
    if r["approved"] or r["max_phase"] >= 4:
        L.append(f"- **Aprobado** (fase {r['max_phase']:g})  ·  indicaciones: {', '.join(sorted(r['approved_indications'])) or 'n/d'}")
    else:
        L.append(f"- Máx fase clínica: {r['max_phase']:g}")
    if r["targets"]: L.append(f"- Targets en la red del SAC: {', '.join(sorted(r['targets']))}")
    if r["moa"]: L.append(f"- MoA: {'; '.join(sorted(m for m in r['moa'] if m))[:300]}")
    if r["lit_relevant"]: L.append(f"- Literatura: {r['lit_relevant']} abstracts con contexto relevante, "
                                   f"{len(r['lit_pmids'])} PMIDs, queries: {', '.join(sorted(r['lit_queries']))}")
    for t in r["lit_titles"][:3]:
        L.append(f"    - {t}")
    if r["trials"]: L.append(f"- Ensayos: {', '.join(sorted(r['trials']))}")
    L.append(f"- Métodos que lo marcaron: {', '.join(sorted(r['methods']))}")
    L.append("")
open(f"{OUT}/candidatos_track2.md", "w").write("\n".join(L))
print(f"05 OK -> {OUT}/candidatos_track2.md  ({len(rows)} fármacos)")
for r in rows[:12]:
    print(f"  [{r['tier']}] {r['drug']:22} score {r['score']:2}  aprob={r['approved']}  lit={r['lit_relevant']}  targets={sorted(r['targets'])[:3]}")
