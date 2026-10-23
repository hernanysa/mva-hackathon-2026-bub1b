#!/usr/bin/env python3
"""C2 — Minería de TEXTO COMPLETO en Europe PMC.

Independiente de 03_pubmed_mining (que usó E-utilities sobre abstracts).
Aquí: Europe PMC search + descarga de full-text XML (Open Access) + escaneo contra
un léxico de fármacos (Broad Repurposing Hub + senoterapéuticos + compuestos
anti-aneuploidía). Objetivo: confirmar/ampliar la lista curada con evidencia de
texto completo, no solo de títulos/abstracts.
"""
import os, re, json, time, urllib.request, urllib.parse, urllib.error, html
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_MD = os.path.join(HERE, "c2_RESULTADO.md")
OUT_JSON = os.path.join(HERE, "c2_hits.json")
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"

def get(url, tries=4, parse="json"):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mva-hackathon-c2/1.0"})
            with urllib.request.urlopen(req, timeout=45) as r:
                raw = r.read().decode("utf-8", "replace")
            return json.loads(raw) if parse == "json" else raw
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            if getattr(e, "code", None) == 404:
                return None
            time.sleep(2 + 3 * i)
    return None

# ---------- léxico de fármacos ----------
lex = {}
hub = os.path.join(HERE, "data", "repurposing_drugs_20200324.txt")
with open(hub, encoding="latin-1") as f:
    for line in f:
        if line.startswith(("!", "pert_iname")):
            continue
        name = line.split("\t", 1)[0].strip().lower()
        name = re.sub(r"\s*\(.*?\)\s*", "", name)
        if len(name) >= 5 and re.match(r"^[a-z0-9][a-z0-9 \-]+$", name) and " " not in name.strip()[-2:]:
            lex[name] = name
EXTRA = ["fisetin", "quercetin", "dasatinib", "navitoclax", "ABT-737", "ABT-263", "piperlongumine",
         "curcumin", "rapamycin", "sirolimus", "metformin", "AICAR", "phenformin", "17-AAG",
         "tanespimycin", "geldanamycin", "17-DMAG", "nicotinamide", "nicotinamide riboside",
         "nicotinamide mononucleotide", "NMN", "resveratrol", "aspirin", "spermidine",
         "hydroxychloroquine", "chloroquine", "celecoxib", "sulforaphane", "EGCG",
         "reversine", "AZ3146", "MPS1-IN-1", "NMS-P715", "BAY 1217389", "CFI-402257",
         "alisertib", "barasertib", "MLN8054", "danusertib", "volasertib", "BI 2536",
         "proscillaridin", "digoxin", "digitoxin", "monensin", "thioridazine", "trifluoperazine",
         "2-deoxyglucose", "2-deoxy-d-glucose", "phenformin", "oligomycin", "antimycin",
         "carboplatin", "cisplatin", "paclitaxel", "vincristine", "etoposide", "doxorubicin",
         "dactinomicin", "actinomycin d", "temsirolimus", "everolimus", "torin", "MLN4924",
         "pevonedistat", "bortezomib", "carfilzomib", "MG132", "chlorpromazine"]
for e in EXTRA:
    lex[e.lower()] = e
lex_pat = re.compile(r"(?<![a-z0-9])(" + "|".join(re.escape(k) for k in sorted(lex, key=len, reverse=True)) + r")(?![a-z0-9])", re.I)
print(f"léxico: {len(lex)} términos")

# ---------- consultas ----------
QUERIES = [
    'BUB1B AND (drug OR compound OR inhibitor OR treatment OR therapy OR rescue)',
    'BUBR1 AND (senescence OR senolytic OR ageing OR aging OR progeroid)',
    'BUB1B AND (senescence OR senolytic)',
    '"mosaic variegated aneuploidy" AND (treatment OR therapy OR management OR drug OR trial)',
    '"mosaic variegated aneuploidy" AND (cancer OR tumor OR surveillance OR rhabdomyosarcoma OR Wilms)',
    'BUBR1 AND (NAD OR SIRT2 OR sirtuin OR "nicotinamide")',
    'aneuploidy AND ("selective" OR "synthetic lethal" OR vulnerability) AND (compound OR drug OR inhibitor)',
    '"chromosomal instability" AND (metformin OR AMPK OR AICAR OR "energy stress")',
    'aneuploid AND (proteotoxic OR "proteotoxic stress" OR autophagy OR HSP90 OR "17-AAG")',
    '"spindle assembly checkpoint" AND (weak OR hypomorph OR partial) AND (rescue OR restore OR compensate)',
    'BubR1 AND (mouse OR model) AND (lifespan OR healthspan OR "life span") AND (treatment OR diet OR drug OR clearance)',
    '"premature chromatid separation" AND (patient OR syndrome) AND (treatment OR outcome OR management)',
    'BUB1B AND rhabdomyosarcoma',
    'CEP57 AND (aneuploidy OR "mosaic variegated")',
    'TRIP13 AND (aneuploidy OR inhibitor OR "DCZ0415" OR degrada*)',
    'aneuploidy AND senescence AND (senolytic OR "p16" OR clearance)',
    '"mitotic checkpoint" AND haploinsufficiency AND tumor',
    '(tetraploid OR tetraploidy) AND (elimination OR "eliminate") AND (resveratrol OR aspirin OR drug)',
    'BUB1B AND (CRISPR OR siRNA OR knockdown) AND (signature OR transcriptome OR "gene expression")',
    'BUBR1 AND insulin AND (growth OR IGF1 OR "growth retardation")',
    '"aneuploidy tolerance" AND (target OR drug OR inhibitor)',
    'MVA AND BUB1B AND (case report OR "long-term" OR follow-up)',
    'senotherapeutic AND (children OR pediatric OR "childhood cancer survivor")',
    'aneuploidy AND (KIF11 OR "Eg5" OR "kinesin") AND selective',
    '"mosaic variegated aneuploidy" AND (fisetin OR dasatinib OR quercetin OR rapamycin OR metformin)',
]

