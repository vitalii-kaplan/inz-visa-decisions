#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <workflow-directory>" >&2
  exit 2
fi

workflow_dir="${1%/}"

if [ ! -d "${workflow_dir}" ]; then
  echo "Workflow directory not found: ${workflow_dir}" >&2
  exit 1
fi

if [ ! -f "${workflow_dir}/workflow.knime" ]; then
  echo "workflow.knime not found in: ${workflow_dir}" >&2
  exit 1
fi

find "${workflow_dir}" -mindepth 1 -maxdepth 1 -type f ! -name "workflow.knime" -delete
find "${workflow_dir}" -mindepth 1 -maxdepth 1 -type d -name ".*" -exec rm -rf {} +

while IFS= read -r node_dir; do
  find "${node_dir}" -mindepth 1 ! -name "settings.xml" -exec rm -rf {} +
done < <(find "${workflow_dir}" -mindepth 1 -maxdepth 1 -type d | sort)
