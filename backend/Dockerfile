FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia e garante permissão de execução no entrypoint
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Copia o restante do código
COPY . .

# Garante que a pasta de migrations está presente e com permissão
RUN chmod -R 755 migrations/

# Cria as pastas necessárias, salva o banco mock como seed e garante permissões
RUN mkdir -p instance app/static/public/images \
    && if [ -f instance/app.db ]; then cp instance/app.db instance/app.db.seed; fi \
    && chmod 664 instance/app.db 2>/dev/null || true

# Variáveis de ambiente padrão
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expõe a porta
EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
