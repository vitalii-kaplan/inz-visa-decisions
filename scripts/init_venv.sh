#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
VENV_DIR="${PROJECT_ROOT}/.venv"
KERNEL_NAME="inz-visa-decisions"
KERNEL_DISPLAY_NAME="Python (.venv: INZ Visa decisions)"

cd "${PROJECT_ROOT}"

if [ ! -d "${VENV_DIR}" ]; then
  python3 -m venv "${VENV_DIR}"
fi

"${VENV_DIR}/bin/python" -m pip install --upgrade pip
"${VENV_DIR}/bin/python" -m pip install -r requirements.txt
"${VENV_DIR}/bin/python" -m ipykernel install \
  --sys-prefix \
  --name "${KERNEL_NAME}" \
  --display-name "${KERNEL_DISPLAY_NAME}"

echo "Virtual environment ready: ${VENV_DIR}"
echo "Activate with: source .venv/bin/activate"
echo "Notebook kernel: ${KERNEL_DISPLAY_NAME}"
