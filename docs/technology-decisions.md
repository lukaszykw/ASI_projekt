# Uzasadnienie technologiczne

## Python + FastAPI

FastAPI dobrze pasuje do projektu, bo automatycznie generuje specyfikacje OpenAPI/Swagger,
ma prosta integracje z typami Pythona i pozwala szybko budowac asynchroniczne endpointy.

## PostgreSQL

PostgreSQL daje stabilna relacyjna baze danych, a pole JSONB pozwala przechowywac oryginalne
odpowiedzi z NASA i Open Notify bez utraty szczegolow. To dobry kompromis miedzy struktura
a elastycznoscia danych z roznych zrodel.

## Docker

Docker Compose rozdziela srodowiska developerskie, testowe i produkcyjne. Dzieki temu projekt
latwiej uruchomic na innym komputerze i latwiej pokazac powtarzalnosc konfiguracji.

## Testy

Testy jednostkowe obejmuja logike normalizacji i bazowe endpointy API. Testy wydajnosciowe sa
przygotowane w Locust, zeby zmierzyc zachowanie API pod obciazeniem.
