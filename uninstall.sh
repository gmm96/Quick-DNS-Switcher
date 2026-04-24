#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(dirname "$(realpath "${0}")")"
TMP_SCRIPT="/tmp/qds-uninstall-$$.sh"
install -Dm755 "${SCRIPT_DIR}/qds/resources/bin/qds-uninstall.sh" "${TMP_SCRIPT}"

exec bash "${TMP_SCRIPT}" "${@}"
