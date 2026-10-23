#!/bin/bash
# Downloads the public datasets used by C1–C6 and the audit into data/ (not committed: see DATA.md).
# The md5 sums are those of the copies used for the report (DGIdb "latest" may change over time).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p data/c4_geo data/lit
get() {  # url  destination  md5
  if [ ! -s "$2" ]; then curl -fL --retry 3 -A "mva-hackathon-track2/1.0" -o "$2" "$1"; fi
  echo "$3  $2" | md5sum -c --quiet || echo "  ! md5 differs for $2 (upstream file changed?)"
}
get https://stringdb-downloads.org/download/protein.links.v12.0/9606.protein.links.v12.0.txt.gz data/string_links.txt.gz 5b7c91d02926e723ad30e81ab9d009a4
get https://stringdb-downloads.org/download/protein.info.v12.0/9606.protein.info.v12.0.txt.gz   data/string_info.txt.gz  1ca9efcefcc68b5cc3b037a335cb870b
get https://s3.amazonaws.com/data.clue.io/repurposing/downloads/repurposing_drugs_20200324.txt   data/repurposing_drugs_20200324.txt   b4b3233dad28d20a522c0200cc4123d1
get https://s3.amazonaws.com/data.clue.io/repurposing/downloads/repurposing_samples_20200324.txt data/repurposing_samples_20200324.txt 44067d6ea0e63c70f51e0469d60232ec
get https://dgidb.org/data/latest/interactions.tsv data/dgidb_interactions.tsv 67b4692af98b9d674bf494f5d9d8dc41
get https://dgidb.org/data/latest/drugs.tsv        data/dgidb_drugs.tsv        6b90ee60486809381850deedd46e34bd
get https://ftp.ncbi.nlm.nih.gov/geo/series/GSE277nnn/GSE277997/suppl/GSE277997_H_v_WT.csv.gz data/c4_geo/GSE277997_H_v_WT.csv.gz 32dbbe759ee77d5e25353748906ffe4a
get https://ftp.ncbi.nlm.nih.gov/geo/series/GSE134nnn/GSE134781/suppl/GSE134781_counts.txt.gz data/c4_geo/GSE134781_counts.txt.gz 5f47d660d5e4f8e48020d81fbee1bc76
get https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9631552/fullTextXML data/lit/PMC9631552.xml 65d9363348ae616941466c6522c834ff
echo "data/ ready"
