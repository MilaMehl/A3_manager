#!/bin/bash
set -e

echo "[prod] Subindo container de produção..."
docker compose up api --build -d
