# Literature check — every external claim in the Track 2 report

Each claim was checked against the abstract (PubMed efetch) or the full text (Europe PMC / PMC),
on 2026-10-07. Numbers in the report that come from our own analyses are checked separately and
automatically by `audit_report.py` (138 checks, all passing).

| Report claim | Source | Verified text (quote or paraphrase) | Status |
|---|---|---|---|
| BUB1B biallelic mutations cause MVA with childhood cancer; embryonal rhabdomyosarcoma reported | Hanks et al., Nat Genet 2004;36:1159 (PMID 15475955) | "In five families with MVA, including two with embryonal rhabdomyosarcoma, we identified truncating and missense mutations of BUB1B" | ✔ |
| Bilateral Wilms tumour in BUB1B-related MVA | Ochiai et al., Pediatr Blood Cancer 2019;66:e27804 (PMID 31081598) | "a 38-month-old … male with PCS/MVA syndrome bearing biallelic BUB1B germline mutations who suffered from bilateral Wilms tumor" | ✔ |
| Cancer risk in MVA is increased but cannot be quantified; renal US every 3 months from birth to age 7 for all MVA types | Nakano et al., Clin Cancer Res 2024;30:5009 (PMID 39264246; full text PMC11705613) | "Whereas cancer risk is clearly increased in MVA, the rarity of the syndrome hampers establishment of an accurate risk assessment"; "renal ultrasound surveillance every 3 months from birth until age 7, for all MVA conditions" | ✔ |
| Genome-instability disorders can be unusually sensitive to radiation and chemotherapy | Nakano et al. 2024 (abstract) | "exquisite sensitivity to anticancer treatments such as ionizing radiation and chemotherapy" (stated for the group, not specifically for MVA) | ✔ (worded as a group statement) |
| Mice with low BubR1 develop progressive aneuploidy and progeroid features | Baker et al., Nat Genet 2004;36:744 (PMID 15208629) | "mutant mice with low levels of … BubR1 develop progressive aneuploidy along with a variety of progeroid features" | ✔ |
| Complete loss of BubR1 is embryonic-lethal in mice | Kim et al., Cancer Biol Ther 2005;4:164 (PMID 15655361) | "…in part due to the embryonic lethality of complete [BubR1 deficiency]" | ✔ |
| Clearance of p16Ink4a-positive cells in the BubR1 progeroid background delays pathology incl. skeletal muscle | Baker et al., Nature 2011;479:232 (PMID 22048312) | "in the BubR1 progeroid mouse background, INK-ATTAC removes p16Ink4a-positive senescent cells … in adipose tissue, skeletal muscle and eye … removal … delayed onset of these phenotypes" | ✔ |
| Aneuploidy-selective compounds: AICAR, 17-AAG and chloroquine | Tang et al., Cell 2011;144:499 (PMID 21315436) | "the energy stress-inducing agent AICAR, the protein folding inhibitor 17-AAG, and the autophagy inhibitor chloroquine" | ✔ (chloroquine added) |
| BubR1 declines with age via NAD⁺/SIRT2 (K668); SIRT2 or NMN raise BubR1; SIRT2 extends lifespan of BubR1-hypomorphs | North et al., EMBO J 2014;33:1438 (PMID 24825348) | "loss of BubR1 levels with age is due to a decline in NAD+ and the ability of SIRT2 to maintain lysine-668 … deacetylated"; "Overexpression of SIRT2 or treatment … with … NMN increases BubR1 abundance in vivo"; "increases median lifespan, with a greater effect in male mice" | ✔ |
| NR in ataxia-telangiectasia: 24 patients (17 children), 25 mg/kg/day, 4 months, tolerated well, improved ataxia and IgG | Veenhuis et al., Mov Disord 2021;36:2951 (PMID 34515380; full text PMC9291897) | "24 patients with A-T were treated with NR (25 mg/kg bodyweight per day) during four consecutive months"; "17 were children"; "Treatment with NR is tolerated well"; "After NR withdrawal, ataxia scores worsened" | ✔ (no 900 mg cap in the paper — removed) |
| Metformin in Fanconi anaemia: dosing, ages, safety, response | Pollard et al., Blood Adv 2022;6:3803 (PMID 35500223; full text PMC9631552) | dose-escalation to 500 mg b.i.d. (<10 y) / 1000 mg b.i.d. (≥10 y); median age 9.4 y; diarrhoea 12/14; "No subjects developed hypoglycemia or metabolic acidosis"; no grade ≥3 AEs; response 4/13 | ✔ (also machine-checked) |
| Dasatinib: bone growth and development events in children | Gore et al., J Clin Oncol 2018;36:1330 (PMID 29498925) | "Bone growth and development events were reported in 4% of patients" | ✔ |
| Clonal chromosomal abnormalities in Ph-negative cells during TKI therapy | Wang et al., Ann Hematol 2013;92:1625 (PMID 23793947) | "clonal cytogenetic abnormalities in Ph- metaphases have been widely observed after treatment with imatinib, or dasatinib/nilotinib" | ✔ |
| Navitoclax: on-target dose-limiting thrombocytopenia | Mahadevan et al., J Hematol Oncol 2025;18:98 (PMID 41225624) | "inhibition of BCL-XL with navitoclax resulted in on-target dose-limiting thrombocytopenia" | ✔ |
| Genetic support could double clinical success | Nelson et al., Nat Genet 2015;47:856 (PMID 26121088) | "selecting genetically supported targets could double the success rate in clinical development" | ✔ |
| Network proximity method | Guney et al., Nat Commun 2016;7:10331 (PMID 26831545) | title/method | ✔ |
| Fisetin is a senotherapeutic | Yousefzadeh et al., EBioMedicine 2018;36:18 (PMID 30279143) | title | ✔ |
| GSE134781 model: patient allele L1012P (mouse L1002P) and X753; carrier muscle | Sieben et al., J Clin Invest 2020;130:171 (PMID 31738183) + GEO series record | "we mimicked the BUBR1 L1012P mutation in mice (BubR1 L1002P) … BubR1+/L1002P and BubR1+/X753" | ✔ |

## Statements removed or corrected because they could not be verified

1. "≈75 % cancer risk" in BUB1B-related MVA — not supported; the 2024 guideline says the risk cannot be estimated.
2. "Tumours mostly before age five" — the cited source (PMID 18548531) describes sibs *without* BUB1B mutations and without cancer.
3. Leukaemia as a reported tumour in BUB1B-related MVA — no primary source found in this audit; removed.
4. NR "maximum 900 mg/day" — not in the Veenhuis paper (came from a secondary review); removed.
5. "≈10 % of normal BubR1" in hypomorphic mice — not in the abstract; replaced by "low BubR1 levels".
6. Tang et al. listed only AICAR and 17-AAG — chloroquine added.
7. The 2024 surveillance guideline was cited with a wrong title — corrected to Nakano et al.
8. "36 subjects without serious adverse events" for fisetin — secondary source, unverifiable; not used.
9. Earlier in the project (registry re-read): adult trials described as paediatric, a metformin dose
   that did not match the protocol, and a mouse allele described as the proband's residue — all corrected.
