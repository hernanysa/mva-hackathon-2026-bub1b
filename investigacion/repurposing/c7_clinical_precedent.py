#!/usr/bin/env python3
"""
C7 — Precedente clínico SISTEMÁTICO para los candidatos de Track 2.

¿Proponer senolíticos / metformina / precursores de NAD+ / rapamicina para un chico
con MVA1-BUB1B tiene anclaje en ensayos reales en poblaciones análogas
(inestabilidad genómica, progeroides, predisposición a cáncer, sobrevivientes de
cáncer infantil)?  Fuente: ClinicalTrials.gov API v2.  Salida: c7_RESULTADO.md
"""
import json, time, urllib.parse, urllib.request, sys, re
from collections import OrderedDict

API = "https://clinicaltrials.gov/api/v2/studies"
# NB: el parámetro `fields` de la API v2 rechaza (400) varios nombres razonables
# (Conditions, InterventionName, ...). Se pide el estudio completo y se parsea local.

# eje -> lista de (intervención, término de contexto, ¿gold? = población análoga)
BATTERY = {
  "senolisis": [
    ("fisetin",  "senescence frailty aging",              False),
    ("fisetin",  "childhood cancer survivor",             True),
    ("fisetin",  "hematopoietic stem cell transplant",    True),
    ("fisetin",  "bone marrow failure",                   True),
    ("dasatinib quercetin", "senescence",                 False),
    ("dasatinib quercetin", "bone marrow transplant survivor", True),
    ("quercetin", "hematopoietic aging",                  True),
    ("navitoclax", "senescence",                          False),
    ("navitoclax", "myelofibrosis",                       False),
  ],
  "aneuploidia": [
    ("metformin", "Fanconi anemia",                       True),
    ("metformin", "Li-Fraumeni",                          True),
    ("metformin", "ataxia telangiectasia",                True),
    ("metformin", "bone marrow failure",                  True),
    ("metformin", "myelodysplastic syndrome prevention",  True),
    ("metformin", "DNA repair deficiency",                True),
    ("metformin", "cancer prevention hereditary",         True),
    ("metformin", "Lynch syndrome",                       True),
    ("metformin", "progeria",                             True),
    ("metformin", "childhood cancer survivor",            True),
    ("AICAR",     "",                                     False),
  ],
  "nad": [
    ("nicotinamide riboside", "DNA repair",               True),
    ("nicotinamide riboside", "ataxia",                   True),
    ("nicotinamide riboside", "mitochondrial myopathy",   False),
    ("nicotinamide", "skin cancer prevention",            True),
    ("nicotinamide", "actinic keratosis",                 True),
    ("nicotinamide", "Fanconi anemia",                    True),
    ("nicotinamide mononucleotide", "aging",              False),
  ],
  "mtor": [
    ("sirolimus",  "progeria Hutchinson-Gilford",         True),
    ("everolimus", "progeria",                            True),
    ("sirolimus",  "Noonan syndrome",                     True),
    ("everolimus", "RASopathy",                           True),
    ("sirolimus",  "Down syndrome",                       True),
    ("sirolimus",  "chromosomal instability",             True),
  ],
  "contexto": [
    ("aspirin",     "Lynch syndrome",                     True),
    ("aspirin",     "hereditary cancer prevention",       True),
    ("aspirin",     "familial adenomatous polyposis",     True),
    ("resveratrol", "cancer prevention",                  False),
  ],
  "control": [
    ("tanespimycin", "",                                  False),
    ("alvespimycin", "",                                  False),
  ],
  "directo": [
    ("", "mosaic variegated aneuploidy",                  True),
    ("", "premature chromatid separation",                True),
    ("", "BUB1B",                                         True),
    ("", "CEP57",                                         True),
    ("", "premature centromere division",                 True),
  ],
}

def fetch(intr, term, page_size=50):
    params = {"pageSize": str(page_size), "countTotal": "true"}
    if intr: params["query.intr"] = intr
    if term: params["query.term"] = term
    url = f"{API}?{urllib.parse.urlencode(params)}"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mva-hackathon-research/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:
            if attempt == 2:
                print(f"  ! {intr!r}+{term!r}: {e}", file=sys.stderr)
                return {"studies": [], "totalCount": 0}
            time.sleep(2)

def g(d, *path, default=None):
    for k in path:
        if isinstance(d, dict) and k in d: d = d[k]
        else: return default
    return d

def parse_study(s):
    p = s.get("protocolSection", {})
    return {
        "nct":    g(p, "identificationModule", "nctId", default="?"),
        "title":  (g(p, "identificationModule", "briefTitle", default="") or "").strip(),
        "status": g(p, "statusModule", "overallStatus", default="?"),
        "phase":  "/".join(g(p, "designModule", "phases", default=[]) or []) or "NA",
        "type":   g(p, "designModule", "studyType", default="?"),
        "cond":   g(p, "conditionsModule", "conditions", default=[]) or [],
        "intr":   [i.get("name","") for i in g(p, "armsInterventionsModule", "interventions", default=[]) or []],
        "n":      g(p, "designModule", "enrollmentInfo", "count", default=None),
        "start":  g(p, "statusModule", "startDateStruct", "date", default=""),
        "sponsor":g(p, "sponsorCollaboratorsModule", "leadSponsor", "name", default=""),
        "results":bool(g(p, "statusModule", "resultsFirstPostDateStruct", "date", default="")),
    }