def esearch(q, page_size=50):
    url = f"{EPMC}/search?" + urllib.parse.urlencode({
        "query": q, "format": "json", "pageSize": page_size,
        "resultType": "lite", "sort": "CITED desc"})
    d = get(url)
    if not d:
        return 0, []
    res = d.get("resultList", {}).get("result", [])
    return d.get("hitCount", 0), res

def fulltext_xml(pmcid):
    return get(f"{EPMC}/{pmcid}/fullTextXML", parse="text")

drug_ev = defaultdict(lambda: {"n_art": 0, "pmids": set(), "queries": set(), "contexts": []})
query_summary = []
seen_ft = set()
FT_BUDGET = 220
ft_done = 0

for qi, q in enumerate(QUERIES, 1):
    hits, res = esearch(q)
    query_summary.append((q, hits, len(res)))
    print(f"[{qi:2}/{len(QUERIES)}] hits={hits:<6} kept={len(res):<3}  {q[:70]}", flush=True)
    for r in res:
        pmid = r.get("pmid") or r.get("id")
        pmcid = r.get("pmcid")
        is_oa = r.get("isOpenAccess") == "Y" and pmcid
        title = r.get("title", "")
        # escaneo de título siempre
        for m in set(x.lower() for x in lex_pat.findall(title)):
            e = drug_ev[lex[m]]
            e["pmids"].add(str(pmid)); e["queries"].add(qi)
            e["contexts"].append(f"[T] {title[:140]} (PMID {pmid})")
        # full text si OA y hay presupuesto
        if is_oa and pmcid not in seen_ft and ft_done < FT_BUDGET:
            seen_ft.add(pmcid); ft_done += 1
            xml = fulltext_xml(pmcid)
            time.sleep(0.34)
            if not xml:
                continue
            text = re.sub(r"<[^>]+>", " ", xml)
            text = html.unescape(re.sub(r"\s+", " ", text))
            found = set(x.lower() for x in lex_pat.findall(text))
            for m in found:
                e = drug_ev[lex[m]]
                e["n_art"] += 1
                e["pmids"].add(str(pmid)); e["queries"].add(qi)
                # snippet
                mm = re.search(r".{120}" + re.escape(m) + r".{120}", text, re.I)
                if mm and len(e["contexts"]) < 6:
                    e["contexts"].append(f"[FT] …{mm.group(0).strip()}… (PMID {pmid})")
    time.sleep(0.5)

print(f"\nfull-texts escaneados: {ft_done}")

# ---------- ranking ----------
CURATED = {"fisetin", "quercetin", "dasatinib", "metformin", "nicotinamide", "nicotinamide riboside",
           "resveratrol", "aspirin", "hydroxychloroquine", "celecoxib", "sirolimus", "rapamycin",
           "aicar", "tanespimycin", "17-aag"}
rows = []
for d, e in drug_ev.items():
    score = len(e["pmids"]) * 2 + e["n_art"] + len(e["queries"])
    rows.append((score, d, len(e["pmids"]), e["n_art"], len(e["queries"]),
                 "curado" if d.lower() in CURATED else "NUEVO", e))
rows.sort(reverse=True)

md = ["# C2 — Minería de texto completo (Europe PMC)\n",
      f"{len(QUERIES)} consultas · {ft_done} artículos Open Access con texto completo escaneados · "
      f"léxico de {len(lex)} fármacos/compuestos.\n",
      "## Consultas y volumen\n", "| # | hits EPMC | consulta |", "|--|--|--|"]
for i, (q, h, k) in enumerate(query_summary, 1):
    md.append(f"| {i} | {h} | {q[:90]} |")

md.append("\n## Fármacos por evidencia (texto completo + títulos)\n")
md.append("| fármaco | estado | PMIDs | arts. full-text | # consultas | score |")
md.append("|--|--|--|--|--|--|")
for score, d, npmid, nart, nq, tag, e in rows[:60]:
    md.append(f"| {'**'+d+'**' if tag=='NUEVO' else d} | {tag} | {npmid} | {nart} | {nq} | {score} |")

md.append("\n## Contextos destacados (fármacos NUEVOS vs lista curada)\n")
for score, d, npmid, nart, nq, tag, e in rows:
    if tag != "NUEVO" or score < 5:
        continue
    md.append(f"\n### {d}  (score {score}, {npmid} PMIDs)")
    for c in e["contexts"][:5]:
        md.append(f"- {c}")

open(OUT_MD, "w").write("\n".join(md))
with open(OUT_JSON, "w") as f:
    json.dump({d: {"pmids": sorted(e["pmids"]), "n_art": e["n_art"],
                   "queries": sorted(e["queries"]), "contexts": e["contexts"]}
               for _, d, _, _, _, _, e in rows}, f, indent=1)
print(f"-> {OUT_MD}")
print("\nTOP 20:")
for score, d, npmid, nart, nq, tag, e in rows[:20]:
    print(f"  {score:4}  {tag:6}  {d:30}  PMIDs={npmid} FT={nart} Q={nq}")
