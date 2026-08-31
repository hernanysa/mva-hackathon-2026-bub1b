# Track 1 — Variant Identification Report
### Rare Disease, Real Kid: MVA Hackathon 2026 · Proband `PROBAND01`

---

## 1. Answer

**Molecular diagnosis: Mosaic Variegated Aneuploidy syndrome, type 1 (MVA1; MIM 257300), caused by biallelic (compound-heterozygous) loss-of-function of `BUB1B`.**

Transcript: `NM_001211.6` / `ENST00000287598.11` (MANE Select), GRCh38.

| | Variant (GRCh38, 1-based) | cDNA / protein | Consequence | Zygosity | Population frequency | Classification |
|---|---|---|---|---|---|---|
| **Allele A** | `chr15:40209701 T>G` (rs759242053) | `c.2210T>G` **p.(Leu737Ter)** | stop-gained, exon 17/23 | heterozygous | gnomAD v4 ≈ 7.9×10⁻⁵ (exomes), 0 in most populations | **Pathogenic** (ClinVar VCV000533901; multiple submitters) |
| **Allele B** | `chr15:40220612 T>G` | `c.3006T>G` **p.(Asn1002Lys)** | missense, exon 23/23 (kinase domain) | heterozygous | **absent from gnomAD v4** | **Likely pathogenic** |

**EPCR (estimated probability of causal relationship): 0.92.**

The phenotype supplied for the proband — rhabdomyosarcoma (HP:0002859), severe pre- and post-natal
growth restriction (born ~1 kg at 32 weeks, HP:0001518/HP:0001622), nephrocalcinosis since birth
(HP:0000121), failure to thrive with skeletal-muscle atrophy (HP:0001508/HP:0003202), and a
parental history of recurrent pregnancy loss (HP:0200067) — is the characteristic constellation of
MVA1, which confers a high risk of embryonal rhabdomyosarcoma and Wilms tumour.

---

## 2. Data and computational environment

**Input.** `WGS_EX2312012_HGWCNDSX7.vcf.gz` — a single-sample germline VCF produced with GATK
4.2.4.0 (HaplotypeCaller → VariantFiltration) on DNAnexus, aligned to GRCh38, Ensembl-style contig
names (`1`–`22`, `X`, `Y`). 5,012,204 variant records, 94.6 % PASS. The eight raw FASTQ files
(4 lanes × R1/R2, ~85 GB, ~30× WGS) were also downloaded and used for the targeted re-alignment in
§3.5.

**Environment constraint (drove the strategy).** Analysis ran on a 2-core / 4-thread Intel
i7-6500U (2015) laptop with 11 GB RAM and a 5400-rpm mechanical disk. Whole-genome re-alignment of
the FASTQ is infeasible on this hardware: `bwa-mem2` requires ~40 GB RAM to build the GRCh38 index,
and `minimap2 -ax sr` streaming ~536 M read pairs benchmarked at >10 h with the coordinate-sort
step making the machine unusable. The pipeline was therefore built **VCF-first**, using the
per-site `AD` and `DP` fields (sufficient for allele-balance and dosage analysis), with a
**k-mer-targeted local re-alignment of the BUB1B locus only** for orthogonal validation.

All software ran in project-local isolated environments (Python venv + a micromamba
bioinformatics environment); no data left the machine.

---

## 3. Methods and results

### 3.1 Sample QC and sex

The VCF is high quality (94.6 % PASS). Relative read depth is **flat across all 22 autosomes**
(per-chromosome robust-median DP ratio 0.98–1.02; autosomal baseline ≈ 43×). Chromosome X carries
~0.49× the autosomal depth and only ~3.5–4.6 k heterozygous SNPs versus ~65 k on a size-matched
autosome, and chromosome Y is present → **the proband is male (46,XY constitutional baseline).**

### 3.2 Genome-wide screen for aneuploidy (`01_cnv_baf.py`)

For every high-confidence biallelic heterozygous SNP (PASS, `MQ` ≥ 59, total AD ≥ 20,
pericentromeric regions masked) we computed B-allele frequency, `BAF = AD_alt / (AD_ref + AD_alt)`,
and binned read depth in 1-Mb windows.

- **Depth:** no autosome deviates from 1.0× (range 0.98–1.02).
- **BAF:** the median |BAF − 0.5| is 0.053 and the 90th percentile 0.133 — **identical on all 22
  autosomes** and exactly the binomial spread expected for true heterozygous sites at ~40× depth.
  No chromosome shows a split BAF band or drift.

→ **The WGS shows no detectable whole-chromosome or large mosaic aneuploidy** at the resolution of
SNP allele-balance and read depth (see §4 for why this does not exclude MVA1).

A first-pass crude metric transiently flagged chromosomes 21/22; on inspection this was an
artefact of read pile-ups over the acrocentric short arms, resolved by pericentromeric masking and
a robust (rather than mean) per-chromosome estimator. We report this to be transparent about the
analysis process.

Runs of homozygosity: the genome-wide heterozygous fraction is 0.63 with a single ~3-Mb ROH on
chromosome 8 → **no consanguinity**, so the expected recessive model is compound heterozygosity,
not homozygosity-by-descent.

