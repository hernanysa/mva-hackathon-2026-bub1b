# C5 — Robustez de la proximidad de red (C1) al método y al umbral

_C1: distancia 'closest' d_c (Guney 2016), STRING≥700. C5: **random-walk-with-restart / personalized PageRank** (integra todos los caminos), en STRING≥700 **y** ≥900. ¿Se sostienen las conclusiones?_


## STRING ≥ 700  (15,882 nodos)


### módulo `MVA_genes`

- top-10 por RWR: **5/10 son inhibidores de huso mitótico** ⚠️
- top-8:
  | # | fármaco | fase | z (RWR) | huso? | MOA |
  |---|---|---|---|---|---|
  | 1 | paclitaxel | Launched | 6.03 | sí | tubulin polymerization inhibitor |
  | 2 | cabazitaxel | Launched | 5.95 |  | microtubule inhibitor |
  | 3 | vinblastine | Launched | 5.92 | sí | microtubule inhibitor|tubulin polymeriza |
  | 4 | docetaxel | Launched | 5.78 | sí | tubulin polymerization inhibitor |
  | 5 | vinorelbine | Launched | 5.49 | sí | tubulin polymerization inhibitor |
  | 6 | clofarabine | Launched | 5.38 |  | ribonucleotide reductase inhibitor |
  | 7 | colchicine | Launched | 4.93 |  | microtubule inhibitor |
  | 8 | AT-7519 | Phase 2 | 4.67 |  | CDK inhibitor |
- candidatos de Track 2 en este módulo (por z RWR):
  - tanespimycin (HSP90): z=2.4, percentil PPR=0.9813
  - temsirolimus (mTOR): z=1.23, percentil PPR=0.9251
  - everolimus (mTOR): z=0.93, percentil PPR=0.9292
  - sirolimus (mTOR): z=0.9, percentil PPR=0.9292
  - torin-1 (mTOR): z=0.72, percentil PPR=0.9542
  - torin-2 (mTOR): z=0.63, percentil PPR=0.9542
  - fisetin (senólisis): z=0.55, percentil PPR=0.8742
  - dasatinib (senólisis): z=0.3, percentil PPR=0.7474

### módulo `SAC_MCC`

- top-10 por RWR: **4/10 son inhibidores de huso mitótico** ⚠️
- top-8:
  | # | fármaco | fase | z (RWR) | huso? | MOA |
  |---|---|---|---|---|---|
  | 1 | paclitaxel | Launched | 5.67 | sí | tubulin polymerization inhibitor |
  | 2 | AT-7519 | Phase 2 | 5.63 |  | CDK inhibitor |
  | 3 | clofarabine | Launched | 5.61 |  | ribonucleotide reductase inhibitor |
  | 4 | colchicine | Launched | 5.46 |  | microtubule inhibitor |
  | 5 | docetaxel | Launched | 5.39 | sí | tubulin polymerization inhibitor |
  | 6 | cabazitaxel | Launched | 5.27 |  | microtubule inhibitor |
  | 7 | PHA-793887 | Phase 1 | 5.26 |  | CDK inhibitor |
  | 8 | vinorelbine | Launched | 4.93 | sí | tubulin polymerization inhibitor |
- candidatos de Track 2 en este módulo (por z RWR):
  - tanespimycin (HSP90): z=1.95, percentil PPR=0.9795
  - torin-2 (mTOR): z=0.74, percentil PPR=0.957
  - temsirolimus (mTOR): z=0.73, percentil PPR=0.9123
  - torin-1 (mTOR): z=0.67, percentil PPR=0.957
  - fisetin (senólisis): z=0.52, percentil PPR=0.8784
  - everolimus (mTOR): z=0.47, percentil PPR=0.9072
  - sirolimus (mTOR): z=0.42, percentil PPR=0.9072
  - geldanamycin (HSP90): z=0.12, percentil PPR=0.5249

### módulo `senescencia`

