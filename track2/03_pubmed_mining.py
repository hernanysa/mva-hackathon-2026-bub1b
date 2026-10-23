#!/usr/bin/env python3
"""Etapa 3 - minería sistemática de PubMed. ~50 búsquedas dirigidas al eje
BUB1B / SAC / aneuploidía / senescencia / repurposing. Resumible por query."""
import os, sys, json, re, time, csv, urllib.parse, xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(__file__))
from lib import get, eprint

OUT = os.path.join(os.path.dirname(__file__), "out")
LIT = f"{OUT}/03_lit"; os.makedirs(LIT, exist_ok=True)
EUT = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
TOOL = "&tool=mva-hackathon-track2"

QUERIES = {
 "bub1b_drug": 'BUB1B[tiab] AND (drug OR inhibitor OR therapy OR treatment OR pharmacolog*[tiab])',
 "bubr1_drug": 'BUBR1[tiab] AND (drug OR inhibitor OR therapy OR compound[tiab])',
 "bubr1_senescence": 'BUBR1[tiab] AND (senescence OR senescent OR "cellular senescence")[tiab]',
 "bubr1_aging_lifespan": 'BubR1[tiab] AND (aging OR ageing OR lifespan OR healthspan OR progeroid)[tiab]',
 "bubr1_hypomorph": '(BubR1 AND (hypomorph* OR "H/H" OR insufficiency OR "low expression"))[tiab]',
 "bubr1_senolytic": '(BubR1 OR BUB1B)[tiab] AND (senolytic OR "senescent cell clearance" OR INK-ATTAC OR p16)[tiab]',
 "mva_treatment": '"mosaic variegated aneuploidy"[tiab] AND (treatment OR therapy OR therapeutic OR drug OR management OR surveillance)[tiab]',
 "mva_review": '"mosaic variegated aneuploidy"[tiab] AND (review OR management OR clinical)[tiab]',
 "sac_repurposing": '"spindle assembly checkpoint"[tiab] AND (repurpos* OR "drug repurposing" OR "approved drug")[tiab]',
 "sac_inhibitor_cancer": '("spindle assembly checkpoint" OR "mitotic checkpoint")[tiab] AND (inhibitor OR therapeutic)[tiab] AND cancer[tiab]',
 "aneuploidy_selective": 'aneuploidy[tiab] AND (selective OR "selective killing" OR vulnerability OR "synthetic lethal" OR "Achilles heel")[tiab]',
 "aneuploidy_compound": 'aneuploid*[tiab] AND (compound OR "small molecule" OR drug)[tiab] AND (proliferation OR viability OR "cell death")[tiab]',
 "aneuploidy_proteotoxic": 'aneuploidy[tiab] AND ("proteotoxic stress" OR "protein folding" OR HSP90 OR proteostasis OR autophagy)[tiab]',
 "aneuploidy_metabolic": 'aneuploidy[tiab] AND ("metabolic stress" OR AMPK OR "energy stress" OR glucose OR AICAR OR metformin)[tiab]',
 "aneuploidy_p53": 'aneuploidy[tiab] AND (p53 OR TP53 OR "hyperactivation" OR "cell cycle arrest")[tiab]',
 "cin_therapeutic": '"chromosomal instability"[tiab] AND (therapeutic OR treatment OR drug OR target OR vulnerability)[tiab]',
 "cin_selective_drug": '("chromosomal instability" OR CIN)[tiab] AND (selective OR "selectively kill" OR paclitaxel OR taxane)[tiab]',
 "pcs_syndrome": '("premature chromatid separation" OR "PCS syndrome")[tiab]',
 "trip13_inhibitor": 'TRIP13[tiab] AND (inhibitor OR DCZ0415 OR "small molecule" OR therapeutic)[tiab]',
 "mps1_ttk_approved": '(TTK OR MPS1)[tiab] AND kinase[tiab] AND (inhibitor OR clinical OR trial)[tiab]',
 "aurora_b_clinical": '"aurora kinase B"[tiab] AND (clinical OR approved OR barasertib OR "phase")[tiab]',
 "rhabdomyosarcoma_predisposition": 'rhabdomyosarcoma[tiab] AND ("cancer predisposition" OR surveillance OR chemoprevention OR "germline")[tiab]',
 "wilms_surveillance": '"Wilms tumor"[tiab] AND surveillance[tiab] AND (predisposition OR syndrome)[tiab]',
 "aneuploidy_antioxidant": 'aneuploidy[tiab] AND ("oxidative stress" OR "reactive oxygen" OR antioxidant OR "N-acetylcysteine")[tiab]',
 "bub1b_wilms": 'BUB1B[tiab] AND (Wilms OR rhabdomyosarcoma OR "childhood cancer")[tiab]',
 "mitotic_slippage_drug": '"mitotic slippage"[tiab] AND (drug OR prevent OR MCL1 OR "cyclin B")[tiab]',
 "hdac_aneuploidy": '(HDAC OR "histone deacetylase")[tiab] AND (aneuploidy OR "chromosome segregation" OR "mitotic")[tiab]',
 "metformin_aneuploidy_cin": 'metformin[tiab] AND (aneuploidy OR "chromosomal instability" OR "chromosome missegregation")[tiab]',
 "rapamycin_senescence_progeria": '(rapamycin OR sirolimus OR everolimus)[tiab] AND (senescence OR progeria OR "premature aging")[tiab]',
 "quercetin_dasatinib_senolytic": '(dasatinib AND quercetin)[tiab] AND (senolytic OR senescent)[tiab]',
 "fisetin_senolytic": 'fisetin[tiab] AND (senolytic OR senescence OR "healthspan")[tiab]',
 "bub1b_expression_restore": 'BUB1B[tiab] AND (overexpression OR "gene therapy" OR "expression restoration" OR upregulat*)[tiab]',
 "aneuploidy_immune_clearance": 'aneuploid*[tiab] AND ("immune" OR "natural killer" OR "NK cell" OR clearance OR surveillance)[tiab]',
 "cgas_sting_micronuclei": '(micronuclei OR micronucleus)[tiab] AND (cGAS OR STING OR "innate immune")[tiab] AND (chromosom* OR aneuploid*)[tiab]',
 "kif11_eg5_clinical": '(KIF11 OR Eg5 OR "kinesin spindle protein")[tiab] AND (inhibitor OR clinical OR ispinesib OR filanesib)[tiab]',
 "mva_case_reports": '"mosaic variegated aneuploidy"[tiab] AND ("case report" OR patient OR "clinical course")[tiab]',
 "chromosome_missegregation_prevent": '"chromosome missegregation"[tiab] AND (prevent OR reduce OR suppress OR rescue)[tiab]',
 "taxane_cin_low_dose": '(paclitaxel OR taxane OR "low-dose")[tiab] AND ("chromosomal instability" OR "chromosome missegregation")[tiab]',
 "autophagy_inhibitor_aneuploidy": '(chloroquine OR hydroxychloroquine OR "autophagy inhibit*")[tiab] AND (aneuploid* OR "chromosomal instability")[tiab]',
 "nampt_nad_senescence": '(NAD+ OR nicotinamide OR NMN OR NR)[tiab] AND (senescence OR "DNA damage" OR aging)[tiab] AND (mouse OR model)[tiab]',
}

