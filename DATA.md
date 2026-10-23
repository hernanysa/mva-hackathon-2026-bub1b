# Data sources

This repository contains code, derived results and the submission deliverables. It does **not**
contain the controlled-access hackathon dataset or any genome-scale data about the proband.

## Controlled-access data (not included)

| Data | Where it comes from | Used by |
|---|---|---|
| WGS FASTQ, VCF and the clinical phenotype of `PROBAND01` | `SageBio/mva-hackathon-2026-data` (Hugging Face, gated; access requires accepting the Hackathon Rules) | Track 1 pipeline (`analisis/`, `align/`); pharmacogenomics (C8) |

Under the Hackathon Rules these data are deleted within 30 days of the hackathon close. Results derived
from them appear here only as named findings (the two `BUB1B` variants; the pharmacogenomic summary in
the Track 2 report, §6). The full pharmacogenomic genotype summary is kept private, so 9 of the 138
checks in `track2/audit_report.py` run only on the author's machine.

## Public data

Download everything with `bash investigacion/repurposing/get_data.sh` (about 110 MB into
`investigacion/repurposing/data/`, which is not committed). The script checks each file against the md5 of
the copy used for the report.

| Dataset | Version / retrieved | URL | md5 |
|---|---|---|---|
| STRING human protein links | v12.0 | https://stringdb-downloads.org/download/protein.links.v12.0/9606.protein.links.v12.0.txt.gz | `5b7c91d02926e723ad30e81ab9d009a4` |
| STRING human protein info | v12.0 | https://stringdb-downloads.org/download/protein.info.v12.0/9606.protein.info.v12.0.txt.gz | `1ca9efcefcc68b5cc3b037a335cb870b` |
| Broad Drug Repurposing Hub — drugs | 2020-03-24 | https://s3.amazonaws.com/data.clue.io/repurposing/downloads/repurposing_drugs_20200324.txt | `b4b3233dad28d20a522c0200cc4123d1` |
| Broad Drug Repurposing Hub — samples | 2020-03-24 | https://s3.amazonaws.com/data.clue.io/repurposing/downloads/repurposing_samples_20200324.txt | `44067d6ea0e63c70f51e0469d60232ec` |
| DGIdb interactions | "latest", retrieved 2026-09-01 | https://dgidb.org/data/latest/interactions.tsv | `67b4692af98b9d674bf494f5d9d8dc41` |
| DGIdb drugs | "latest", retrieved 2026-09-01 | https://dgidb.org/data/latest/drugs.tsv | `6b90ee60486809381850deedd46e34bd` |
| GEO GSE277997 (BubR1-insufficient mouse heart, DE table) | retrieved 2026-09-10 | https://ftp.ncbi.nlm.nih.gov/geo/series/GSE277nnn/GSE277997/suppl/GSE277997_H_v_WT.csv.gz | `32dbbe759ee77d5e25353748906ffe4a` |
| GEO GSE134781 (BubR1 carrier mouse muscle, counts) | retrieved 2026-09-10 | https://ftp.ncbi.nlm.nih.gov/geo/series/GSE134nnn/GSE134781/suppl/GSE134781_counts.txt.gz | `5f47d660d5e4f8e48020d81fbee1bc76` |
| Pollard et al. 2022, full text (Fanconi anaemia metformin trial) | Europe PMC PMC9631552 | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9631552/fullTextXML | `65d9363348ae616941466c6522c834ff` |
| AlphaFold model of human BUBR1 | AF-O60566-F1, model v6 | https://alphafold.ebi.ac.uk/files/AF-O60566-F1-model_v6.pdb (downloaded by `investigacion/estructura/n1002_structure.py`) | `943e5596717db0424b1a020ae429e174` |

DGIdb serves its current release at the "latest" URL, so a later download may differ from the copy used here.

## Public APIs (queried live by the scripts)

| Service | Endpoint | Queried | Used by |
|---|---|---|---|
| Europe PMC | https://www.ebi.ac.uk/europepmc/webservices/rest | 2026-09 | C2 |
| NCBI E-utilities (PubMed) | https://eutils.ncbi.nlm.nih.gov/entrez/eutils | 2026-09-01 | curated pipeline (`track2/03_pubmed_mining.py`) |
| L1000CDS2 (LINCS) | https://maayanlab.cloud/L1000CDS2/query | 2026-09 | C3, C4 |
| Enrichr | https://maayanlab.cloud/Enrichr | 2026-09-10 | C6 |
| ClinicalTrials.gov API v2 | https://clinicaltrials.gov/api/v2/studies | 2026-09-09/10, 2026-10-07 | C7, curated pipeline |
| openFDA FAERS | https://api.fda.gov/drug/event.json | data last updated 2026-07-30 | C9 |
| Open Targets Platform | https://api.platform.opentargets.org/api/v4/graphql | 2026-09-10 | C10, curated pipeline |
| UniProt, KEGG, Reactome, STRING API, DGIdb, ChEMBL | see `track2/01_mechanism.py`, `02_target_drugs.py` | 2026-09-01 | curated pipeline |

API results change over time; each script saves what it received (`*.json`, `*.tsv`, `*_RESULTADO.md`),
and the audit checks the report against those saved outputs.

## Narration voice (video)

`video/make_video.py` uses the offline Piper voice `en_US-lessac-high`:
`python3 -m piper.download_voices --data-dir video/voices en_US-lessac-high` (about 110 MB; not committed).