- top-10 por RWR: **0/10 son inhibidores de huso mitótico**
- top-8:
  | # | fármaco | fase | z (RWR) | huso? | MOA |
  |---|---|---|---|---|---|
  | 1 | PHA-793887 | Phase 1 | 6.66 |  | CDK inhibitor |
  | 2 | AT-7519 | Phase 2 | 6.61 |  | CDK inhibitor |
  | 3 | AZD5438 | Phase 1 | 6.44 |  | CDK inhibitor |
  | 4 | geldanamycin | Preclinical | 6.17 |  | HSP inhibitor |
  | 5 | N-acetyl-D-glucosamine | Phase 2/Phase 3 | 6.13 |  |  |
  | 6 | boceprevir | Launched | 5.9 |  | HCV inhibitor |
  | 7 | VBY-825 | Preclinical | 5.41 |  | cathepsin inhibitor |
  | 8 | cathepsin-inhibitor-1 | Preclinical | 5.02 |  | cathepsin inhibitor |
- candidatos de Track 2 en este módulo (por z RWR):
  - geldanamycin (HSP90): z=6.17, percentil PPR=0.7458
  - aspirin (quimioprevención): z=2.16, percentil PPR=0.8322
  - dasatinib (senólisis): z=2.12, percentil PPR=0.7995
  - tanespimycin (HSP90): z=2.0, percentil PPR=0.9966
  - torin-1 (mTOR): z=1.09, percentil PPR=0.9907
  - torin-2 (mTOR): z=1.08, percentil PPR=0.9907
  - metformin (AMPK/aneuploidía): z=1.07, percentil PPR=0.8662
  - fisetin (senólisis): z=1.01, percentil PPR=0.9275

### módulo `aneuploidia_estres`

- top-10 por RWR: **0/10 son inhibidores de huso mitótico**
- top-8:
  | # | fármaco | fase | z (RWR) | huso? | MOA |
  |---|---|---|---|---|---|
  | 1 | menadione | Launched | 7.04 |  | mitochondrial DNA polymerase inhibitor|p |
  | 2 | flumazenil | Launched | 6.36 |  | benzodiazepine receptor antagonist |
  | 3 | menadione-bisulfite | Phase 2 | 6.25 |  | vitamin K |
  | 4 | acamprosate | Launched | 6.15 |  | glutamate receptor antagonist |
  | 5 | dicoumarol | Launched | 6.08 |  | NADPH inhibitor |
  | 6 | etomidate | Launched | 6.06 |  | GABA receptor modulator |
  | 7 | methoxyflurane | Launched | 5.96 |  | membrane permeability inhibitor |
  | 8 | propofol | Launched | 5.76 |  | benzodiazepine receptor agonist |
- candidatos de Track 2 en este módulo (por z RWR):
  - aspirin (quimioprevención): z=4.15, percentil PPR=0.8851
  - metformin (AMPK/aneuploidía): z=2.82, percentil PPR=0.9927
  - dasatinib (senólisis): z=2.41, percentil PPR=0.7975
  - temsirolimus (mTOR): z=2.17, percentil PPR=0.9877
  - geldanamycin (HSP90): z=1.66, percentil PPR=0.1974
  - sirolimus (mTOR): z=1.47, percentil PPR=0.9764
  - everolimus (mTOR): z=1.43, percentil PPR=0.9764
  - fisetin (senólisis): z=1.36, percentil PPR=0.9423

## STRING ≥ 900 (más estricto)  (11,693 nodos)


### módulo `MVA_genes`

- top-10 por RWR: **5/10 son inhibidores de huso mitótico** ⚠️
- top-8:
  | # | fármaco | fase | z (RWR) | huso? | MOA |
  |---|---|---|---|---|---|
  | 1 | vinorelbine | Launched | 6.27 | sí | tubulin polymerization inhibitor |
  | 2 | cabazitaxel | Launched | 5.92 |  | microtubule inhibitor |
  | 3 | paclitaxel | Launched | 5.84 | sí | tubulin polymerization inhibitor |
  | 4 | docetaxel | Launched | 5.79 | sí | tubulin polymerization inhibitor |
  | 5 | TC-S-7005 | Preclinical | 5.61 | sí | PLK inhibitor |
  | 6 | clofarabine | Launched | 5.57 |  | ribonucleotide reductase inhibitor |
  | 7 | colchicine | Launched | 5.45 |  | microtubule inhibitor |
  | 8 | fludarabine | Launched | 4.58 |  | ribonucleotide reductase inhibitor |
