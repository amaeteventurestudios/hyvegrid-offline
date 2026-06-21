#!/usr/bin/env bash
set -euo pipefail

mkdir -p model

MODEL_PATH="model/hyvegrid-offline.gguf"
MODEL_URL="https://huggingface.co/ibm-granite/granite-3.3-2b-instruct-GGUF/resolve/main/granite-3.3-2b-instruct-Q4_K_M.gguf"
MODEL_SHA256="ac71e9e32c0bea919b409c5918f69ca74339854b0319c5065e4e9fb6d95c4852"

if [ -f "$MODEL_PATH" ]; then
  echo "Model already exists at $MODEL_PATH"
else
  echo "Downloading HyveGrid Offline model..."
  curl -L --fail -C - "$MODEL_URL" -o "$MODEL_PATH"
fi

echo "Verifying SHA256..."
ACTUAL_SHA256="$(shasum -a 256 "$MODEL_PATH" | awk '{print $1}')"
if [ "$ACTUAL_SHA256" != "$MODEL_SHA256" ]; then
  echo "SHA256 mismatch for $MODEL_PATH"
  echo "Expected: $MODEL_SHA256"
  echo "Actual:   $ACTUAL_SHA256"
  exit 1
fi

echo "Model ready at $MODEL_PATH"
