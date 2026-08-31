#!/bin/bash
# Fase 2 - extraccion dirigida de BUB1B.
#  1. bbduk por lane (archivos .gz directos): quedarse SOLO con pares que comparten
#     un 31-mer EXACTO con la secuencia NO-repetitiva de BUB1B +-10kb (~32k k-mers).
#  2. minimap2: alinear esos pares contra chr15.
#  3. filtrar MAPQ>=20 + ventana, ordenar, indexar -> align/bub1b.bam
# Resumible por lane (.kmer.done). Capeado desde el lanzador (nice + ionice).
set -uo pipefail
cd "$HOME/mva-hackathon"
source bio.sh

A=align
KREF="$A/bub1b_kmerref.fa"
WIN="15:40120000-40260000"     # BUB1B 40,160,984-40,221,137 + flanco

echo "=== INICIO $(date -Is) ==="
echo "$$" > "$A/extraer.pid"; trap 'rm -f "$A/extraer.pid"' EXIT

# --- 1. bbduk por lane ---
for L in L001 L002 L003 L004; do
  if [ -f "$A/${L}.kmer.done" ]; then echo "  $L ya hecho ($(zcat "$A/${L}.m_R1.fq.gz"|wc -l|awk '{print $1/4}') pares)"; continue; fi
  R1=$(ls data/*_${L}_R1_001.fastq.gz); R2=$(ls data/*_${L}_R2_001.fastq.gz)
  echo "--- bbduk $L  $(date -Is) ---"
  bbduk.sh -Xmx3g threads=2 overwrite=t \
    in="$R1" in2="$R2" \
    outm="$A/${L}.m_R1.fq.gz" outm2="$A/${L}.m_R2.fq.gz" \
    ref="$KREF" k=31 hdist=0 2> "$A/bbduk_${L}.log"
  rc=$?
  if [ "$rc" -ne 0 ]; then echo "  !! bbduk $L fallo rc=$rc — ver $A/bbduk_${L}.log"; exit 1; fi
  echo "  $L -> $(( $(zcat "$A/${L}.m_R1.fq.gz" | wc -l) / 4 )) pares"
  grep -E "^(Input|Contaminants|Result):" "$A/bbduk_${L}.log" | sed 's/^/    /'
  touch "$A/${L}.kmer.done"
done

# --- 2. concatenar matched + alinear ---
echo "--- concat + minimap2  $(date -Is) ---"
cat "$A"/L001.m_R1.fq.gz "$A"/L002.m_R1.fq.gz "$A"/L003.m_R1.fq.gz "$A"/L004.m_R1.fq.gz > "$A/all_R1.fq.gz"
cat "$A"/L001.m_R2.fq.gz "$A"/L002.m_R2.fq.gz "$A"/L003.m_R2.fq.gz "$A"/L004.m_R2.fq.gz > "$A/all_R2.fq.gz"
echo "  total matched: $(( $(zcat "$A/all_R1.fq.gz" | wc -l) / 4 )) pares"

minimap2 -ax sr -t 3 -R "@RG\tID:EX2312012\tSM:EX2312012\tPL:ILLUMINA\tLB:HGWCNDSX7" \
  ref/chr15.sr.mmi "$A/all_R1.fq.gz" "$A/all_R2.fq.gz" 2> "$A/minimap2.log" \
  | samtools sort -@2 -m 512M -o "$A/bub1b.full.bam" -
samtools index "$A/bub1b.full.bam"

# --- 3. ventana + MAPQ ---
samtools view -b -q 20 "$A/bub1b.full.bam" "$WIN" > "$A/bub1b.bam"
samtools index "$A/bub1b.bam"

echo "=== FIN $(date -Is) ==="
samtools flagstat "$A/bub1b.bam" | sed 's/^/  /'
echo "--- cobertura media, cuerpo de BUB1B (40,160,984-40,221,137) ---"
samtools depth -a -r 15:40160984-40221137 "$A/bub1b.bam" | awk '{s+=$3;n++} END{if(n)printf "  media %.1fx sobre %d bp con lectura\n",s/n,n}'
