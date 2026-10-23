#!/bin/bash
# Pipeline de evidencia para Track 2. Resumible (cada etapa cachea su salida).
# Lanzar capeado:
#   systemd-run --user --scope -p CPUQuota=200% -p MemoryMax=1500M -p MemoryHigh=1200M \
#     nice -n 19 ionice -c3 bash ~/mva-hackathon/track2/run_all.sh > ~/mva-hackathon/track2/run.log 2>&1 &
set -u
ulimit -Sv 2000000   # ~2 GB de memoria virtual como tope duro (el pipeline usa <400 MB)
cd "$(dirname "$0")"
PY="${PY:-python3}"
echo "=== INICIO $(date -Is) ==="
echo $$ > run.pid
trap 'rm -f run.pid' EXIT

for stage in 01_mechanism.py 02_target_drugs.py 03_pubmed_mining.py 04_neighborhood_trials.py; do
  echo "--- $stage  $(date -Is) ---"
  $PY "$stage"
  rc=$?
  echo "    ($stage exit $rc)"
done

echo "--- 05_consolidate.py  $(date -Is) ---"
$PY 05_consolidate.py

echo "=== FIN $(date -Is) ==="
ls -la out/
