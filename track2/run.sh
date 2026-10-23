#!/bin/bash
# Regenera figuras y PDF del report de Track 2 con las cachés dentro del proyecto.
set -e
[ -f "$HOME/mva-hackathon/env.sh" ] && source "$HOME/mva-hackathon/env.sh"   # entorno del autor; opcional
cd "$(dirname "$0")"
python3 make_figures.py
python3 build_pdf.py
