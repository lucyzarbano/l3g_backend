# Database MySQL

Gli script in `backend/database/init` creano le tabelle pensate per sostituire i dati mockati nel frontend.

## Tabelle principali

- `rooms`: dati principali delle camere, inclusi prezzo, capienza, rating e visibilita.
- `room_images`: immagini delle camere, incluse gallery e cover.
- `services`: dizionario dei servizi con chiave icona FontAwesome.
- `room_services`: associazione camere-servizi, divisa tra `base` e `additional`.
- `room_badges`: etichette come "Piu comoda" o "Piu venduta".
- `places`: dati principali dei luoghi da vedere.
- `place_images`: gallery dei luoghi.
- `place_info_items`: info ripetute dei luoghi, come distanza, tipo e percorrenza.
- `about_sections`: contenuto principale del Chi siamo.
- `about_paragraphs`: paragrafi ordinati del Chi siamo.
- `about_images`: immagini del Chi siamo.

## Avvio

Gli script vengono montati in MySQL tramite `docker-compose.yml` e vengono eseguiti automaticamente solo quando il volume `mysql_data` viene inizializzato per la prima volta.

```powershell
docker compose up -d
```

Se il volume esiste gia e vuoi ricreare tutto da zero:

```powershell
docker compose down -v
docker compose up -d
```

## Accesso da Adminer

- URL: `http://localhost:8080`
- Sistema: `MySQL`
- Server: `mysql`
- Utente: `my_bb_user`
- Password: `my_bb_password`
- Database: `my_bb`

## Backoffice

Il backoffice dovra usare le API FastAPI esposte da `backend/main.py`.

Avvia MySQL:

```powershell
docker compose up -d
```

Avvia il backend FastAPI:

```powershell
cd backend
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Avvia il sito:

```powershell
cd frontend
npm run dev
```

Per configurare un host API diverso, usa:

```text
VITE_API_BASE_URL=http://localhost:8000/api
```
