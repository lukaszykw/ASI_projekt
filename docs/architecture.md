# Architektura

## C4 - Container View

```mermaid
flowchart LR
    nasa[NASA API<br/>APOD + NeoWs]
    openNotify[Open Notify<br/>ISS position]
    ingestion[Python ingestion<br/>httpx + normalizacja]
    db[(PostgreSQL<br/>space_observations)]
    api[FastAPI REST API<br/>Swagger/OpenAPI]
    frontend[Frontend dashboard<br/>HTML + CSS + JS]

    nasa --> ingestion
    openNotify --> ingestion
    ingestion --> db
    db --> api
    api --> frontend
```

## Przeplyw danych

1. Klient ingestion pobiera JSON z zewnetrznych API.
2. Normalizatory wybieraja potrzebne pola i zachowuja surowy payload do audytu.
3. Dane trafiaja do PostgreSQL jako rekordy obserwacji.
4. FastAPI wystawia endpointy REST i dokumentacje Swagger pod `/docs`.
5. Frontend pobiera dane z backendu i pokazuje dashboard.
