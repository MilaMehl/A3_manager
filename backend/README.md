# Propedido Backend Mock

API REST desenvolvida em **Flask** com banco de dados **SQLite**, estruturada no padrão **MVC** (Models, Views, Controllers), com autenticação via **JWT** e suporte a **Docker**.

---

## 📋 Requisitos

- Python 3.11+
- pip
- Docker e Docker Compose (opcional)

---

## 🚀 Como rodar a aplicação

### Opção 1 — Localmente

**1. Clone o repositório e acesse a pasta:**
```bash
cd propedido-backend-mock
```

**2. Crie e ative o ambiente virtual:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o .env com suas configurações
```

**5. Rode as migrations:**
```bash
flask db upgrade
```

**6. Rode o seeder para criar o usuário administrador:**
```bash
python3 -c "
from app import create_app
from app.seeders import run_all_seeders
app = create_app()
with app.app_context():
    run_all_seeders()
"
```

**7. Inicie o servidor:**
```bash
python3 run.py
```

A API estará disponível em: `http://localhost:5000`

---

### Opção 2 — Docker

**1. Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o .env com suas configurações
```

**2. Escolha o modo de execução:**

#### 🛠️ Modo Desenvolvimento (hot-reload ativo)
Qualquer alteração no código é refletida automaticamente, sem necessidade de rebuild.
```bash
./docker-dev.sh
```
> Equivalente a: `docker compose up api-dev --build`

#### 🚀 Modo Produção
Sobe a aplicação em background, otimizada para produção.
```bash
./docker-prod.sh
```
> Equivalente a: `docker compose up api --build -d`

> ✅ As migrations e o seeder são executados **automaticamente** ao subir qualquer container.

**Outros comandos úteis:**

Ver logs:
```bash
docker compose logs -f
```

Parar containers:
```bash
docker compose down
```

#### Diferenças entre os modos

| Característica | Desenvolvimento (`api-dev`) | Produção (`api`) |
|---|---|---|
| Hot-reload | ✅ Sim | ❌ Não |
| Código montado em volume | ✅ Sim | ❌ Não |
| Roda em background | ❌ Não | ✅ Sim |
| `FLASK_ENV` | `development` | `production` |

---

## 👤 Usuário administrador (Seeder)

Um usuário administrador é criado automaticamente ao rodar o seeder:

| Campo | Valor |
|-------|-------|
| **E-mail** | `admin@sistema.com.br` |
| **Senha** | `Admin123!` |

> O seeder é **idempotente**: se o usuário já existir, ele não será duplicado.

---

## 🔐 Autenticação

Todas as rotas protegidas exigem um token JWT no header:

```
Authorization: Bearer <token>
```

O token é obtido na rota de login descrita abaixo.

---

## 📡 Rotas disponíveis

### 1. Login
**`POST /api/auth/login`**

Autentica o usuário e retorna o token JWT.

**Body:**
```json
{
  "email": "admin@sistema.com.br",
  "password": "Admin123!"
}
```

**Resposta de sucesso (`200`):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "nome": "Administrador",
    "email": "admin@sistema.com.br",
    "created_at": "2026-04-20T10:00:00",
    "updated_at": "2026-04-20T10:00:00"
  }
}
```

**Resposta de erro (`401`):**
```json
{
  "error": "Email ou senha inválidos."
}
```

---

### 2. Listar Solicitações
**`GET /api/requests/`** 🔒 *requer token*

Retorna as solicitações filtradas. Todos os parâmetros são **opcionais** e combináveis.

**Query params:**

| Parâmetro | Tipo | Exemplo | Descrição |
|-----------|------|---------|-----------|
| `date_from` | string | `2024-01-01` | Data inicial (formato `YYYY-MM-DD`) |
| `date_to` | string | `2024-12-31` | Data final (formato `YYYY-MM-DD`) |
| `status` | string | `em andamento` | Filtra por status (busca parcial) |
| `classification` | string | `buraco` | Filtra por classificação (busca parcial) |
| `address` | string | `Paulista` | Filtra por endereço (busca parcial, case-insensitive) |

**Exemplo de requisição:**
```
GET /api/requests/?status=em+andamento&address=Paulista&date_from=2024-01-01
Authorization: Bearer <token>
```

**Resposta de sucesso (`200`):**
```json
{
  "total": 2,
  "data": [
    {
      "id": 1,
      "address": "Rua das Flores, 123",
      "classification": "Buraco na via",
      "date": "2024-06-15T08:30:00",
      "latitude": -23.5505,
      "longitude": -46.6333,
      "photo_path": "public/images/abc123.jpg",
      "photo_url": "http://localhost:5000/static/public/images/abc123.jpg",
      "status": "em andamento",
      "created_at": "2026-04-20T10:00:00",
      "updated_at": "2026-04-20T10:00:00"
    }
  ]
}
```

