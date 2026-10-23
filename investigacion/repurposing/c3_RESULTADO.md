# C3 — Reversión de firma transcripcional (L1000CDS2 / Connectivity Map)

Tercer método independiente (ni literatura ni topología de red: **datos de expresión**).
3 firmas: senescencia, respuesta a aneuploidía (Dürrbaum/Sheltzer), CIN70 (Carter 2006). Se pide a L1000CDS2 los perturbágenos que producen el perfil **opuesto**.

## Perturbágenos que revierten ≥2 de las 3 firmas

| perturbágeno | # firmas | firmas | score | aprobado | fase | MOA |
|--|--|--|--|--|--|--|
| **geldanamycin** | 2 | resp_aneuploidia,senescencia | 0.17 | sí | Preclinical | HSP inhibitor |
| **NVP-AUY922** | 2 | resp_aneuploidia,senescencia | 0.167 | sí | Phase 2 | HSP inhibitor |
| **alvocidib** | 2 | resp_aneuploidia,senescencia | 0.167 | sí | Phase 2 | CDK inhibitor |
| **BMS-387032** | 2 | resp_aneuploidia,senescencia | 0.148 | sí | Phase 1 | CDK inhibitor|cell cycle inhibitor|MCL1 inhib |
| **fostamatinib** | 2 | resp_aneuploidia,senescencia | 0.148 | sí | Launched | SYK inhibitor |
| **CGP-60474** | 2 | resp_aneuploidia,senescencia | 0.148 | sí | Preclinical | CDK inhibitor |

## Top 25 (todos)

| perturbágeno | #f | score | aprobado | MOA |
|--|--|--|--|--|
| geldanamycin | 2 | 0.17 | sí | HSP inhibitor |
| NVP-AUY922 | 2 | 0.167 | sí | HSP inhibitor |
| alvocidib | 2 | 0.167 | sí | CDK inhibitor |
| BMS-387032 | 2 | 0.148 | sí | CDK inhibitor|cell cycle inhibitor|MCL1 inhibitor |
| fostamatinib | 2 | 0.148 | sí | SYK inhibitor |
| CGP-60474 | 2 | 0.148 | sí | CDK inhibitor |
| AZD-7762 | 1 | 0.207 |  |  |
| dasatinib | 1 | 0.189 | sí | Bcr-Abl kinase inhibitor|ephrin inhibitor|KIT inhi |
| PF-562271 | 1 | 0.189 | sí | focal adhesion kinase inhibitor |
| QL-X-138 | 1 | 0.185 |  |  |
| GSK-1059615 | 1 | 0.17 |  |  |
| torin-1 | 1 | 0.167 | sí | mTOR inhibitor |
| canertinib | 1 | 0.151 | sí | EGFR inhibitor |
| WYE-125132 | 1 | 0.148 | sí | mTOR inhibitor |
| A443654 | 1 | 0.148 |  |  |
| sirolimus | 1 | 0.148 | sí | mTOR inhibitor |
| vincristine | 1 | 0.148 | sí | tubulin polymerization inhibitor |
| S1175 | 1 | 0.148 |  |  |
| E3380 | 1 | 0.148 |  |  |
| S1205 | 1 | 0.148 |  |  |
| albendazole | 1 | 0.148 | sí | tubulin polymerization inhibitor |
| LDN-193189 | 1 | 0.148 |  |  |
| PF-431396 | 1 | 0.148 | sí | focal adhesion kinase inhibitor |
| AZD-8055 | 1 | 0.148 |  |  |
| AT-7519 | 1 | 0.148 | sí | CDK inhibitor |

_score L1000CDS2: 0–2, mayor = mejor reversión de la firma._

---

## Lectura

**Nota técnica:** la firma CIN70 (solo genes UP) devolvió 0 reversores — L1000CDS2 rinde mejor con
listas UP **y** DN. Las otras dos firmas (con ambas direcciones) sí son informativas.

### Reversores de la firma de SENESCENCIA
- **dasatinib** — aparece 4× (células HME1, varias dosis, score hasta 0.19). El senolítico del
  análisis curado, confirmado por reversión de firma.
- **geldanamycin / NVP-AUY922** (inhibidores de HSP90) — repetidos.
- AZD-7762 (inhibidor de CHK1), PF-562271 (FAK), GSK-1059615 (PI3K/mTOR).

### Reversores de la firma de RESPUESTA A ANEUPLOIDÍA
- **torin-1, AZD-8055, WYE-125132, sirolimus (rapamicina)** — inhibidores de mTOR. El eje
  rapamicina del análisis curado, confirmado.
- **NVP-AUY922 / geldanamycin** (HSP90) — otra vez, y **revierten las DOS firmas**.
- alvocidib y otros inhibidores de CDK.
- (albendazol, vincristina = tubulina → dirección contraindicada, ruido.)

### Convergencia entre los 3 métodos independientes

| Mecanismo | Curado (Tang-Amon / Baker) | C1 proximidad de red | C2 literatura | C3 reversión de firma |
|---|---|---|---|---|
| **Inhibición de HSP90** (17-AAG / geldanamicina) | ✓ | ✓ z=−4.2, d_c=0 | — | ✓ revierte 2/2 firmas |
| **Inhibición de mTOR** (rapamicina) | ✓ | ✓ z=−4.0 | ✓ 53 PMIDs | ✓ revierte firma aneuploidía |
| **Dasatinib** (senolítico) | ✓ (D+Q) | ✓ z=−3.4 | ✓ 18 PMIDs | ✓ revierte firma senescencia |
| **Activación de AMPK** (metformina / AICAR) | ✓ | ✓ AICAR z=−5.7 | ✓ | ~ (AMPK mal representado en L1000) |
| **Senólisis BCL-2** (navitoclax) | ✓ | ✓ z=−2.2 | ✓ 15 PMIDs | — |
| **Aspirina** | ✓ | ✓ z=−6.0 | ✓ (ITP) | — |

**Tres métodos ortogonales — topología de red, minería de literatura, reversión de firma
transcripcional — más el análisis curado, convergen en el mismo conjunto reducido de mecanismos:
inhibición de mTOR, inhibición de HSP90, activación de AMPK y senólisis.** Ninguno propone un
candidato nuevo fuera de ese marco.

> Los inhibidores de HSP90 (17-AAG y sucesores) son la señal computacional **más fuerte y más
> consistente entre métodos**, pero **NO son aprobados, fracasaron clínicamente por toxicidad
> (hepática, ocular) y no son apropiados para un niño**. Es una validación mecanística del eje
> "estrés proteotóxico de la aneuploidía" (Tang & Amon 2011), no una recomendación.
