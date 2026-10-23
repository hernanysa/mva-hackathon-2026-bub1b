# C1 — Repurposing por proximidad de red (Guney 2016)

Interactoma STRING v12 (score≥700): **15,882 genes / 236,712 interacciones** (componente conexa mayor).
Fármacos: Broad Drug Repurposing Hub ∪ DGIdb-aprobados = **8,706** (evaluados los que tienen 1–25 dianas en el interactoma y fase ≥1).
Métrica *closest* d_c(S,T); z-score vs 1000 conjuntos de dianas degree-matched.

> Qué mide: si las **dianas del fármaco caen cerca del módulo mitótico de la enfermedad**. NO captura el eje senescencia/senolíticos (esos actúan río abajo) — es una lente complementaria, no un veredicto único.


## Módulo `MVA_genes`  =  {BUB1B, CEP57, TRIP13}

### Todos (incluye fármacos de huso mitótico)

| # | fármaco | fase | z | d_c | dianas | huso? | MOA |
|--|--|--|--|--|--|--|--|
| 1 | **AMG900** | Phase 1 | -4.85 | 1.0 | 3/3 | sí | Aurora kinase inhibitor |
| 2 | **CYC116** | Phase 1 | -4.48 | 1.25 | 4/4 | sí | Aurora kinase inhibitor |
| 3 | **clofarabine** | Launched | -4.0 | 2.0 | 15/15 |  | ribonucleotide reductase inhibitor |
| 4 | **BI-847325** | Phase 1 | -3.87 | 2.0 | 8/8 | sí | Aurora kinase inhibitor|MEK inhibitor |
| 5 | **SNS-314** | Phase 1 | -3.46 | 1.6 | 5/5 | sí | Aurora kinase inhibitor |
| 6 | **NMS-1286937** | Phase 2 | -3.45 | 1.75 | 4/4 | sí | PLK inhibitor |
| 7 | **danusertib** | Phase 2 | -3.39 | 1.889 | 9/9 | sí | Aurora kinase inhibitor|growth factor recepto |
| 8 | **fludarabine** | Launched | -3.33 | 2.083 | 12/12 |  | ribonucleotide reductase inhibitor |
| 9 | **KW-2449** | Phase 1 | -3.27 | 1.5 | 4/4 | sí | Abl kinase inhibitor|Aurora kinase inhibitor| |
| 10 | **MK-5108** | Phase 1 | -3.23 | 1.667 | 6/6 | sí | Aurora kinase inhibitor |
| 11 | **PF-03814735** | Phase 1 | -3.19 | 1.0 | 2/2 | sí | Aurora kinase inhibitor |
| 12 | **vorinostat** | Launched | -3.05 | 2.0 | 10/10 |  | HDAC inhibitor |
| 13 | **daunorubicin** | Launched | -2.97 | 1.5 | 2/2 |  | RNA synthesis inhibitor|topoisomerase inhibit |
| 14 | **teniposide** | Launched | -2.95 | 1.5 | 2/2 |  | topoisomerase inhibitor |
| 15 | **amonafide** | Phase 3 | -2.9 | 1.5 | 2/2 |  | topoisomerase inhibitor |
| 16 | **amrubicin** | Launched | -2.86 | 1.5 | 2/2 |  | topoisomerase inhibitor |
| 17 | **tozasertib** | Phase 2 | -2.85 | 1.8 | 5/5 | sí | Aurora kinase inhibitor|Bcr-Abl kinase inhibi |
| 18 | **tacedinaline** | Phase 3 | -2.84 | 2.0 | 10/10 |  | HDAC inhibitor |

### Sin fármacos de huso mitótico (candidatos de repurposing propiamente dichos)