### 3.3 Targeted gene-panel annotation (`02_genes_candidatos.py`)

A 20-gene panel was assembled *a priori* from the phenotype: MVA genes (`BUB1B`, `CEP57`,
`TRIP13`, `CENATAC`); chromosome-instability / breakage syndromes (`NBN`, `MRE11`, `RAD50`, `BLM`,
`FANCA/C/G`, `BRCA2`, `PALB2`, `RECQL4`); cancer-predisposition differentials with phenotype
overlap (`TP53`, `DICER1`, `SMARCB1`, `SMARCA4`); and primordial-dwarfism genes (`PCNT`, `ATR`).
Gene coordinates were retrieved from Ensembl REST. All **1,187 PASS non-reference variants** in the
panel were annotated with Ensembl VEP REST (consequence, gnomAD frequency, ClinVar, SIFT, PolyPhen,
AlphaMissense).

Of 35 coding/splice variants in the panel, **only `BUB1B`** satisfied all of: (i) ≥ 2 qualifying
variants, (ii) at least one *bona fide* loss-of-function allele, and (iii) variants surviving a
rare-frequency filter. Every other hit (e.g. `PCNT` ×15, `RECQL4` ×4, `BRCA2` ×3, `TP53` p.Pro72Arg
rs1042522, a common `TP53` 3′ indel at AF 0.71, an `NBN` splice-region SNP at AF 0.41) is a common
benign polymorphism.

### 3.4 The two `BUB1B` variants

Both are high-quality heterozygous calls in the VCF: FILTER = PASS, `MQ` = 60, `GQ` = 99, balanced
allelic depth (A: `AD` 21,25 at DP 46; B: `AD` 15,13 at DP 28).

- **`c.2210T>G` p.(Leu737Ter)** — nonsense in exon 17/23. Removes 314 C-terminal residues including
  most of the BUBR1 kinase domain (~aa 766–1040). ClinVar: Pathogenic / Likely pathogenic
  (VCV000533901; RCV000641226, RCV003324778), cited in the MVA literature (PMID 15475955,
  21190457, 29641532). gnomAD v4 allele frequency ≈ 7.9×10⁻⁵ (exomes), consistent with a rare
  recessive pathogenic allele carried by unaffected heterozygotes.
- **`c.3006T>G` p.(Asn1002Lys)** — missense in the terminal exon (23/23), within the kinase domain.
  **Absent from gnomAD v4.** All three orthogonal predictors concur: SIFT deleterious (0.01),
  PolyPhen-2 probably damaging (0.997), AlphaMissense likely pathogenic (0.923). Being in the last
  exon it escapes nonsense-mediated decay and is expected to produce a stable, hypomorphic protein.

A third rare `BUB1B` variant, `c.2679-1026A>G` (`chr15:40216470`), is **deep intronic** (1,026 bp
from the nearest splice site) and was excluded.

GATK did not report physical phasing (`PID`/`PGT`) for A and B — expected, as they lie 10,911 bp
apart, far beyond read/fragment length.

### 3.5 Orthogonal validation: k-mer-targeted re-alignment of BUB1B (`extraer_bub1b.sh`, `05_analisis_bam.py`)

To (a) confirm both variants from raw reads and (b) exclude a heterozygous exon deletion or a
structural variant as the second allele, BUB1B reads were extracted directly from the FASTQ without
a genome-wide alignment:

1. `bbduk` (k = 31, exact match) kept only read pairs sharing a 31-mer with the **repeat-masked**
   BUB1B sequence ± 10 kb (~32,000 unique k-mers). ~536 M input pairs → **10,508 matched pairs**
   (0.002 %).
2. Matched pairs were aligned with `minimap2 -ax sr` to chromosome 15, filtered to MAPQ ≥ 20 and
   the gene window, and sorted → `bub1b.bam` (mean depth 33.8× across the gene body; per-exon
   median 54×).

Findings:

- **No heterozygous exon deletion.** Every one of the 23 exons lies at 0.72–1.44× the per-exon
  median depth, each 100 % covered; none approaches the ~0.5× signature of a heterozygous deletion
  (`cobertura_exones_bub1b.png`). → the second allele is **not a copy-number variant**.
- **Both variants confirmed heterozygous from raw reads**, independent of the GATK caller:
  - p.(Leu737Ter): depth 52, 25 REF `T` / **27 ALT `G`**, VAF **0.52**, strand-balanced
    (REF 14+/11−, ALT 15+/12−), median MAPQ 60, median BASEQ 37.
  - p.(Asn1002Lys): depth 32, 16 REF `T` / **16 ALT `G`**, VAF **0.50**, both strands
    (ALT 6+/10−), median MAPQ 60, median BASEQ 37.
- **No structural variant** affecting BUB1B: zero reads with a mate on another chromosome; the only
  soft-clip cluster is within the AT-rich 3′UTR (downstream of the stop codon at
  `chr15:40220759`), where alignment is intrinsically noisy and the original GATK VCF also called
  nothing → alignment artefact, not a breakpoint.

