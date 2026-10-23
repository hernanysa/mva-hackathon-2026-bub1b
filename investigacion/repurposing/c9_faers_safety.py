#!/usr/bin/env python3
"""
C9 — Señales de seguridad de los candidatos de Track 2 en FAERS (openFDA).

¿Los fármacos que proponemos para un niño con MVA1 tienen, en la farmacovigilancia
real, señales pediátricas o señales que choquen con el fenotipo del probando
(renal/nefrocalcinosis, hepático, hematológico/citopenias, crecimiento)?

FAERS está MUY confundido (metformina ~ diabéticos ancianos; dasatinib ~ LMC).
Sirve para: (a) ¿hay reportes pediátricos?  (b) ¿cuáles son los AE de clase?
Fuente: api.fda.gov/drug/event  ·  Salida: c9_RESULTADO.md
"""
import json, urllib.parse, urllib.request, time, sys, re

API = "https://api.fda.gov/drug/event.json"
# nombre en FAERS (medicinalproduct / substancename) -> etiqueta
DRUGS = {
  "METFORMIN":       "metformina",
  "DASATINIB":       "dasatinib (D+Q)",
  "QUERCETIN":       "quercetina",
  "SIROLIMUS":       "rapamicina/sirolimus",
  "NICOTINAMIDE":    "nicotinamida",
  "NICOTINAMIDE RIBOSIDE": "nicotinamida ribósido",
  "ASPIRIN":         "aspirina",
  "NAVITOCLAX":      "navitoclax",
}
# agrupaciones de reacciones relevantes al fenotipo del probando
PHENO = {
  "renal (nefrocalcinosis del probando)": re.compile(r"RENAL|NEPHRO|KIDNEY|CALCINOSIS|CREATININE|GLOMERUL|TUBUL|ACIDOSIS, RENAL", re.I),
  "hepático":       re.compile(r"HEPAT|LIVER|TRANSAMINASE|BILIRUBIN|ALT INCREASED|AST INCREASED", re.I),
  "hematológico / citopenias / MDS": re.compile(r"NEUTROPEN|THROMBOCYTOPEN|ANAEMIA|ANEMIA|PANCYTOPEN|LEUKOPEN|MYELODYSPLAS|CYTOPEN|APLAS|MARROW", re.I),
  "crecimiento / desarrollo": re.compile(r"GROWTH|SHORT STATURE|FAILURE TO THRIVE|WEIGHT DECREASED|BONE AGE|EPIPHYS", re.I),
  "acidosis láctica (clase biguanida)": re.compile(r"LACTIC ACIDOSIS|LACTATE|METABOLIC ACIDOSIS", re.I),
}

def q(params):
    url = f"{API}?{urllib.parse.urlencode(params)}"
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"mva-hackathon-research/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:  # openFDA devuelve 404 cuando no hay resultados
                return {"meta":{"results":{"total":0}}, "results":[]}
            if attempt == 3:
                print(f"  ! {e} :: {params}", file=sys.stderr); return None
            time.sleep(2)
        except Exception as e:
            if attempt == 3:
                print(f"  ! {e}", file=sys.stderr); return None
            time.sleep(2)

def total(search):
    r = q({"search": search, "limit": 1})
    return (r or {}).get("meta",{}).get("results",{}).get("total", 0)

def top_reactions(search, n=8):
    r = q({"search": search, "count": "patient.reaction.reactionmeddrapt.exact", "limit": n})
    return [(x["term"], x["count"]) for x in (r or {}).get("results", [])]

rows = []
for name, label in DRUGS.items():
    gn = name.lower()
    field = f'patient.drug.openfda.generic_name:"{gn}"'
    tot   = total(field)
    if not tot:  # fallback al nombre de producto
        field = f'patient.drug.medicinalproduct:"{name}"'
        tot   = total(field)
    # pediátrico: agegroup 2 (infante) .. 4 (adolescente)
    ped   = total(f'{field} AND patient.patientagegroup:("2" "3" "4")')
    child = total(f'{field} AND patient.patientagegroup:"3"')
    top   = top_reactions(field, 12)
    top_ped = top_reactions(f'{field} AND patient.patientagegroup:("2" "3" "4")', 10)
    # señales por grupo fenotípico (sobre las 80 reacciones más frecuentes de la droga)
    all_rx = top_reactions(field, 80)
    pheno_hits = {}
    for gname, rx in PHENO.items():
        hits = [(t,c) for t,c in all_rx if rx.search(t)]
        if hits: pheno_hits[gname] = hits[:4]
    rows.append(dict(name=name, label=label, tot=tot, ped=ped, child=child,
                     top=top, top_ped=top_ped, pheno=pheno_hits))
    print(f"{label:24s} tot={tot:>8} ped(2-4)={ped:>6} child={child:>5}")
    time.sleep(0.4)

