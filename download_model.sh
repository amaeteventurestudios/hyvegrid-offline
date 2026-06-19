#!/usr/bin/env bash
set -euo pipefail

mkdir -p model

MODEL_PATH="model/hyvegrid-offline.gguf"
MODEL_URL="PUBLIC_MODEL_URL_HERE"

if [ -f "$MODEL_PATH" ]; then
  echo "Model already exists at $MODEL_PATH"
  exit 0
fi

if [ "$MODEL_URL" = "PUBLIC_MODEL_URL_HERE" ]; then
  echo "MODEL_URL has not been set yet."
  echo "Do not run this script until a GGUF model has been selected and verified."
  echo "Next step: fill artifacts/model-candidate-matrix.md and choose a candidate."
  exit 1
fi

echo "Downloading HyveGrid Offline model..."
curl -L "$MODEL_URL" -o "$MODEL_PATH"

echo "Downloaded model to $MODEL_PATH"