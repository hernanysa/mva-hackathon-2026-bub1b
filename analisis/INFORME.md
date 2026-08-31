# Diagnóstico molecular — Probando WGS_EX2312012
### Rare Disease, Real Kid: MVA Hackathon 2026

---

## Resultado

**Síndrome de Aneuploidía Variegada en Mosaico tipo 1 (MVA1; MIM 257300)** por variantes
**bialélicas en `BUB1B`** (mitotic checkpoint serine/threonine kinase B), transcripto
canónico `NM_001211.6` / `ENST00000287598.11`.

| | Variante (GRCh38) | HGVS | Consecuencia | Cigosidad | Frecuencia | Clasificación |
|---|---|---|---|---|---|---|
| **Alelo A** | 15:40209701 T>G (rs759242053) | `c.2210T>G` **p.(Leu737Ter)** | nonsense, exón 17/23 | het (AD 21,25; DP 46; GQ 99) | gnomAD 7.9e-5 (0 en la mayoría de poblaciones) | **Patogénica** — ClinVar VCV000533901; descrita en MVA (PMID 15475955, 21190457, 29641532) |
| **Alelo B** | 15:40220612 T>G | `c.3006T>G` **p.(Asn1002Lys)** | missense, exón 23/23 (dominio quinasa) | het (AD 15,13; DP 28; GQ 99) | **ausente de gnomAD** (0) | **Probablemente patogénica** — SIFT deletéreo (0.01), PolyPhen probably_damaging (0.997), AlphaMissense likely_pathogenic (0.923) |

Genotipo asumido: **heterocigota compuesta** (A en *trans* con B). El fenotipo del probando
—rabdomiosarcoma, restricción severa del crecimiento pre/postnatal, nefrocalcinosis,
atrofia muscular, historia de abortos recurrentes parentales— es el cuadro característico de
MVA1, con predisposición a rabdomiosarcoma y tumor de Wilms.

---

## Métodos

- **Insumo:** `WGS_EX2312012_HGWCNDSX7.vcf.gz` (VCF germinal GATK 4.2.4.0, GRCh38, muestra
  única, sin trío). Las 8 FASTQ (~85 GB, ~30×) se descargaron pero **no se alinearon**: la
  máquina de trabajo (2 núcleos, 11 GB RAM) no puede indexar GRCh38 con `bwa-mem2` (~40 GB RAM)
  ni alinear en tiempo razonable. El VCF trae `AD` y `DP` por sitio → suficiente para dosis y BAF.
- **Cariotipo molecular (`01_cnv_baf.py`):** DP en bins de 1 Mb normalizado al baseline
  autosómico (enmascarando pericentrómero); BAF = AD_alt/(AD_ref+AD_alt) de SNP heterocigotas
  bialélicas PASS con MQ≥59, DP≥20.
- **Panel dirigido (`02_genes_candidatos.py`):** 20 genes (MVA: BUB1B, CEP57, TRIP13, CENATAC;
  inestabilidad/rotura cromosómica: NBN, MRE11, RAD50, BLM, FANCA/C/G, BRCA2, PALB2, RECQL4;
  predisposición con solapamiento fenotípico: TP53, DICER1, SMARCB1, SMARCA4; enanismo
  primordial: PCNT, ATR). Coordenadas de Ensembl REST; anotación de las 1187 variantes PASS
  no-referencia con Ensembl VEP REST (consecuencia, gnomAD, ClinVar, SIFT/PolyPhen/AlphaMissense).
- **Workup de BUB1B (`03_bub1b_workup.py`):** ROH genome-wide, revisión de variantes raras del locus.

---

## Hallazgos de soporte

**1. QC de la muestra.** 5.012.204 variantes (94,6 % PASS). **Sexo genético masculino (XY)**:
chrX a 0,49× de la dosis autosómica con ~3.500 SNP het (vs ~65.000 en un autosoma equivalente),
chrY presente.

**2. Sin aneuploidía de cromosoma entero detectable (`out/cnv_baf/genome_wide.png`).**
Cobertura relativa 0,98–1,02 en los 22 autosomas; desviación mediana de BAF idéntica en todos
(|BAF−0,5| ≈ 0,053, p90 ≈ 0,133 — el ruido binomial esperado a 40×). Ningún cromosoma muestra
banda de BAF partida ni deriva de dosis.
→ **El WGS de esta muestra NO muestra aneuploidía variegada en mosaico** a resolución de WGS.
Esto **no descarta MVA1**: el grado de aneuploidía en BUB1B-MVA es muy variable, el fenotipo
celular más penetrante es la separación prematura de cromátides (PCS), invisible al WGS, y la
fracción de células aneuploides depende del tejido (sangre suele mostrarla menos que fibroblastos).
Confirmar requiere cariotipo / ensayo de PCS en células cultivadas.