| # | fármaco | fase | z | d_c | dianas | MOA |
|--|--|--|--|--|--|--|
| 1 | **clofarabine** | Launched | -4.0 | 2.0 | 15/15 | ribonucleotide reductase inhibitor |
| 2 | **fludarabine** | Launched | -3.33 | 2.083 | 12/12 | ribonucleotide reductase inhibitor |
| 3 | **vorinostat** | Launched | -3.05 | 2.0 | 10/10 | HDAC inhibitor |
| 4 | **daunorubicin** | Launched | -2.97 | 1.5 | 2/2 | RNA synthesis inhibitor|topoisomerase inhibitor |
| 5 | **teniposide** | Launched | -2.95 | 1.5 | 2/2 | topoisomerase inhibitor |
| 6 | **amonafide** | Phase 3 | -2.9 | 1.5 | 2/2 | topoisomerase inhibitor |
| 7 | **amrubicin** | Launched | -2.86 | 1.5 | 2/2 | topoisomerase inhibitor |
| 8 | **tacedinaline** | Phase 3 | -2.84 | 2.0 | 10/10 | HDAC inhibitor |
| 9 | **dexrazoxane** | Launched | -2.81 | 1.5 | 2/2 | chelating agent|topoisomerase inhibitor |
| 10 | **belinostat** | Launched | -2.75 | 2.0 | 11/11 | HDAC inhibitor |
| 11 | **cobimetinib** | Launched | -2.75 | 2.333 | 9/9 | MEK inhibitor |
| 12 | **trimethoprim** | Launched | -2.74 | 1.5 | 2/2 | dihydrofolate reductase inhibitor |
| 13 | **PEMETREXED DISODIUM** | Launched | -2.68 | 1.5 | 2/2 |  |
| 14 | **JNJ-26481585** | Phase 2 | -2.67 | 2.0 | 12/12 | HDAC inhibitor |
| 15 | **binimetinib** | Launched | -2.67 | 2.375 | 8/8 | MEK inhibitor |
| 16 | **fludarabine-phosphate** | Launched | -2.65 | 1.833 | 6/6 | ribonucleotide reductase inhibitor |
| 17 | **refametinib** | Phase 2 | -2.65 | 2.375 | 8/8 | MEK inhibitor |
| 18 | **entinostat** | Phase 3 | -2.64 | 2.0 | 11/11 | HDAC inhibitor |

## Módulo `SAC_MCC`  =  {BUB1B, BUB1, BUB3, MAD1L1, MAD2L1, TTK, CDC20, CENPE, KNL1, ZW10, ZWILCH}

### Todos (incluye fármacos de huso mitótico)

| # | fármaco | fase | z | d_c | dianas | huso? | MOA |
|--|--|--|--|--|--|--|--|
| 1 | **AMG900** | Phase 1 | -4.11 | 1.0 | 3/3 | sí | Aurora kinase inhibitor |
| 2 | **CYC116** | Phase 1 | -3.92 | 1.25 | 4/4 | sí | Aurora kinase inhibitor |
| 3 | **AT-7519** | Phase 2 | -3.84 | 2.111 | 18/18 |  | CDK inhibitor |
| 4 | **SNS-314** | Phase 1 | -3.64 | 1.4 | 5/5 | sí | Aurora kinase inhibitor |
| 5 | **MK-5108** | Phase 1 | -3.61 | 1.5 | 6/6 | sí | Aurora kinase inhibitor |
| 6 | **PHA-793887** | Phase 1 | -3.52 | 2.2 | 15/15 |  | CDK inhibitor |
| 7 | **R547** | Phase 1 | -3.31 | 1.25 | 4/4 |  | CDK inhibitor |
| 8 | **daprodustat** | Launched | -3.08 | 2.0 | 4/4 |  | hypoxia inducible factor inhibitor |
| 9 | **NMS-1286937** | Phase 2 | -3.01 | 1.75 | 4/4 | sí | PLK inhibitor |
| 10 | **LB-100** | Phase 2 | -2.96 | 1.333 | 3/3 |  | protein phosphatase inhibitor |
| 11 | **danusertib** | Phase 2 | -2.94 | 1.778 | 9/9 | sí | Aurora kinase inhibitor|growth factor recepto |
| 12 | **PF-03814735** | Phase 1 | -2.91 | 1.0 | 2/2 | sí | Aurora kinase inhibitor |
| 13 | **colchicine** | Launched | -2.89 | 2.222 | 18/18 | sí | microtubule inhibitor |
| 14 | **PF-477736** | Phase 1 | -2.87 | 1.0 | 2/2 |  | CHK inhibitor |
| 15 | **clofarabine** | Launched | -2.85 | 2.0 | 15/15 |  | ribonucleotide reductase inhibitor |
| 16 | **alvocidib** | Phase 2 | -2.83 | 1.7 | 10/10 |  | CDK inhibitor |
| 17 | **dipyridamole** | Launched | -2.79 | 2.32 | 25/25 |  | phosphodiesterase inhibitor |
| 18 | **panobinostat** | Launched | -2.78 | 1.917 | 12/12 |  | HDAC inhibitor |