→ **p.(Asn1002Lys) is confirmed as the second allele; no alternative (CNV / SV) exists.**

---

## 4. Interpretation

### ACMG/AMP classification

- **p.(Leu737Ter):** PVS1 (nonsense in a gene where loss of function is the established disease
  mechanism for MVA1) + PM2_supporting (rare in gnomAD) + supporting evidence from an existing
  Pathogenic ClinVar entry with literature. → **Pathogenic.**
- **p.(Asn1002Lys):** PM2 (absent from gnomAD) + PP3_moderate (SIFT, PolyPhen-2 and AlphaMissense
  concordantly deleterious; residue in the kinase domain) + PP4 (phenotype highly specific for
  MVA1) + PM3 (*in trans* with a Pathogenic variant — **assumed**; see limitations). →
  **Likely pathogenic** (Pathogenic if the *trans* configuration is confirmed).

The genotype — **one truncating allele plus one rare missense allele** — is the canonical MVA1
configuration. Biallelic complete loss of *BUB1B* is thought to be embryonic-lethal; described
MVA1 patients characteristically carry a null allele together with a missense or expression-
reducing hypomorphic allele (Hanks et al., 2004; subsequent case series).

### Why MVA1 despite no visible mosaic aneuploidy in the WGS

MVA is defined cytogenetically by **multiple different aneuploidies in different cells**, but the
cellular hallmark of *BUB1B*-related MVA is **premature chromatid separation (PCS)**, which is
invisible to short-read WGS. The proportion of aneuploid cells is highly tissue-variable and often
low in peripheral blood (the likely source of this sample) relative to cultured fibroblasts, and
aneuploid clones are selected against *in vivo*. A flat SNP allele-balance profile therefore does
**not** exclude MVA1; it indicates only that any constitutional mosaic aneuploidy in the sequenced
tissue is below the detection limit of BAF/depth analysis (≈ 10–15 % of cells).

---

## 5. Limitations and recommended confirmation

1. **Phase not experimentally established.** Short reads cannot phase variants 10.9 kb apart and no
   parental DNA was provided. Compound heterozygosity is strongly inferred (two rare damaging
   variants in a recessive gene, matching phenotype, no consanguinity) but is formally an
   assumption. → **Targeted Sanger sequencing of both positions in each parent** would confirm
   *trans* and upgrade p.(Asn1002Lys) to Pathogenic.
2. **Cellular diagnosis of MVA** requires a karyotype of cultured lymphocytes/fibroblasts plus a
   PCS assay.
3. Mosaic aneuploidy may be tissue-dependent; a fibroblast sample would be more informative than
   blood.

---

## 6. Reproducibility

All code, parameters and intermediate outputs are in the accompanying GitHub repository
(`analisis/` = VCF pipeline, `align/` = targeted re-alignment). The controlled-access dataset is
**not** redistributed. Key scripts: `01_cnv_baf.py`, `02_genes_candidatos.py`, `03_bub1b_workup.py`,
`extraer_bub1b.sh`, `05_analisis_bam.py`. External resources: Ensembl REST / VEP REST, Ensembl
GRCh38 chromosome-15 FASTA.

## 7. AI-assistance disclosure

This analysis was performed with substantial assistance from **Claude (Anthropic), via Claude
Code** (agentic CLI). Claude designed and wrote the analysis scripts, ran them locally, interpreted
outputs and drafted this report, under human direction. **Data handling:** all genomic files were
processed by scripts executing on the local machine; the raw controlled-access data (FASTQ, VCF)
were never uploaded to Anthropic. Portions of derived results and a limited number of individual
VCF lines passed through the model's context during the interactive session. No dataset content
was used for model training (Claude Code API traffic is not trained on).

## 8. Author's note

I am not a specialist. I have no formal training in bioinformatics, genetics or software
engineering; I am someone who was moved by this child's story and spent my free time over the
course of the hackathon learning the biology and the tooling needed to work through the case, with
an AI assistant acting less as a code generator and more as a tutor. Inexperience is a real risk to a report like this, and I have
tried to compensate for it directly rather than hide it: every key finding is checked by a second,
independent method — the two variants are confirmed both by the GATK calls and by re-alignment of
the raw reads; the absence of a deletion is verified by per-exon coverage; the aneuploidy screen
is cross-checked against read depth — and every point where I am uncertain, above all the phasing
of the two alleles, is stated plainly instead of smoothed over. The findings should stand on that
validation, not on my credentials.

## 9. Key references

- Hanks S, Coleman K, Reid S, *et al.* Constitutional aneuploidy and cancer predisposition caused
  by biallelic mutations in *BUB1B*. *Nat Genet.* 2004;36(11):1159–61. (PMID 15475955)
- OMIM #257300 (Mosaic Variegated Aneuploidy syndrome 1); *BUB1B* #602860.
- ClinVar VCV000533901 (`BUB1B` c.2210T>G, p.Leu737Ter).
- Ensembl VEP; gnomAD v4; AlphaMissense (Cheng *et al.*, *Science* 2023).
