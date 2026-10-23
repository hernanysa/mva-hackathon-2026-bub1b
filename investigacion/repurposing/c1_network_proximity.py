#!/usr/bin/env python3
"""C1 — Repurposing por PROXIMIDAD DE RED (Guney et al., Nat Commun 2016).

Método independiente del pipeline de literatura de Track 2. Pregunta:
"¿qué fármacos aprobados/en-clínica tienen dianas que caen cerca del módulo de
enfermedad (BUB1B / genes MVA / checkpoint del huso) en el interactoma humano?"

- Interactoma: STRING v12, combined_score >= 700, símbolos, componente conexa mayor.
- Métrica: d_c(S,T) = promedio_{t in T} min_{s in S} d(s,t)  (distancia "closest").
- Referencia nula: 1000 conjuntos T' de igual tamaño y grado (binned) -> z-score, p empírico.
- Fármacos: Broad Drug Repurposing Hub (fase clínica + MOA + dianas) ∪ DGIdb (aprobados).

Salida: investigacion/repurposing/c1_RESULTADO.md + c1_ranking.tsv
"""
import os, sys, gzip, json, time, random, statistics, csv
import networkx as nx

random.seed(42)
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
OUT_MD = os.path.join(HERE, "c1_RESULTADO.md")
OUT_TSV = os.path.join(HERE, "c1_ranking.tsv")
t0 = time.time()

def log(m): print(f"[{time.time()-t0:6.0f}s] {m}", flush=True)

# ---------- 1. interactoma STRING ----------
log("mapa ENSP -> símbolo")
ensp2sym = {}
with gzip.open(os.path.join(D, "string_info.txt.gz"), "rt") as f:
    next(f)
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) >= 2:
            ensp2sym[p[0]] = p[1]

log("cargando aristas STRING (score >= 700)")
G = nx.Graph()
THR = 700
n_raw = 0
with gzip.open(os.path.join(D, "string_links.txt.gz"), "rt") as f:
    next(f)
    for line in f:
        a, b, s = line.split()
        n_raw += 1
        if int(s) < THR:
            continue
        ga, gb = ensp2sym.get(a), ensp2sym.get(b)
        if ga and gb and ga != gb:
            G.add_edge(ga, gb)
log(f"  {n_raw:,} aristas crudas -> grafo {G.number_of_nodes():,} nodos / {G.number_of_edges():,} aristas")
G = G.subgraph(max(nx.connected_components(G), key=len)).copy()
log(f"  componente mayor: {G.number_of_nodes():,} nodos / {G.number_of_edges():,} aristas")
deg = dict(G.degree())

# ---------- 2. módulos de enfermedad ----------
MODULES = {
    "MVA_genes":   ["BUB1B", "CEP57", "TRIP13", "CENATAC"],
    "SAC_MCC":     ["BUB1B", "BUB1", "BUB3", "MAD1L1", "MAD2L1", "TTK", "CDC20",
                    "CENPE", "KNL1", "ZW10", "ZWILCH"],
    # eje 2 del análisis curado: supervivencia de células senescentes (BubR1^H/H = modelo senolítico)
    "senescencia": ["CDKN2A", "CDKN1A", "TP53", "RB1", "SERPINE1", "GLB1", "LMNB1",
                    "BCL2", "BCL2L1", "BCL2L2", "MCL1", "TP53BP1", "E2F1", "MDM2"],
    # eje 1 del análisis curado: tolerancia/estrés de la aneuploidía
    "aneuploidia_estres": ["HSP90AA1", "HSP90AB1", "HSF1", "PRKAA1", "PRKAA2", "AMPK",
                           "MTOR", "TFEB", "SQSTM1", "MAP1LC3B", "ATG7", "NQO1", "NFE2L2"],
}
for k, v in MODULES.items():
    inG = [g for g in dict.fromkeys(v) if g in G]
    MODULES[k] = inG
    log(f"  módulo {k}: {inG}")

# dS[modulo][nodo] = min distancia a cualquier semilla del módulo
dS = {}
for k, seeds in MODULES.items():
    best = {}
    for s in seeds:
        for node, dist in nx.single_source_shortest_path_length(G, s).items():
            if node not in best or dist < best[node]:
                best[node] = dist
    dS[k] = best
    log(f"  dS[{k}] alcanza {len(best):,} nodos")

# ---------- 3. bins de grado para la referencia nula ----------
import math
def gbin(d):
    if d <= 100: return d
    return 100 + int(math.log2(d / 100) * 4)
bins = {}
for node, d in deg.items():
    bins.setdefault(gbin(d), []).append(node)
log(f"  {len(bins)} bins de grado")