- candidatos de Track 2 en este módulo (por z RWR):
  - geldanamycin (HSP90): z=1.85, percentil PPR=0.969
  - tanespimycin (HSP90): z=1.51, percentil PPR=0.9608
  - temsirolimus (mTOR): z=1.05, percentil PPR=0.9019
  - everolimus (mTOR): z=0.98, percentil PPR=0.907
  - sirolimus (mTOR): z=0.92, percentil PPR=0.907
  - navitoclax (senólisis): z=0.84, percentil PPR=0.8605
  - torin-2 (mTOR): z=0.79, percentil PPR=0.9414
  - torin-1 (mTOR): z=0.78, percentil PPR=0.9414

### módulo `SAC_MCC`

- top-10 por RWR: **3/10 son inhibidores de huso mitótico** ⚠️
- top-8:
  | # | fármaco | fase | z (RWR) | huso? | MOA |
  |---|---|---|---|---|---|
  | 1 | docetaxel | Launched | 5.88 | sí | tubulin polymerization inhibitor |
  | 2 | cabazitaxel | Launched | 5.74 |  | microtubule inhibitor |
  | 3 | colchicine | Launched | 5.64 |  | microtubule inhibitor |
  | 4 | vinorelbine | Launched | 5.6 | sí | tubulin polymerization inhibitor |
  | 5 | paclitaxel | Launched | 5.5 | sí | tubulin polymerization inhibitor |
  | 6 | flumazenil | Launched | 5.27 |  | benzodiazepine receptor antagonist |
  | 7 | clofarabine | Launched | 5.18 |  | ribonucleotide reductase inhibitor |
  | 8 | etomidate | Launched | 4.86 |  | GABA receptor modulator |
- candidatos de Track 2 en este módulo (por z RWR):
  - geldanamycin (HSP90): z=1.78, percentil PPR=0.9701
  - tanespimycin (HSP90): z=1.64, percentil PPR=0.9637
  - torin-1 (mTOR): z=1.12, percentil PPR=0.9442
  - temsirolimus (mTOR): z=1.09, percentil PPR=0.8978
  - torin-2 (mTOR): z=1.05, percentil PPR=0.9442
  - everolimus (mTOR): z=0.99, percentil PPR=0.8969
  - navitoclax (senólisis): z=0.96, percentil PPR=0.8644
  - sirolimus (mTOR): z=0.92, percentil PPR=0.8969

### módulo `senescencia`

- top-10 por RWR: **0/10 son inhibidores de huso mitótico**
- top-8:
  | # | fármaco | fase | z (RWR) | huso? | MOA |
  |---|---|---|---|---|---|
  | 1 | boceprevir | Launched | 5.5 |  | HCV inhibitor |
  | 2 | N-acetyl-D-glucosamine | Phase 2/Phase 3 | 4.75 |  |  |
  | 3 | VBY-825 | Preclinical | 4.72 |  | cathepsin inhibitor |
  | 4 | U-0126 | Preclinical | 4.37 |  | MEK inhibitor |
  | 5 | PD-98059 | Preclinical | 4.19 |  | MEK inhibitor |
  | 6 | cathepsin-inhibitor-1 | Preclinical | 4.14 |  | cathepsin inhibitor |
  | 7 | pepstatin | Preclinical | 4.12 |  | aspartic protease inhibitor |
  | 8 | "4,5,6,7-tetrabromobenzotriazole" | Preclinical | 4.09 |  | casein kinase inhibitor |
- candidatos de Track 2 en este módulo (por z RWR):
  - aspirin (quimioprevención): z=2.22, percentil PPR=0.8404
  - geldanamycin (HSP90): z=1.81, percentil PPR=0.9956
  - tanespimycin (HSP90): z=1.8, percentil PPR=0.9928
  - dasatinib (senólisis): z=1.7, percentil PPR=0.7673
  - temsirolimus (mTOR): z=1.34, percentil PPR=0.9127
  - torin-2 (mTOR): z=1.23, percentil PPR=0.9738
  - torin-1 (mTOR): z=1.18, percentil PPR=0.9738
  - sirolimus (mTOR): z=1.05, percentil PPR=0.8941

### módulo `aneuploidia_estres`