seen = OrderedDict()
axis_of = {}
nq = 0
for axis, rows in BATTERY.items():
    for intr, term, is_gold in rows:
        nq += 1
        res = fetch(intr, term)
        studies = res.get("studies", []) or []
        print(f"[{axis:11s}] intr={intr or '-':24s} term={term or '-':32s} -> {len(studies):3d} (tot {res.get('totalCount','?')})")
        for s in studies:
            d = parse_study(s); nct = d["nct"]
            if nct not in seen:
                d["why"] = set(); d["gold"] = False; seen[nct] = d
            seen[nct]["why"].add(f"{intr}·{term}".strip("·"))
            if is_gold: seen[nct]["gold"] = True
            axis_of.setdefault(nct, set()).add(axis)
        time.sleep(0.2)

CAND = re.compile(r"fisetin|dasatinib|quercetin|navitoclax|metformin|AICAR|nicotinamide|"
                  r"sirolimus|rapamycin|everolimus|aspirin|resveratrol|tanespimycin|alvespimycin", re.I)
NOISE = re.compile(r"meniscus|sleep quality|periodont|denture|hair loss|jet lag|skin hydration|"
                   r"exercise performance|muscle soreness", re.I)

def relevant(d):
    if d["nct"] == "?": return False
    blob = (d["title"]+" "+" ".join(d["intr"])+" "+" ".join(d["cond"])).lower()
    if NOISE.search(blob) and not d["gold"]: return False
    # para ejes con fármaco: tiene que mencionarlo. para 'directo': basta la condición.
    if "directo" in axis_of.get(d["nct"], set()):
        return True
    return bool(CAND.search(d["title"]+" "+" ".join(d["intr"])))

rel = [d for d in seen.values() if relevant(d)]
gold = [d for d in rel if d["gold"]]
with_results = [d for d in rel if d["results"]]

PH_ORD = {"PHASE3":0,"PHASE2/PHASE3":1,"PHASE2":2,"PHASE1/PHASE2":3,"PHASE1":4,"EARLY_PHASE1":5,"NA":6}
def sortkey(d): return (0 if d["status"]=="COMPLETED" else 1, PH_ORD.get(d["phase"],9), d["nct"])

out = []
out.append("# C7 — Precedente clínico de los candidatos de Track 2\n")
out.append(f"_ClinicalTrials.gov API v2 · {nq} búsquedas (fármaco × contexto) · "
           f"{len(seen)} estudios únicos · {len(rel)} relevantes · {len(gold)} en poblaciones "
           f"análogas · {len(with_results)} con resultados publicados._\n")
out.append("**La pregunta:** ¿estos fármacos ya se probaron clínicamente en gente parecida a un "
           "MVA1 — inestabilidad genómica, progeroides, predisposición a cáncer, sobrevivientes "
           "de cáncer infantil?\n")

# precedentes VERIFICADOS a mano (leído el registro completo) — el fármaco de interés ES el
# objeto del ensayo, no un co-fármaco de contexto (p.ej. sirolimus como profilaxis de EICH).
VERIFIED = {
 # (registro leído vía API: título oficial, fase, N y EDAD de elegibilidad — ver c7_verified.json)
 "NCT03398824":"metformina en anemia de Fanconi — 6–35 a, Phase 2 COMPLETO, n=15 (14 tratados), respuesta hematológica 4/13 (31%), sin acidosis ni eventos ≥G3 (Blood Adv 2022)",
 "NCT06519786":"metformina en citopenia de anemia de Fanconi — niños y adolescentes 5–18 a, Phase 3, n=30, estado 'unknown'",
 "NCT01981525":"metformina en Li-Fraumeni (predisposición a cáncer por TP53) — ADULTOS ≥18 a, Phase 1 COMPLETO, n=26",
 "NCT02733679":"metformina + pioglitazona en ataxia-telangiectasia (RAMP; inestabilidad genómica bialélica) — 18–30 a, Phase 4 COMPLETO, n=27",
 "NCT04733534":"SEN-SURVIVORS: fisetina y D+Q en fragilidad de sobrevivientes ADULTOS (≥18 a) de cáncer infantil — Phase 2, n=120. NO pediátrico",
 "NCT04313634":"senolíticos (D+Q / fisetina) y salud ósea en ADULTOS MAYORES ≥60 a — Phase 2 COMPLETO, n=74. NO pediátrico",
 "NCT02652052":"D+Q en sobrevivientes ADULTOS (≥18 a) de trasplante de células madre (HTSS) — Phase 1 COMPLETO, n=9",
 "NCT04870866":"NR/suplementación de NAD en ataxia-telangiectasia — ≥3 a, Phase 2, n=13, activo",
 "NCT06324877":"nicotinamida ribósido en ataxia-telangiectasia ('ATNAD', disfunción mitocondrial) — single-arm, n=10, estado 'unknown'",
 "NCT04192136":"NR + ejercicio en ataxia de Friedreich — 10–40 a, n=75, COMPLETO",
 "NCT05955924":"SPRINTR: nicotinamida para quimioprevención de carcinoma queratinocítico en receptores ADULTOS de trasplante de órgano sólido — Phase 3, n=396",
 "NCT02579044":"everolimus + lonafarnib en progeria (HGPS y laminopatías progeroides) — 18 meses–25 a, Phase 1/2, n=80, Boston Children's",
 "NCT06950385":"SERENTA: rapamicina encapsulada (eRapa) en poliposis adenomatosa familiar — ADULTOS ≥18 a, Phase 3, n=168",
 "NCT02497820":"CaPP3 (registro Israel): aspirina 600 vs 300 vs 100 mg en portadores de Lynch — ADULTOS ≥18 a, Phase 3, n=1800, 'not yet recruiting'",
 "NCT02813824":"AAS-Lynch: aspirina dosis baja para prevención de adenomas/CCR en Lynch — ADULTOS 18–75 a, Phase 3, n=852",
}