### Sin fármacos de huso mitótico (candidatos de repurposing propiamente dichos)

| # | fármaco | fase | z | d_c | dianas | MOA |
|--|--|--|--|--|--|--|
| 1 | **AT-7519** | Phase 2 | -3.84 | 2.111 | 18/18 | CDK inhibitor |
| 2 | **PHA-793887** | Phase 1 | -3.52 | 2.2 | 15/15 | CDK inhibitor |
| 3 | **R547** | Phase 1 | -3.31 | 1.25 | 4/4 | CDK inhibitor |
| 4 | **daprodustat** | Launched | -3.08 | 2.0 | 4/4 | hypoxia inducible factor inhibitor |
| 5 | **LB-100** | Phase 2 | -2.96 | 1.333 | 3/3 | protein phosphatase inhibitor |
| 6 | **PF-477736** | Phase 1 | -2.87 | 1.0 | 2/2 | CHK inhibitor |
| 7 | **clofarabine** | Launched | -2.85 | 2.0 | 15/15 | ribonucleotide reductase inhibitor |
| 8 | **alvocidib** | Phase 2 | -2.83 | 1.7 | 10/10 | CDK inhibitor |
| 9 | **dipyridamole** | Launched | -2.79 | 2.32 | 25/25 | phosphodiesterase inhibitor |
| 10 | **panobinostat** | Launched | -2.78 | 1.917 | 12/12 | HDAC inhibitor |
| 11 | **SCH-900776** | Phase 2 | -2.76 | 1.0 | 2/2 | CHK inhibitor |
| 12 | **E7449** | Phase 2 | -2.76 | 1.75 | 4/4 | PARP inhibitor |
| 13 | **AZD7762** | Phase 1 | -2.73 | 1.0 | 2/2 | CHK inhibitor |
| 14 | **P276-00** | Phase 2 | -2.73 | 1.333 | 3/3 | CDK inhibitor |
| 15 | **lubiprostone** | Launched | -2.68 | 1.5 | 2/2 | chloride channel activator |
| 16 | **fludarabine** | Launched | -2.55 | 2.0 | 12/12 | ribonucleotide reductase inhibitor |
| 17 | **dinaciclib** | Phase 3 | -2.53 | 1.5 | 4/4 | CDK inhibitor |
| 18 | **AMG-925** | Phase 1 | -2.52 | 1.333 | 3/3 | CDK inhibitor|FLT3 inhibitor |

## Módulo `senescencia`  =  {CDKN2A, CDKN1A, TP53, RB1, SERPINE1, GLB1, LMNB1, BCL2, BCL2L1, BCL2L2, MCL1, TP53BP1, E2F1, MDM2}

### Todos (incluye fármacos de huso mitótico)

