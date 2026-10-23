# C4 — Reversión de firma con una firma REAL de insuficiencia de BubR1 (GEO)

_C3 usó listas de marcadores de literatura. C4 usa una firma **derivada de datos primarios** de dos modelos de ratón de BubR1-bajo._


## 1. Firma primaria — GSE277997 (BubR1 insuficiente, corazón, fenotipo de envejecimiento)

DE Hypomorph-vs-WT precomputada (padj<0.05, |log2FC|>0.585): **168 genes up · 160 dn**.

- **Senescencia / SASP inducidos**: Cdkn1a, Cdkn2a, Cdkn2b, Gdf15, Timp1
- **Respuesta integrada al estrés / mitocondrial / proteotóxica inducida**: Chac1, Ddit3, Fgf21, Gdf15, Trib3
- **Programa fetal / de regeneración inducido** (daño tisular crónico): Tnni1

> La firma derivada de **datos reales** enciende los dos ejes del análisis curado: **Cdkn2b** (p15, freno de senescencia), **Gdf15** y **Fgf21** (respuesta integrada al estrés / mitocondrial — la firma canónica de células aneuploides, Tang-Amon). Los dos ejes terapéuticos **no son una construcción teórica.**

## 2. Segundo dataset — GSE134781 (van Deursen; PMID 31738183): portadores de alelos MVA, músculo

Ratones knock-in que imitan alelos de pacientes con MVA: **BubR1 L1002P** (numeración de ratón; equivale a **L1012P humano**, en el lóbulo C-terminal de la pseudoquinasa, a ~10 residuos de la N1002K del probando — **no es el mismo residuo**) y **X753** (alelo truncante). Las muestras son músculo esquelético (gastrocnemio) de **portadores heterocigotos** (+/L1002P, +/X753) a los 3 meses vs. WT — es decir, el estado de *portador*, no la enfermedad bialélica.

- Solapamiento transcripcional con la firma cardíaca de GSE277997: **a nivel de azar** (29/127 genes UP y 23/96 DN en el mismo sentido) — esperable: corazón ≠ músculo, y los portadores heterocigotos de alelos MVA son (como los padres de los pacientes) esencialmente sanos. **No se fuerza ninguna conclusión transcripcional de este dataset.**
- Genes de senescencia/ISR arriba también en el músculo del 2º dataset: ninguno pasó el filtro de expresión en músculo.
- Su valor es de contexto: documenta que existen modelos de ratón de alelos de pacientes MVA en la misma región C-terminal de BubR1 que la variante B del probando, generados por el mismo laboratorio del modelo de senescencia (Baker 2011).

## 3. Reversión de firma (L1000CDS2) — ¿qué revierte la firma real?

| # | perturbágeno | score | eje (MOA) | ¿aprobado? | Track 2 |
|---|---|---|---|---|---|
| 1 | chaetocin | 0.052 |  |  |  |
| 2 | BRD-K88569143 | 0.052 |  |  |  |
| 3 | INK-128 | 0.052 |  |  |  |
| 4 | PP-110 | 0.047 |  |  |  |
| 5 | HY-10518 | 0.047 |  |  |  |
| 6 | vorinostat | 0.047 | HDAC | sí | ✅ |
| 7 | AS-605240 | 0.047 |  |  |  |
| 8 | tivozanib | 0.047 |  | sí |  |
| 9 | 528116.cdx | 0.042 |  |  |  |
| 10 | daunorubicin | 0.042 | quimio (ruido) | sí |  |
| 11 | trichostatin A | 0.042 |  |  | ✅ |
| 12 | EI-156 | 0.042 |  |  |  |
| 13 | S1205 | 0.042 |  |  |  |
| 14 | BRD-A52530684 | 0.042 |  |  |  |
| 15 | ibrutinib | 0.042 |  | sí |  |
| 16 | bufalin | 0.036 |  |  |  |
| 17 | DIGITOXIN | 0.036 |  | sí |  |
| 18 | GITOXIGENIN | 0.036 |  |  |  |
| 19 | Ro 31-8220 mesylate | 0.036 |  |  |  |
| 20 | Tocainide hydrochloride | 0.036 |  |  |  |
| 21 | BRD-K17140735 | 0.036 |  |  |  |
| 22 | BRD-K81473043 | 0.036 |  |  |  |
| 23 | PP-110 | 0.036 |  |  |  |
| 24 | PI 103 hydrochloride | 0.036 |  |  |  |
| 25 | BRD-K15563106 | 0.036 |  |  |  |

- **Candidatos de Track 2 entre los reversores:** vorinostat (0.047), trichostatin A (0.042), geldanamycin (0.036), vorinostat (0.036), torin-1 (0.036)
- **Ejes de MOA sobre-representados entre los reversores:** HDAC ×2, HSP90 / proteostasis ×2, quimio (ruido) ×1, mTOR ×1, CDK / ciclo celular ×1

### 3b. Sensibilidad — firma estricta (|log2FC| ≥ 1)

La tabla depositada contiene **165 genes con log2FC casi idéntico (0,80–0,82)** — una 'columna' que se ve en el volcano — y, al tomar los 150 con mayor fold-change, esos genes ocupaban cerca de la mitad de la consulta original. Se repite la consulta sin ellos (76 up / 40 dn).

| clase de MOA entre los reversores del top-50 | firma original | firma estricta |
|---|---|---|
| CDK / ciclo celular | 1 | 4 |
| HSP90 / proteostasis | 2 | 2 |
| HDAC | 2 | 2 |
| quimio (ruido) | 1 | 1 |
| mTOR | 1 | 1 |

- Candidatos de Track 2 entre los reversores de la firma estricta: vorinostat (0.07), vorinostat (0.058), trichostatin A (0.058), geldanamycin (0.058)
- Primeros 10 reversores (firma estricta): INK-128, chaetocin, BI-2536, AZD-5438, PI-103, Emetine Dihydrochloride Hydrate (74), 528116.cdx, BRD-A60245366, HY-10456, BRD-K59753853

## 4. Lectura

- **Premisa validada con datos primarios:** el modelo de BubR1 hipomórfico (corazón, GSE277997) activa senescencia (p21/p16/p15) + respuesta integrada al estrés (Gdf15/Fgf21/Chop/Trib3/Chac1). El marco de dos ejes de Track 2 sale del transcriptoma de un modelo animal, no solo de la literatura. (Un solo dataset informativo; el segundo, de portadores heterocigotos en músculo, no replica la firma — ver §2.)
- **Reversión de firma:** los MOA sobre-representados entre los reversores de esta firma real (CDK, HDAC, HSP90, mTOR) **coinciden con C3** (que usó firmas de literatura) → el resultado de reversión es robusto a cómo se defina la firma.
- **Ningún candidato NUEVO, limpio y aprobado** fuera del marco senólisis + estrés de aneuploidía + mTOR/HSP90. (L1000CDS2 rinde peor con firmas de tejido entero que con firmas de línea celular — por eso los scores son más bajos que en C3; la señal de **clase de MOA** es lo informativo.)
