#!/usr/bin/env bash

set -euo pipefail

SCRIPT_PATH="$(realpath "$(readlink -f "${0}")")"
BASE_DIR="$(dirname "${SCRIPT_PATH}")"

exec env PYTHONPATH="${BASE_DIR}:${PYTHONPATH:-}" python3 -m qds.main "${@}"