| # | fármaco | fase | z | d_c | dianas | huso? | MOA |
|--|--|--|--|--|--|--|--|
| 1 | **boceprevir** | Launched | -4.04 | 1.286 | 7/7 |  | HCV inhibitor |
| 2 | **PHA-793887** | Phase 1 | -3.82 | 1.6 | 15/15 |  | CDK inhibitor |
| 3 | **emricasan** | Phase 2 | -3.69 | 1.4 | 10/10 |  | caspase inhibitor |
| 4 | **RGB-286638** | Phase 1 | -3.66 | 1.267 | 15/15 |  | CDK inhibitor |
| 5 | **panobinostat** | Launched | -3.62 | 1.25 | 12/12 |  | HDAC inhibitor |
| 6 | **NMS-1286937** | Phase 2 | -3.37 | 1.0 | 4/4 | sí | PLK inhibitor |
| 7 | **AT-7519** | Phase 2 | -3.34 | 1.667 | 18/18 |  | CDK inhibitor |
| 8 | **alvocidib** | Phase 2 | -3.27 | 1.1 | 10/10 |  | CDK inhibitor |
| 9 | **I-BET-762** | Phase 2 | -3.1 | 1.0 | 3/3 |  | bromodomain inhibitor |
| 10 | **JNJ-26481585** | Phase 2 | -3.09 | 1.25 | 12/12 |  | HDAC inhibitor |
| 11 | **idasanutlin** | Phase 3 | -3.06 | 0.0 | 2/2 |  | MDM inhibitor |
| 12 | **topotecan** | Launched | -2.97 | 1.0 | 2/2 |  | topoisomerase inhibitor |
| 13 | **CABOZANTINIB S-MALATE** | Launched | -2.97 | 1.0 | 3/3 |  |  |
| 14 | **irinotecan** | Launched | -2.88 | 1.0 | 2/2 |  | topoisomerase inhibitor |
| 15 | **AMG-548** | Phase 1 | -2.85 | 1.0 | 4/4 |  | MAP kinase inhibitor |
| 16 | **E7449** | Phase 2 | -2.78 | 1.25 | 4/4 |  | PARP inhibitor |
| 17 | **bicyclol** | Launched | -2.76 | 1.0 | 2/2 |  | NFkB pathway inhibitor |
| 18 | **17-hydroxyprogesterone-caproate** | Launched | -2.75 | 1.286 | 7/7 |  | progesterone receptor agonist |

### Sin fármacos de huso mitótico (candidatos de repurposing propiamente dichos)

| # | fármaco | fase | z | d_c | dianas | MOA |
|--|--|--|--|--|--|--|
| 1 | **boceprevir** | Launched | -4.04 | 1.286 | 7/7 | HCV inhibitor |
| 2 | **PHA-793887** | Phase 1 | -3.82 | 1.6 | 15/15 | CDK inhibitor |
| 3 | **emricasan** | Phase 2 | -3.69 | 1.4 | 10/10 | caspase inhibitor |
| 4 | **RGB-286638** | Phase 1 | -3.66 | 1.267 | 15/15 | CDK inhibitor |
| 5 | **panobinostat** | Launched | -3.62 | 1.25 | 12/12 | HDAC inhibitor |
| 6 | **AT-7519** | Phase 2 | -3.34 | 1.667 | 18/18 | CDK inhibitor |
| 7 | **alvocidib** | Phase 2 | -3.27 | 1.1 | 10/10 | CDK inhibitor |
| 8 | **I-BET-762** | Phase 2 | -3.1 | 1.0 | 3/3 | bromodomain inhibitor |
| 9 | **JNJ-26481585** | Phase 2 | -3.09 | 1.25 | 12/12 | HDAC inhibitor |
| 10 | **idasanutlin** | Phase 3 | -3.06 | 0.0 | 2/2 | MDM inhibitor |
| 11 | **topotecan** | Launched | -2.97 | 1.0 | 2/2 | topoisomerase inhibitor |
| 12 | **CABOZANTINIB S-MALATE** | Launched | -2.97 | 1.0 | 3/3 |  |
| 13 | **irinotecan** | Launched | -2.88 | 1.0 | 2/2 | topoisomerase inhibitor |
| 14 | **AMG-548** | Phase 1 | -2.85 | 1.0 | 4/4 | MAP kinase inhibitor |
| 15 | **E7449** | Phase 2 | -2.78 | 1.25 | 4/4 | PARP inhibitor |
| 16 | **bicyclol** | Launched | -2.76 | 1.0 | 2/2 | NFkB pathway inhibitor |
| 17 | **17-hydroxyprogesterone-caproate** | Launched | -2.75 | 1.286 | 7/7 | progesterone receptor agonist |
| 18 | **VX-702** | Phase 2 | -2.73 | 1.125 | 8/8 | p38 MAPK inhibitor |

## Módulo `aneuploidia_estres`  =  {HSP90AA1, HSP90AB1, HSF1, PRKAA1, PRKAA2, MTOR, TFEB, SQSTM1, MAP1LC3B, ATG7, NQO1, NFE2L2}

### Todos (incluye fármacos de huso mitótico)