---

### 3. Listar Agrupamentos
**`GET /api/groupings/`** 🔒 *requer token*

Retorna os agrupamentos de solicitações. Se qualquer filtro for informado, retorna apenas os grupos que possuem ao menos uma solicitação compatível. Todos os parâmetros são **opcionais** e combináveis.

**Query params:**

| Parâmetro | Tipo | Exemplo | Descrição |
|-----------|------|---------|-----------|
| `address` | string | `Centro` | Filtra grupos cujo request contenha o endereço (busca parcial, case-insensitive) |
| `status` | string | `E` | Filtra pelo status do agrupamento |
| `classification` | string | `A` | Filtra pela classificação do agrupamento |
| `date_from` | string | `2024-01-01` | Filtra grupos com requests a partir desta data |
| `date_to` | string | `2024-12-31` | Filtra grupos com requests até esta data |

**Exemplo de requisição:**
```
GET /api/groupings/?address=Centro&classification=A&date_from=2024-01-01
Authorization: Bearer <token>
```

**Resposta de sucesso (`200`):**
```json
{
  "total": 1,
  "data": [
    {
      "id": 1,
      "latitude": -23.5505,
      "longitude": -46.6333,
      "classification": "A",
      "status": "E",
      "date": "2024-06-15T00:00:00",
      "created_at": "2026-04-20T10:00:00",
      "updated_at": "2026-04-20T10:00:00",
      "total_requests": 3,
      "requests": [
        {
          "id": 1,
          "address": "Rua das Flores, 123",
          "classification": "Buraco na via",
          "date": "2024-06-15T08:30:00",
          "latitude": -23.5505,
          "longitude": -46.6333,
          "photo_path": "public/images/abc123.jpg",
          "photo_url": "http://localhost:5000/static/public/images/abc123.jpg",
          "status": "em andamento",
          "created_at": "2026-04-20T10:00:00",
          "updated_at": "2026-04-20T10:00:00"
        }
      ]
    }
  ]
}
```

---

### 4. Traçar Rota por Solicitações
**`POST /api/routes/`** 🔒 *requer token*

Recebe a localização atual do usuário e uma lista de IDs de **solicitações**. Retorna os pontos ordenados pelo melhor trajeto (algoritmo Nearest Neighbor) e uma URL do Google Maps para navegação.

**Body:**
```json
{
  "latitude": -23.5505,
  "longitude": -46.6333,
  "request_ids": [1, 5, 12, 30, 47]
}
```

**Resposta de sucesso (`200`):**
```json
{
  "total_stops": 5,
  "total_distance_km": 12.4,
  "origin": {
    "latitude": -23.5505,
    "longitude": -46.6333
  },
  "ordered_stops": [
    {
      "id": 5,
      "address": "Rua das Flores, 123",
      "classification": "Buraco na via",
      "status": "em andamento",
      "latitude": -23.551,
      "longitude": -46.634,
      "distance_from_prev_km": 1.2
    }
  ],
  "google_maps_url": "https://www.google.com/maps/dir/?api=1&origin=...&destination=...&waypoints=...&travelmode=driving",
  "requests_without_coords": []
}
```

---

### 5. Traçar Rota por Agrupamentos
**`POST /api/grouping-routes/`** 🔒 *requer token*

Semelhante à rota anterior, porém recebe IDs de **agrupamentos** (`InfoGroupingRequest`) em vez de solicitações individuais. Utiliza as coordenadas do centroide de cada agrupamento para calcular o trajeto otimizado.

**Body:**
```json
{
  "latitude": -23.5505,
  "longitude": -46.6333,
  "grouping_ids": [1, 2, 3]
}
```

**Resposta de sucesso (`200`):**
```json
{
  "total_stops": 3,
  "total_distance_km": 8.7,
  "origin": {
    "latitude": -23.5505,
    "longitude": -46.6333
  },
  "ordered_stops": [
    {
      "id": 2,
      "classification": "A",
      "status": "E",
      "latitude": -23.551,
      "longitude": -46.634,
      "distance_from_prev_km": 0.9
    }
  ],
  "google_maps_url": "https://www.google.com/maps/dir/?api=1&origin=...&destination=...&waypoints=...&travelmode=driving",
  "groupings_without_coords": []
}
```

> O campo `google_maps_url` pode ser aberto diretamente no navegador ou no app do Google Maps para iniciar a navegação com todos os pontos já configurados.