**3. Sin consanguinidad.** Fracción het genome-wide 0,63; un único tramo ROH de ~3 Mb (chr8).
→ el modelo esperado es heterocigota compuesta, no homocigosis por descendencia.

**4. El panel señala solo BUB1B.** De 35 variantes codificantes/splice en el panel, únicamente
BUB1B reúne (a) ≥2 variantes cualificantes, (b) al menos una LoF de novo/rara, (c) variantes
que pasan el filtro de frecuencia. Los demás hits (PCNT ×15, RECQL4 ×4, BRCA2 ×3, TP53 P72R,
TP53 indel AF 0,71, NBN splice AF 0,41) son polimorfismos comunes. Una 3ª variante rara en
BUB1B (15:40216470, `c.2679-1026A>G`) es intrónica profunda → sin relevancia.

---

## Clasificación ACMG (resumen)

- **p.(Leu737Ter):** PVS1 (nonsense; LoF es el mecanismo de enfermedad en BUB1B) + PP5/PS
  (patogénica en ClinVar, literatura MVA) + PM2_supporting (rara) → **Patogénica**.
- **p.(Asn1002Lys):** PM2 (ausente de gnomAD) + PP3_moderate (SIFT+PolyPhen+AlphaMissense
  concordantes, dominio quinasa) + PP4 (fenotipo altamente específico) + PM3 (*in trans* con
  variante patogénica — **asumido**, no probado) → **Probablemente patogénica**
  (Patogénica si se confirma la fase).

---

## Validación Fase 2 — alineamiento dirigido de BUB1B (extracción por k-mers desde las FASTQ)

Se extrajeron de las 8 FASTQ las lecturas de BUB1B (bbduk, 31-mers exactos de la secuencia
no-repetitiva del gen ±10kb; ~10.500 pares) y se alinearon a chr15 → `align/bub1b.bam`,
cobertura media **33.8×** sobre el cuerpo del gen.

1. **Sin deleción de exón.** Los 23 exones a 0.72–1.44× de la mediana del gen, todos 100%
   cubiertos, ninguno cae a ~0.5×. → el 2º alelo **no es una CNV**
   (`align/cobertura_exones_bub1b.png`).
2. **Las dos variantes, confirmadas desde lecturas crudas** (independiente del llamador GATK):
   - p.(Leu737Ter): profundidad 52, T 25 / **G 27**, VAF **0.52**, hebras balanceadas, MAPQ 60, BASEQ 37.
   - p.(Asn1002Lys): profundidad 32, T 16 / **G 16**, VAF **0.50**, ambas hebras, MAPQ 60, BASEQ 37.
3. **Sin variante estructural / translocación** que afecte BUB1B: 0 lecturas con mate en otro
   cromosoma; los soft-clips se concentran en el 3'UTR AT-rich (baja complejidad, el VCF tampoco
   llamó nada ahí) → artefacto de alineamiento, no un breakpoint real.

→ **p.(Asn1002Lys) queda confirmado como 2º alelo** (no hay CNV ni SV alternativos).

## Limitaciones y confirmación recomendada

1. **Fase no probada.** Sin ADN parental ni lecturas largas no se puede demostrar que A y B
   están en *trans* (están a 10,9 kb; ninguna lectura corta las cruza). → **Test parental
   dirigido** (Sanger de ambas posiciones en padre y madre): confirma *trans* y clasifica PM3.
2. **Aneuploidía en mosaico no observada.** → cariotipo de linfocitos/fibroblastos cultivados
   + ensayo de PCS para el diagnóstico celular de MVA.
3. Muestra probablemente de sangre; la mosaico puede ser tejido-dependiente.

---

## Archivos

```
analisis/
  INFORME.md                      este documento
  PLAN.md                         plan y decisiones
  01_cnv_baf.py  02_genes_candidatos.py  03_bub1b_workup.py
  out/cnv_baf/genome_wide.png     BAF + dosis genome-wide (euploide)
  out/cnv_baf/resumen.txt         tabla por cromosoma
  out/genes/shortlist.tsv         variantes priorizadas del panel
  out/genes/genes_coords.json     coordenadas usadas
```
