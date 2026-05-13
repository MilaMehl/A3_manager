#!/bin/bash
set -e

echo "[dev] Subindo container de desenvolvimento..."
docker compose up api-dev --build