---

## 🗂️ Estrutura do projeto

```
app/
├── configs/          # Configurações (banco de dados)
├── controllers/      # Lógica de entrada/saída das requisições
│   ├── auth_controller.py
│   ├── grouping_controller.py
│   ├── grouping_route_controller.py
│   ├── request_controller.py
│   └── route_controller.py
├── middlewares/      # Autenticação JWT
├── models/           # Modelos do banco de dados (SQLAlchemy)
│   ├── user_model.py
│   ├── request_model.py
│   ├── info_grouping_request_model.py
│   └── grouping_request_model.py
├── repositories/     # Acesso ao banco de dados
│   ├── user_repository.py
│   ├── request_repository.py
│   ├── grouping_repository.py
│   └── route_repository.py
├── routes/           # Definição dos endpoints
│   ├── auth_routes.py          → /api/auth
│   ├── request_routes.py       → /api/requests
│   ├── grouping_routes.py      → /api/groupings
│   ├── route_routes.py         → /api/routes
│   └── grouping_route_routes.py → /api/grouping-routes
├── seeders/          # Dados iniciais do banco
└── services/         # Regras de negócio
    ├── auth_service.py
    ├── request_service.py
    ├── grouping_service.py
    ├── grouping_route_service.py
    └── route_service.py
migrations/           # Migrations do Alembic
tests/                # Testes unitários e de integração
├── models/           # Testes dos models
├── repositories/     # Testes dos repositórios
├── services/         # Testes dos services
├── controllers/      # Testes dos controllers
└── routes/           # Testes de integração das rotas
instance/             # Banco de dados SQLite (gerado automaticamente)
```

---

## 🧪 Testes

O projeto utiliza **pytest** para testes unitários e de integração. Os testes rodam com banco em memória (SQLite `:memory:`), sem afetar o banco de dados real.

### Rodando os testes

```bash
# Todos os testes
python3 -m pytest

# Com saída detalhada
python3 -m pytest -v

# Uma pasta específica
python3 -m pytest tests/services/

# Um arquivo específico
python3 -m pytest tests/services/test_auth_service.py
```

### Cobertura dos testes (185 testes)

#### Models (`tests/models/`)
| Arquivo | O que é testado |
|---|---|
| `test_request_model.py` | `to_dict`, campos nulos, persistência |
| `test_info_grouping_request_model.py` | `to_dict`, lat/lon como float, persistência |
| `test_grouping_request_model.py` | Relacionamentos, cascade delete, múltiplos vínculos |

#### Repositories (`tests/repositories/`)
| Arquivo | O que é testado |
|---|---|
| `test_request_repository.py` | Filtros por status, classification, address, datas, ordenação |
| `test_grouping_repository.py` | Filtros por address, status, classification, datas; requests por grupo |
| `test_route_repository.py` | Busca por IDs, lista vazia, IDs inexistentes |
| `test_user_repository.py` | Busca por e-mail e por ID |

#### Services (`tests/services/`)
| Arquivo | O que é testado |
|---|---|
| `test_auth_service.py` | Login, geração e decodificação de token JWT |
| `test_request_service.py` | Parsing de datas, URL de foto, repasse de todos os filtros |
| `test_grouping_service.py` | Parsing de datas, serialização, repasse de filtros, agrupamentos |
| `test_route_service.py` | Haversine, Nearest Neighbor, URL do Google Maps |
| `test_grouping_route_service.py` | Rota por agrupamentos, coordenadas ausentes, URL do Google Maps |

#### Controllers (`tests/controllers/`)
| Arquivo | O que é testado |
|---|---|
| `test_auth_controller.py` | Login, validações de body, campos obrigatórios |
| `test_request_controller.py` | Listagem, repasse de filtros, data inválida, autenticação |
| `test_grouping_controller.py` | Listagem, repasse de filtros, erro interno, autenticação |
| `test_route_controller.py` | Rota por requests, validações de body, autenticação |
| `test_grouping_route_controller.py` | Rota por agrupamentos, validações de body, autenticação |

#### Routes (`tests/routes/`)
| Arquivo | O que é testado |
|---|---|
| `test_auth_routes.py` | Middleware JWT (válido/inválido/expirado), rota de login |
| `test_request_routes.py` | Endpoint `/api/requests/`, filtros, método não permitido |
| `test_grouping_routes.py` | Endpoint `/api/groupings/`, filtros, método não permitido |
| `test_route_routes.py` | Endpoint `/api/routes/`, validações, autenticação |
| `test_grouping_route_routes.py` | Endpoint `/api/grouping-routes/`, validações, autenticação |