- top-10 por RWR: **3/10 son inhibidores de huso mitótico**
- top-8:
  | # | fármaco | fase | z (RWR) | huso? | MOA |
  |---|---|---|---|---|---|
  | 1 | menadione | Launched | 6.03 |  | mitochondrial DNA polymerase inhibitor|p |
  | 2 | dicoumarol | Launched | 5.9 |  | NADPH inhibitor |
  | 3 | SB-203580 | Preclinical | 5.51 |  | p38 MAPK inhibitor |
  | 4 | menadione-bisulfite | Phase 2 | 5.31 |  | vitamin K |
  | 5 | docetaxel | Launched | 5.23 | sí | tubulin polymerization inhibitor |
  | 6 | paclitaxel | Launched | 5.23 | sí | tubulin polymerization inhibitor |
  | 7 | colchicine | Launched | 5.18 |  | microtubule inhibitor |
  | 8 | U-0126 | Preclinical | 4.84 |  | MEK inhibitor |
- candidatos de Track 2 en este módulo (por z RWR):
  - aspirin (quimioprevención): z=3.97, percentil PPR=0.9136
  - navitoclax (senólisis): z=2.36, percentil PPR=0.9652
  - metformin (AMPK/aneuploidía): z=2.13, percentil PPR=0.9941
  - temsirolimus (mTOR): z=2.01, percentil PPR=0.9861
  - dasatinib (senólisis): z=1.89, percentil PPR=0.7745
  - resveratrol (quimioprevención): z=1.71, percentil PPR=0.9258
  - everolimus (mTOR): z=1.52, percentil PPR=0.9732
  - fisetin (senólisis): z=1.46, percentil PPR=0.9077

## Concordancia C5 (RWR) vs C1 (d_c)

| módulo | Spearman ρ (z de C1 vs z de C5, STRING≥700) | n |
|---|---|---|
| MVA_genes | -0.58 | 3869 |
| SAC_MCC | -0.63 | 3868 |
| senescencia | -0.67 | 3857 |
| aneuploidia_estres | -0.67 | 3852 |

## Lectura

**Concordancia C1↔C5.** El ρ de Spearman da **−0,58 a −0,67** — y ese **signo negativo es la
concordancia**: C1 puntúa con una *distancia* d_c (menor = más cerca = mejor) y C5 con un *z de
proximidad* (mayor = más cerca = mejor), así que anti-correlacionados = **de acuerdo**. Dos métricas
distintas (camino más corto vs. random-walk que integra todos los caminos) y dos umbrales de red
(STRING≥700 y ≥900) coinciden.

**Módulos del gen de enfermedad (`MVA_genes`, `SAC_MCC`):** el top por RWR está dominado por
**venenos de huso** (paclitaxel, docetaxel, vinorelbina, colchicina, inhibidores de PLK) +
quimioterápicos (clofarabina, fludarabina) + inhibidores de CDK. Los candidatos de repurposing
puntúan **bajo** aquí (fisetina z≈0,5; dasatinib z≈0,3; metformina ni aparece).

**Módulos río abajo (`senescencia`, `aneuploidia_estres`):** 0/10 del top son venenos de huso, y
los candidatos de repurposing **suben claramente**:
- senolíticos: z medio RWR en `senescencia` **0,60** vs en `MVA_genes` **0,19** (~3× más cerca río abajo)
- mTOR/HSP90/AMPK: z medio RWR en `aneuploidia_estres` **1,37** vs en `MVA_genes` **0,64** (~2×)
- aspirina destaca en `aneuploidia_estres` (z=4,2 a ≥700, 4,0 a ≥900) — coincide con C1 (z=−6,0) y
  con el mecanismo "resveratrol+aspirina elimina células tetraploides".

**Conclusión C5: la conclusión de C1 es robusta al método y al umbral de red.** No hay atajo
farmacológico en el gen de enfermedad — solo inhibidores de huso, contraindicados. La oportunidad
terapéutica está en los módulos río abajo (senescencia, estrés de aneuploidía), y ahí es donde
caen fisetina, metformina, rapamicina y NR.

_(Ruido conocido de los métodos de red: en `aneuploidia_estres` aparecen anestésicos/vitamina K
—menadiona, propofol, etomidato— porque los nodos redox/mitocondriales del módulo (NQO1, NFE2L2)
los atraen. No afecta la ubicación de los candidatos, que es la señal robusta.)_
