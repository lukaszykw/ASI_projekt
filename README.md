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
