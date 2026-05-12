# Le Tre Gemme Backend

Backend FastAPI per esporre API al frontend React e gestire i contenuti salvati su MySQL.

## Requisiti

- Python 3.11+
- MySQL avviato via Docker Compose dalla root del progetto

## Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Avvio database

Dalla root del progetto:

```powershell
docker compose up -d
```

## Avvio API

Dalla cartella `backend`:

```powershell
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

La porta puo essere modificata nel file `.env` tramite `API_PORT`.

## Autenticazione admin

Le API sotto `/api/admin/*` richiedono un JWT Bearer ottenuto con:

```http
POST /api/auth/login
```

Variabili `.env` consigliate:

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=una-password-sicura
JWT_SECRET_KEY=una-chiave-lunga-e-casuale
JWT_EXPIRES_MINUTES=60
```

## Struttura

- `main.py`: entrypoint FastAPI.
- `lib/logger.py`: configurazione logging con rotazione giornaliera.
- `lib/database.py`: configurazione SQLAlchemy e connessione MySQL.
- `lib/db_session.py`: dependency injection della sessione DB.
- `models/`: modelli SQLAlchemy e schemi Pydantic.
- `abstractrepository/`: contratti base dei repository.
- `repository/`: accesso concreto al database.
- `services/`: logica applicativa.
- `routes/`: rotte FastAPI.
- `logs/`: file di log generati.

## Endpoint MVP

- `GET /api/health`
- `POST /api/auth/login`
- `GET /api/rooms`
- `GET /api/rooms/{room_id}`
- `GET /api/places`
- `GET /api/places/{place_id}`
- `GET /api/about`