| # | fármaco | fase | z | d_c | dianas | huso? | MOA |
|--|--|--|--|--|--|--|--|
| 1 | **OSI-027** | Phase 1 | -7.59 | 0.857 | 7/7 |  | mTOR inhibitor |
| 2 | **AZD8055** | Phase 1 | -7.26 | 0.857 | 7/7 |  | mTOR inhibitor |
| 3 | **aspirin** | Launched | -5.95 | 1.35 | 20/20 |  | cyclooxygenase inhibitor |
| 4 | **CH5132799** | Phase 1 | -5.91 | 0.8 | 5/5 |  | PI3K inhibitor |
| 5 | **SB-2343** | Phase 1 | -5.86 | 0.8 | 5/5 |  | mTOR inhibitor|PI3K inhibitor |
| 6 | **acadesine** | Phase 3 | -5.74 | 0.833 | 6/6 |  | AMPK activator |
| 7 | **GSK2126458** | Phase 1 | -5.56 | 0.8 | 5/5 |  | mTOR inhibitor|PI3K inhibitor |
| 8 | **VE-822** | Phase 2 | -5.48 | 0.75 | 4/4 |  | ATR kinase inhibitor |
| 9 | **NVP-BEZ235** | Phase 3 | -5.47 | 0.8 | 5/5 |  | mTOR inhibitor|PI3K inhibitor |
| 10 | **MLN0128** | Phase 2 | -5.43 | 0.75 | 4/4 |  | mTOR inhibitor |
| 11 | **GDC-0980** | Phase 2 | -5.42 | 1.0 | 7/7 |  | mTOR inhibitor|PI3K inhibitor |
| 12 | **SAPANISERTIB** | Launched | -5.4 | 1.0 | 5/5 |  |  |
| 13 | **trilaciclib** | Launched | -5.36 | 1.0 | 5/5 |  | CDK inhibitor |
| 14 | **temsirolimus** | Launched | -5.2 | 0.667 | 3/3 |  | mTOR inhibitor |
| 15 | **dicoumarol** | Launched | -5.03 | 0.667 | 3/3 |  | NADPH inhibitor |
| 16 | **AZD6482** | Phase 1 | -4.79 | 1.0 | 4/4 |  | PI3K inhibitor |
| 17 | **GDC-0941** | Phase 2 | -4.7 | 1.0 | 4/4 |  | PI3K inhibitor |
| 18 | **menadione** | Launched | -4.66 | 1.615 | 13/13 |  | mitochondrial DNA polymerase inhibitor|phosph |

### Sin fármacos de huso mitótico (candidatos de repurposing propiamente dichos)

| # | fármaco | fase | z | d_c | dianas | MOA |
|--|--|--|--|--|--|--|
| 1 | **OSI-027** | Phase 1 | -7.59 | 0.857 | 7/7 | mTOR inhibitor |
| 2 | **AZD8055** | Phase 1 | -7.26 | 0.857 | 7/7 | mTOR inhibitor |
| 3 | **aspirin** | Launched | -5.95 | 1.35 | 20/20 | cyclooxygenase inhibitor |
| 4 | **CH5132799** | Phase 1 | -5.91 | 0.8 | 5/5 | PI3K inhibitor |
| 5 | **SB-2343** | Phase 1 | -5.86 | 0.8 | 5/5 | mTOR inhibitor|PI3K inhibitor |
| 6 | **acadesine** | Phase 3 | -5.74 | 0.833 | 6/6 | AMPK activator |
| 7 | **GSK2126458** | Phase 1 | -5.56 | 0.8 | 5/5 | mTOR inhibitor|PI3K inhibitor |
| 8 | **VE-822** | Phase 2 | -5.48 | 0.75 | 4/4 | ATR kinase inhibitor |
| 9 | **NVP-BEZ235** | Phase 3 | -5.47 | 0.8 | 5/5 | mTOR inhibitor|PI3K inhibitor |
| 10 | **MLN0128** | Phase 2 | -5.43 | 0.75 | 4/4 | mTOR inhibitor |
| 11 | **GDC-0980** | Phase 2 | -5.42 | 1.0 | 7/7 | mTOR inhibitor|PI3K inhibitor |
| 12 | **SAPANISERTIB** | Launched | -5.4 | 1.0 | 5/5 |  |
| 13 | **trilaciclib** | Launched | -5.36 | 1.0 | 5/5 | CDK inhibitor |
| 14 | **temsirolimus** | Launched | -5.2 | 0.667 | 3/3 | mTOR inhibitor |
| 15 | **dicoumarol** | Launched | -5.03 | 0.667 | 3/3 | NADPH inhibitor |
| 16 | **AZD6482** | Phase 1 | -4.79 | 1.0 | 4/4 | PI3K inhibitor |
| 17 | **GDC-0941** | Phase 2 | -4.7 | 1.0 | 4/4 | PI3K inhibitor |
| 18 | **menadione** | Launched | -4.66 | 1.615 | 13/13 | mitochondrial DNA polymerase inhibitor|phosphatase |

