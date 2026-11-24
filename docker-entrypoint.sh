#!/bin/sh
set -e

API_PORT="${API_PORT:-8001}"
UI_PORT="${PORT:-7860}"

if [ "$1" = "combined" ]; then
    export VAULT_API_URL="${VAULT_API_URL:-http://127.0.0.1:${API_PORT}/api}"

    uvicorn src.api.main:app --host 0.0.0.0 --port "$API_PORT" &
    api_pid=$!

    i=0
    while [ "$i" -lt 180 ]; do
        if python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:${API_PORT}/api/health', timeout=2)" >/dev/null 2>&1; then
            break
        fi
        i=$((i + 1))
        sleep 1
    done

    streamlit run src/ui/app.py \
        --server.address 0.0.0.0 \
        --server.port "$UI_PORT" \
        --server.headless true &
    ui_pid=$!

    trap 'kill "$api_pid" "$ui_pid" 2>/dev/null || true' TERM INT
    wait "$ui_pid"
    status=$?
    kill "$api_pid" 2>/dev/null || true
    exit "$status"
fi

exec "$@"