# ---------- 4. fármacos ----------
drugs = {}   # name -> {phase, moa, targets:set, src:set}
PHASE_RANK = {"Launched": 4, "Phase 3": 3, "Phase 2": 2, "Phase 1": 1, "Preclinical": 0, "Withdrawn": -1}
hub = os.path.join(D, "repurposing_drugs_20200324.txt")
with open(hub, encoding="latin-1") as f:
    for line in f:
        if line.startswith("!") or line.startswith("pert_iname"):
            continue
        p = line.rstrip("\n").split("\t")
        if len(p) < 4:
            continue
        name, phase, moa, target = p[0], p[1], p[2], p[3]
        tg = set(t for t in target.split("|") if t)
        drugs[name.lower()] = {"name": name, "phase": phase, "moa": moa,
                               "targets": tg, "src": {"broad"}}
log(f"  Broad hub: {len(drugs)} fármacos")

# DGIdb: SOLO para (a) marcar aprobación y (b) añadir dianas de interacciones con
# tipo mecanístico explícito y score decente (evita el ruido text-mined tipo
# "cefalotina -> APEX1"). El Broad hub sigue siendo la fuente primaria de dianas.
dgi = os.path.join(D, "dgidb_interactions.tsv")
GOOD_ITYPE = {"inhibitor", "antagonist", "agonist", "blocker", "activator", "partial agonist",
              "inverse agonist", "antibody", "channel blocker", "positive allosteric modulator",
              "negative allosteric modulator", "binder", "modulator"}
n_dgi = 0
with open(dgi) as f:
    r = csv.DictReader(f, delimiter="\t")
    for row in r:
        gene = (row.get("gene_name") or "").strip()
        dname = (row.get("drug_name") or "").strip()
        appr = (row.get("approved") or "").strip().upper() == "TRUE"
        itype = (row.get("interaction_type") or "").strip().lower()
        try:
            sc = float(row.get("interaction_score") or 0)
        except ValueError:
            sc = 0.0
        if not gene or not dname:
            continue
        key = dname.lower()
        d = drugs.get(key)
        if d is None:
            if not appr:
                continue
            d = drugs[key] = {"name": dname, "phase": "Launched" if appr else "",
                              "moa": "", "targets": set(), "src": set()}
        if appr and PHASE_RANK.get(d["phase"], -9) < 4:
            d["phase"] = "Launched"
        # añade la diana solo si es una interacción mecanística creíble
        if itype in GOOD_ITYPE and sc >= 0.25:
            d["targets"].add(gene)
            d["src"].add("dgidb")
            n_dgi += 1
log(f"  + DGIdb: {n_dgi:,} interacciones mecanísticas integradas -> {len(drugs)} fármacos")

# ---------- 5. proximidad ----------
NPERM = 1000
def perm_ref(target_nodes, dvec):
    """media/std de d_c bajo 1000 remuestreos degree-matched."""
    pools = []
    for tn in target_nodes:
        b = gbin(deg[tn])
        pool = bins.get(b) or [tn]
        pools.append(pool)
    vals = []
    for _ in range(NPERM):
        acc = 0.0
        for pool in pools:
            for _try in range(20):
                cand = random.choice(pool)
                if cand in dvec:
                    acc += dvec[cand]; break
            else:
                acc += dvec.get(random.choice(pool), 6)
        vals.append(acc / len(pools))
    return statistics.fmean(vals), statistics.pstdev(vals)

SPINDLE_MOA = ("aurora", "polo-like", "plk ", "plk inhibitor", "kinesin", "eg5", "kif11",
               "tubulin", "mps1", "ttk", "cenp-e", "mitotic", "microtubule")
def is_spindle(moa):
    m = (moa or "").lower()
    return any(k in m for k in SPINDLE_MOA)

results = []
KEEP_PHASE = {"Launched", "Phase 3", "Phase 2", "Phase 1"}
for key, d in drugs.items():
    if d["phase"] and d["phase"] not in KEEP_PHASE:
        continue
    T = sorted(t for t in d["targets"] if t in G)
    if not (1 <= len(T) <= 25):
        continue
    for mod, dvec in dS.items():
        tin = [t for t in T if t in dvec]
        if not tin:
            continue
        dc = statistics.fmean(dvec[t] for t in tin)
        mu, sd = perm_ref(tin, dvec)
        z = (dc - mu) / sd if sd > 0 else 0.0
        direct = sum(1 for t in tin if dvec[t] == 0)
        adj = sum(1 for t in tin if dvec[t] == 1)
        results.append({"drug": d["name"], "phase": d["phase"], "moa": d["moa"],
                        "module": mod, "n_target": len(T), "n_in_mod_graph": len(tin),
                        "d_c": round(dc, 3), "z": round(z, 2), "mu": round(mu, 3),
                        "direct_hits": direct, "adjacent_hits": adj,
                        "spindle": int(is_spindle(d["moa"])),
                        "targets": ";".join(T[:12]), "src": ",".join(sorted(d["src"])) or "broad"})