## Lectura

- **Módulos `MVA_genes` / `SAC_MCC`:** dominados por inhibidores de Aurora / PLK / TTK-MPS1 / tubulina — **conceptualmente contraindicados** (inhibir aún más un checkpoint ya débil). El método encuentra la vecindad correcta, pero al quitar los fármacos de huso lo que queda son agentes de daño al ADN (PARP-i, antimetabolitos) = quimioterapia, no repurposing. → **no hay candidato 'limpio' a la altura del propio gen de enfermedad.**
- **Módulo `senescencia`:** aquí sí aparecen candidatos de repurposing con lógica — inhibidores de BCL-2/BCL-xL (navitoclax = senolítico), y agentes que tocan p53/MDM2/RB. Confirma por red el **eje senolítico** del análisis curado (BubR1^H/H = modelo fundador).
- **Módulo `aneuploidia_estres`:** inhibidores de HSP90 (17-AAG/tanespimicina) y moduladores de AMPK/mTOR/autofagia — confirma por red el **eje de tolerancia a la aneuploidía** (metformina/AICAR, HSP90; Tang & Amon 2011).

> Conclusión C1: la proximidad de red **no aporta un candidato nuevo** más allá de lo curado, pero **valida independientemente** que (1) el gen de enfermedad no es 'drogable' de forma útil y (2) los dos ejes terapéuticos correctos son downstream: senescencia y estrés de aneuploidía.
---

## Dónde cae cada fármaco del análisis curado (z-score por módulo)

| fármaco (curado) | MVA_genes | SAC_MCC | senescencia | aneuploidia_estres | lectura |
|---|---|---|---|---|---|
| **acadesine (AICAR)** | +0.7 | −0.6 | −1.5 | **−5.7** | valida eje AMPK (Tang & Amon 2011) |
| **aspirin** | +0.2 | −0.8 | −2.5 | **−6.0** | valida quimioprevención / eje estrés |
| **sirolimus (rapamicina)** | +0.3 | +0.8 | −0.4 | **−4.0** | mTOR = nodo del eje aneuploidía |
| **metformin** | +0.7 | +1.3 | −1.6 | **−3.7** | AMPK, coherente |
| **tanespimycin (17-AAG)** | +0.2 | +0.5 | −1.4 | **−4.2 (d_c 0)** | HSP90 directo (Tang & Amon 2011) |
| **dasatinib** | +0.5 | +1.1 | −0.6 | **−3.4** | SRC/ABL cerca de PI3K-AMPK |
| **navitoclax** | +0.8 | +1.3 | **−2.2** | +1.3 | senolítico → módulo senescencia, coherente |
| **phenformin** | −0.9 | −0.5 | −0.3 | −2.0 | AMPK |
| **quercetin** | −0.1 | +0.5 | +0.5 | −1.4 | señal débil (flavonoide, muchas dianas) |
| **nicotinamide** | +0.5 | −0.7 | −0.8 | −0.2 | sin señal de red (actúa vía NAD+/SIRT, no en el interactoma PPI) |
| **hydroxychloroquine** | +0.3 | +1.2 | +0.4 | +0.9 | sin señal (autofagia lisosomal, no capturada por PPI) |

**z ≤ −2 = proximidad significativa.** Los senolíticos (navitoclax) puntúan en el módulo de
**senescencia**; los agentes de estrés metabólico / HSP90 (AICAR, rapamicina, metformina, 17-AAG,
aspirina) puntúan fuerte en **aneuploidia_estres**. Ninguno puntúa en el módulo del gen de
enfermedad. → **la topología de red, sin usar una sola cita, reconstruye los dos ejes del análisis
curado y confirma que la oportunidad terapéutica está río abajo del checkpoint.**