def esearch(term, retmax=60):
    d = get(f"{EUT}/esearch.fcgi?db=pubmed&retmode=json&sort=relevance&retmax={retmax}"
            f"&term={urllib.parse.quote(term)}{TOOL}", min_gap=0.4)
    return (d or {}).get("esearchresult", {}).get("idlist", [])

def efetch(pmids):
    if not pmids: return []
    x = get(f"{EUT}/efetch.fcgi?db=pubmed&retmode=xml&id={','.join(pmids)}{TOOL}",
            min_gap=0.4, raw=True)
    if not x: return []
    out = []
    try:
        root = ET.fromstring(x)
    except ET.ParseError:
        return []
    for art in root.findall(".//PubmedArticle"):
        pmid = art.findtext(".//PMID") or ""
        title = "".join(art.find(".//ArticleTitle").itertext()) if art.find(".//ArticleTitle") is not None else ""
        abst = " ".join("".join(a.itertext()) for a in art.findall(".//Abstract/AbstractText"))
        year = art.findtext(".//PubDate/Year") or art.findtext(".//PubDate/MedlineDate") or ""
        jrnl = art.findtext(".//Journal/ISOAbbreviation") or ""
        out.append({"pmid": pmid, "year": year, "journal": jrnl, "title": title, "abstract": abst})
    return out