out.append("\n## 1. Precedentes VERIFICADOS en poblaciones análogas (registro leído; edades de elegibilidad exactas)\n")
out.append("_El fármaco de interés es el objeto del ensayo (no un co-fármaco de contexto). "
           "**Solo 5 de 15 incluyen explícitamente niños o adolescentes** (Fanconi ×2: 6–35 a y 5–18 a; A-T ≥3 a; Friedreich 10–40 a; progeria desde 18 meses); NCT06324877 no registra edad mínima; el resto son adultos. **El eje senolítico solo tiene ensayos en adultos.**_\n")
out.append("| NCT | qué es |")
out.append("|---|---|")
for nct, desc in VERIFIED.items():
    out.append(f"| [{nct}](https://clinicaltrials.gov/study/{nct}) | {desc} |")

out.append("\n## 1b. Todos los hits auto-clasificados como 'población análoga' (sin curar — puede haber confusión de contexto)\n")
out.append("| NCT | intervención | fase | estado | condición | eje |")
out.append("|---|---|---|---|---|---|")
for d in sorted(gold, key=sortkey):
    ints = ", ".join(sorted({i for i in d["intr"] if CAND.search(i)})[:3]) or ", ".join(d["intr"][:2])
    res = " ·📊" if d["results"] else ""
    v = " ✅" if d["nct"] in VERIFIED else ""
    out.append(f"| [{d['nct']}](https://clinicaltrials.gov/study/{d['nct']}){v} | {ints} | {d['phase']} | "
               f"{d['status']}{res} | {'; '.join(d['cond'][:2])} | {', '.join(sorted(axis_of.get(d['nct'],[])))} |")
out.append("\n_📊 = resultados publicados · ✅ = verificado a mano (tabla 1)_\n")

out.append("\n## 2. Todos los ensayos relevantes, por eje\n")
NAMES = {"senolisis":"Eje 1 — senólisis (fisetina, D+Q, navitoclax)",
         "aneuploidia":"Eje 2 — metformina / activación de AMPK",
         "nad":"Upstream — precursores de NAD+","mtor":"mTOR — rapamicina / everolimus",
         "contexto":"Contexto — aspirina / resveratrol","control":"Control mecanístico — HSP90i",
         "directo":"Enfermedad directa — MVA / PCS / BUB1B / CEP57"}
for axis in BATTERY:
    ds = [d for d in rel if axis in axis_of.get(d["nct"], set())]
    out.append(f"\n### {NAMES[axis]}  ({len(ds)})\n")
    if not ds: out.append("_Sin ensayos._"); continue
    out.append("| NCT | intervención | fase | estado | condición | N |")
    out.append("|---|---|---|---|---|---|")
    for d in sorted(ds, key=sortkey):
        out.append(f"| [{d['nct']}](https://clinicaltrials.gov/study/{d['nct']}) | {', '.join(d['intr'][:3])} | "
                   f"{d['phase']} | {d['status']} | {'; '.join(d['cond'][:2])} | {d['n'] or '?'} |")

open("c7_RESULTADO.md","w").write("\n".join(out) + "\n")
json.dump({n:{k:(sorted(v) if isinstance(v,set) else v) for k,v in d.items()} for n,d in seen.items()},
          open("c7_studies.json","w"), indent=1, default=str)
print(f"\nOK -> c7_RESULTADO.md ({len(rel)} relevantes · {len(gold)} análogos · {len(with_results)} con resultados)")