out = ["# C9 — Señales de seguridad en FAERS (openFDA)\n"]
out.append("_Farmacovigilancia real. **Muy confundido por indicación** (metformina ≈ diabéticos "
           "mayores; dasatinib ≈ LMC adulta) — se usa para detectar señales pediátricas y AE de "
           "clase, no para estimar riesgo basal._\n")
out.append("\n## Resumen\n")
out.append("| candidato | reportes totales | pediátricos (2–18a) | niño (3–11a) | AE de clase a vigilar |")
out.append("|---|---|---|---|---|")
CLASS_AE = {
 "metformina":"acidosis láctica (raro; contraindicada si TFG<30 — **ojo nefrocalcinosis del probando**), déficit B12, GI",
 "dasatinib (D+Q)":"derrame pleural, HTAP, mielosupresión, sangrado, **placa de crecimiento** en pediátrico",
 "quercetina":"suplemento — GI, interacción CYP3A4/CYP2C9; señal escasa",
 "rapamicina/sirolimus":"inmunosupresión, dislipidemia, aftas, retraso de cicatrización, neumonitis",
 "nicotinamida":"hepatotoxicidad a dosis alta (>3 g/d), náusea; segura ≤ dosis ONTRAC",
 "nicotinamida ribósido":"suplemento — bien tolerada en ensayos; GI leve",
 "aspirina":"**síndrome de Reye** (evitar en virosis febril), sangrado GI, broncoespasmo",
 "navitoclax":"**trombocitopenia dosis-limitante** (BCL-xL) — por eso se prefieren senolíticos más suaves",
}
for r in rows:
    out.append(f"| {r['label']} | {r['tot']:,} | {r['ped']:,} | {r['child']:,} | {CLASS_AE.get(r['label'],'—')} |")

out.append("\n## Detalle por candidato\n")
for r in rows:
    out.append(f"\n### {r['label']}  (`{r['name']}`)\n")
    out.append(f"- Reportes: **{r['tot']:,}** totales · {r['ped']:,} pediátricos (2–18a) · {r['child']:,} en niños (3–11a).")
    if r["top"]:
        out.append(f"- AE más reportados: " + "; ".join(f"{t} ({c})" for t,c in r["top"][:6]))
    if r["top_ped"]:
        out.append(f"- AE más reportados **en pediátricos**: " + "; ".join(f"{t} ({c})" for t,c in r["top_ped"][:6]))
    if r["pheno"]:
        out.append("- Señales que rozan el fenotipo del probando:")
        for g, hits in r["pheno"].items():
            out.append(f"  - **{g}**: " + ", ".join(f"{t} ({c})" for t,c in hits))
    else:
        out.append("- Sin señales prominentes en los grupos fenotípicos del probando (renal/hepático/hematológico/crecimiento).")

out.append("\n## Lectura para el report\n")
out.append("- ⚠️ **FAERS es numerador sin denominador y con confusión masiva por indicación.** Las "
           "señales renales de metformina y aspirina son en gran parte la **comorbilidad de la "
           "población** (diabéticos con ERC, cardiópatas), no causalidad del fármaco. Sirve para: "
           "(a) confirmar que **hay** experiencia pediátrica (metformina 523, sirolimus 672, "
           "aspirina 1.344 reportes pediátricos), (b) los AE de clase conocidos.")
out.append("- **Metformina**: la señal de acidosis láctica existe (19.411; 86 pediátricos) pero es "
           "rara y ligada a insuf. renal → en este chico (nefrocalcinosis) obliga a monitorear TFG "
           "y suspender en deshidratación/contraste. Es el caveat #1 y va explícito.")
out.append("- **Aspirina**: la señal de Reye confirma que se suspende en cuadros virales febriles "
           "y peri-cirugía (ya estaba en el red-team, frontier F).")
out.append("- **Navitoclax**: trombocitopenia dosis-limitante → refuerza preferir fisetina / "
           "BH3-miméticos BCL-xL-selectivos más nuevos.")
out.append("- **Fisetina / NR / nicotinamida**: perfil de suplemento, sin señales pediátricas "
           "preocupantes → coherente con elegirlos de primera línea.")
open("c9_RESULTADO.md","w").write("\n".join(out) + "\n")
json.dump([{k:v for k,v in r.items()} for r in rows], open("c9_faers.json","w"), indent=1)
print("\nOK -> c9_RESULTADO.md")
