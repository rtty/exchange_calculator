# Currency exchange API

## Prerequisites

- PostgreSQL (`docker & docker-compose`)
- Python v3.11
- Pip3
- Docker


## Configuration

Located in the file `config.py` and can be changed by setting corresponding environment variables:

- **DATABASE_URL** PostgreSQL database url

Configuration parameters can be set in either `.env`, or through environment variables.

## Local deployment

1. Install requirements: `pip3 install -r requirements.txt`

2. Before running application, start postgres database in docker, `docker-compose up --build db`

3. Run application 
- `python main.py`

4. To run as uvicorn server 
- `uvicorn main:app`

5. Populate historical data:
- `python populate.py --input-file data/exchange.csv`

## Docker deployment


1. Start postgres database and app in docker, `docker-compose up --build`

2. Populate historical data:

- `docker exec exchange-api python populate.py --input-file data/exchange.csv`

## Verification

### Swagger

```
http://localhost:8000/docs
```

### API

CRUD currency operations:

```bash
curl -i --request POST --location 'http://127.0.0.1:8000/currencies/' --header 'Content-Type: application/json' --data '{"code": "USD"}'
```

```bash
curl -i --request PUT --location 'http://127.0.0.1:8000/currencies/1' --header 'Content-Type: application/json' --data '{"code": "USA"}'
```

```bash
curl -i --request DELETE --location 'http://127.0.0.1:8000/currencies/USA' --header 'Content-Type: application/json'
```

Retrieve all currencies:

```bash
curl -i --request GET --location 'http://127.0.0.1:8000/currencies/' --header 'Content-Type: application/json'
```

CRUD rate operations:

```bash
curl -i --request POST --location 'http://127.0.0.1:8000/rates/' --header 'Content-Type: application/json' --data '{"rate": 0.91,"currency_base": "USD", "currency_target": "EUR","date": "2023-12-20"}'
```

```bash
curl -i --request PUT --location 'http://127.0.0.1:8000/rates/1' --header 'Content-Type: application/json' --data '{"rate": 0.92,"currency_base": "USD", "currency_target": "EUR","date": "2023-12-20"}'
```

```bash
curl -i --request DELETE --location 'http://127.0.0.1:8000/rates/1' --header 'Content-Type: application/json' 
```

Retrieve historical data:

```bash
curl -i --request GET --location 'http://127.0.0.1:8000/rates/history/USD/EUR' --header 'Content-Type: application/json' 
```

Calculate rate for given pair at given date:

```bash
curl -i --request GET --location 'http://127.0.0.1:8000/rates/rate/USD/EUR/2020-12-01' --header 'Content-Type: application/json' 
```

```bash
curl -i --request GET --location 'http://127.0.0.1:8000/rates/rate/NZD/AUD/2020-12-01' --header 'Content-Type: application/json' 
```

```bash
curl -i --request GET --location 'http://127.0.0.1:8000/rates/rate/NZD/JPY/2020-12-01' --header 'Content-Type: application/json' 
```

```bash
curl -i --request GET --location 'http://127.0.0.1:8000/rates/rate/AUD/NZD/2020-12-01' --header 'Content-Type: application/json' 
```
