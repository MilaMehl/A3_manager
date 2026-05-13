#!/bin/sh
set -e

# Restaura o banco mock caso não exista (primeira execução ou container novo)
if [ ! -f "instance/app.db" ]; then
  echo "[entrypoint] Banco de dados não encontrado. Restaurando mock inicial..."
  cp /app/instance/app.db.seed instance/app.db 2>/dev/null || true
fi

echo "[entrypoint] Verificando migrations..."
if [ ! -d "migrations/versions" ] || [ -z "$(ls -A migrations/versions 2>/dev/null)" ]; then
  echo "[entrypoint] Pasta de migrations vazia ou ausente. Inicializando..."
  flask db init || true
  flask db migrate -m "initial migration"
fi

echo "[entrypoint] Aplicando migrations..."
# Corrige possível divergência entre revisão no banco e arquivos de migration
flask db upgrade 2>/dev/null || {
  echo "[entrypoint] Erro no upgrade. Alinhando revisão ao estado atual do banco..."
  flask db stamp head
  flask db upgrade
}

echo "[entrypoint] Rodando seeders..."
python3 -c "
from app import create_app
from app.seeders import run_all_seeders
app = create_app()
with app.app_context():
    run_all_seeders()
"

if [ "$FLASK_ENV" = "development" ]; then
  echo "[entrypoint] Iniciando servidor em modo DESENVOLVIMENTO (hot-reload ativo)..."
  exec flask run --host=0.0.0.0 --port=5000 --debug --reload
else
  echo "[entrypoint] Iniciando servidor em modo PRODUÇÃO..."
  exec python3 run.py
fi