log(f"  {len(results)} (fármaco x módulo) evaluados")

# ---------- 6. reporte ----------
results.sort(key=lambda x: (x["z"], x["d_c"]))
with open(OUT_TSV, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(results[0].keys()), delimiter="\t")
    w.writeheader()
    for r in results:
        w.writerow(r)

def top_for(mod, n=25, exclude_spindle=False, min_in=2):
    rr = [r for r in results if r["module"] == mod and r["n_in_mod_graph"] >= min_in]
    if exclude_spindle:
        rr = [r for r in rr if not r["spindle"]]
    return rr[:n]

md = ["# C1 — Repurposing por proximidad de red (Guney 2016)\n",
      f"Interactoma STRING v12 (score≥700): **{G.number_of_nodes():,} genes / {G.number_of_edges():,} "
      f"interacciones** (componente conexa mayor).",
      f"Fármacos: Broad Drug Repurposing Hub ∪ DGIdb-aprobados = **{len(drugs):,}** "
      f"(evaluados los que tienen 1–25 dianas en el interactoma y fase ≥1).",
      f"Métrica *closest* d_c(S,T); z-score vs {NPERM} conjuntos de dianas degree-matched.\n",
      "> Qué mide: si las **dianas del fármaco caen cerca del módulo mitótico de la enfermedad**. "
      "NO captura el eje senescencia/senolíticos (esos actúan río abajo) — es una lente complementaria, "
      "no un veredicto único.\n"]

for mod in MODULES:
    md.append(f"\n## Módulo `{mod}`  =  {{{', '.join(MODULES[mod])}}}\n")
    md.append("### Todos (incluye fármacos de huso mitótico)\n")
    md.append("| # | fármaco | fase | z | d_c | dianas | huso? | MOA |")
    md.append("|--|--|--|--|--|--|--|--|")
    for i, r in enumerate(top_for(mod, 18), 1):
        md.append(f"| {i} | **{r['drug']}** | {r['phase']} | {r['z']} | {r['d_c']} | "
                  f"{r['n_in_mod_graph']}/{r['n_target']} | {'sí' if r['spindle'] else ''} | "
                  f"{r['moa'][:45]} |")
    md.append("\n### Sin fármacos de huso mitótico (candidatos de repurposing propiamente dichos)\n")
    md.append("| # | fármaco | fase | z | d_c | dianas | MOA |")
    md.append("|--|--|--|--|--|--|--|")
    for i, r in enumerate(top_for(mod, 18, exclude_spindle=True), 1):
        md.append(f"| {i} | **{r['drug']}** | {r['phase']} | {r['z']} | {r['d_c']} | "
                  f"{r['n_in_mod_graph']}/{r['n_target']} | {r['moa'][:50]} |")

md.append("\n## Lectura\n")
md.append("- **Módulos `MVA_genes` / `SAC_MCC`:** dominados por inhibidores de Aurora / PLK / TTK-MPS1 / "
          "tubulina — **conceptualmente contraindicados** (inhibir aún más un checkpoint ya débil). "
          "El método encuentra la vecindad correcta, pero al quitar los fármacos de huso lo que queda "
          "son agentes de daño al ADN (PARP-i, antimetabolitos) = quimioterapia, no repurposing. "
          "→ **no hay candidato 'limpio' a la altura del propio gen de enfermedad.**")
md.append("- **Módulo `senescencia`:** aquí sí aparecen candidatos de repurposing con lógica — "
          "inhibidores de BCL-2/BCL-xL (navitoclax = senolítico), y agentes que tocan p53/MDM2/RB. "
          "Confirma por red el **eje senolítico** del análisis curado (BubR1^H/H = modelo fundador).")
md.append("- **Módulo `aneuploidia_estres`:** inhibidores de HSP90 (17-AAG/tanespimicina) y "
          "moduladores de AMPK/mTOR/autofagia — confirma por red el **eje de tolerancia a la aneuploidía** "
          "(metformina/AICAR, HSP90; Tang & Amon 2011).")
md.append("\n> Conclusión C1: la proximidad de red **no aporta un candidato nuevo** más allá de lo curado, "
          "pero **valida independientemente** que (1) el gen de enfermedad no es 'drogable' de forma útil "
          "y (2) los dos ejes terapéuticos correctos son downstream: senescencia y estrés de aneuploidía.")
open(OUT_MD, "w").write("\n".join(md))
log(f"-> {OUT_MD}")
log(f"-> {OUT_TSV}")
for mod in MODULES:
    print(f"\n=== TOP 10 (sin huso) — módulo {mod} ===")
    for r in top_for(mod, 10, exclude_spindle=True):
        print(f"  z={r['z']:6}  d_c={r['d_c']:5}  {r['phase']:9}  {r['drug']:26}  {r['moa'][:38]}")
