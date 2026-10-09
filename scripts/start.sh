#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export MPLCONFIGDIR="${MPLCONFIGDIR:-/tmp/polaris-matplotlib}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/tmp/polaris-cache}"
mkdir -p "$MPLCONFIGDIR" "$XDG_CACHE_HOME"
exec .venv/bin/python -m streamlit run app.py --server.address 0.0.0.0 --server.port "${PORT:-8501}" --server.headless true --browser.gatherUsageStats false