index = {}
for name, term in QUERIES.items():
    fp = f"{LIT}/{name}.json"
    if os.path.exists(fp):
        index[name] = json.load(open(fp)); eprint(f"  {name}: cache"); continue
    eprint(f"query {name} ...")
    pmids = esearch(term)
    arts = []
    for i in range(0, len(pmids), 20):
        arts += efetch(pmids[i:i+20])
    rec = {"query": term, "n": len(arts), "articles": arts}
    json.dump(rec, open(fp, "w"), ensure_ascii=False)
    index[name] = rec
    eprint(f"  {name}: {len(arts)} artículos")

# --- extracción de menciones de fármacos ---
DRUGS = ("metformin|rapamycin|sirolimus|everolimus|temsirolimus|dasatinib|quercetin|fisetin|"
 "navitoclax|chloroquine|hydroxychloroquine|paclitaxel|docetaxel|vinblastine|vincristine|"
 "nocodazole|colchicine|AICAR|17-AAG|tanespimycin|geldanamycin|ganetespib|17-DMAG|"
 "vorinostat|romidepsin|panobinostat|belinostat|entinostat|"
 "N-acetylcysteine|NAC|nicotinamide|nicotinamide riboside|NMN|resveratrol|spermidine|"
 "alisertib|barasertib|danusertib|tozasertib|volasertib|BI-2536|GSK461364|onvansertib|"
 "ispinesib|filanesib|SB-743921|MK-0731|litronesib|"
 "reversine|MPS1-IN|BAY-1217389|CFI-402257|empesertib|"
 "DCZ0415|proTAME|apcin|bortezomib|carfilzomib|ixazomib|"
 "aspirin|celecoxib|statin|simvastatin|atorvastatin|"
 "thioridazine|mefloquine|niclosamide|disulfiram|itraconazole|"
 "cisplatin|carboplatin|doxorubicin|etoposide|dactinomycin|cyclophosphamide")
rx = re.compile(r"\b(" + DRUGS + r")\b", re.I)
KEYW = re.compile(r"aneuploid|chromosom\w* instab|missegregation|spindle assembly checkpoint|"
                  r"mitotic checkpoint|BUB1B|BUBR1|senescen|senolytic|premature chromatid|"
                  r"chromosomal instability|micronucle", re.I)

ment = {}
for name, rec in index.items():
    for a in rec["articles"]:
        text = f"{a['title']} {a['abstract']}"
        drugs = {m.group(1).lower() for m in rx.finditer(text)}
        if not drugs: continue
        rel = bool(KEYW.search(text))
        for d in drugs:
            ment.setdefault(d, {"pmids": set(), "queries": set(), "relevant_context": 0, "titles": []})
            ment[d]["pmids"].add(a["pmid"]); ment[d]["queries"].add(name)
            if rel:
                ment[d]["relevant_context"] += 1
                if len(ment[d]["titles"]) < 4:
                    ment[d]["titles"].append(f"[{a['year']}] {a['title'][:140]} (PMID {a['pmid']})")

with open(f"{OUT}/03_drug_mentions.tsv", "w", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["drug", "n_pmids", "n_relevant_context", "n_queries", "pmids", "queries", "example_titles"])
    for d, v in sorted(ment.items(), key=lambda x: -x[1]["relevant_context"]):
        w.writerow([d, len(v["pmids"]), v["relevant_context"], len(v["queries"]),
                    ",".join(sorted(v["pmids"])), ";".join(sorted(v["queries"])),
                    " || ".join(v["titles"])])
eprint(f"03 OK — {sum(r['n'] for r in index.values())} artículos, {len(ment)} fármacos mencionados")
