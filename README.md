# Space Earth Dashboard

Backend i dashboard do prezentowania danych z NASA APOD, NASA NeoWs oraz pozycji ISS.

## Stack

- Python 3.11+
- FastAPI
- PostgreSQL
- Docker Compose
- Pytest
- Locust

## Uruchomienie developerskie

```powershell
docker compose -f docker-compose.dev.yml up --build
```

API: <http://localhost:8000/api/v1/health>

Swagger: <http://localhost:8000/docs>

## Zapis danych do PostgreSQL

Po uruchomieniu Dockera zainicjalizuj tabele:

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/v1/space/database/init
```

Nastepnie mozna zapisac dane pobrane z API:

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/v1/space/ingest/apod
Invoke-RestMethod -Method Post http://localhost:8000/api/v1/space/ingest/iss-position
Invoke-RestMethod -Method Post "http://localhost:8000/api/v1/space/ingest/neo?start_date=2026-05-23"
```

Zapisane obserwacje sa dostepne pod:

```text
http://localhost:8000/api/v1/space/observations
```

## Bledy zewnetrznych API

Gdy NASA albo Open Notify nie odpowiada, backend zwraca czytelny blad JSON, np.:

```json
{
  "detail": "NASA API request failed with status 429.",
  "source": "nasa",
  "upstream_status_code": 429
}
```

Bledy sa rowniez zapisywane w logach aplikacji.

## Testy

```powershell
pip install -e ".[dev]"
pytest
```

## Test wydajnosciowy

```powershell
locust -f tests/performance/locustfile.py --host http://localhost:8000
```

## Srodowiska

- `docker-compose.dev.yml` - hot reload i lokalna baza developerska.
- `docker-compose.test.yml` - uruchamianie testow w izolowanym kontenerze.
- `docker-compose.prod.yml` - konfiguracja produkcyjna z osobnym plikiem `.env`.
