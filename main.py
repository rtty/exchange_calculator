import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DatabaseError

from api import currencies, rates
from config import engine
from db import models

# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# build urls
app.include_router(currencies.router)
app.include_router(rates.router)


# handle exceptions
@app.exception_handler(DatabaseError)
async def database_exception_handler(request: Request, exc: Exception):
    error_message = f'Database error occurred: {exc.args}'
    return JSONResponse(status_code=400, content={'message': error_message})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: Exception):
    error_message = ', '.join([f'{e["loc"][-1]} {e["msg"]}' for e in exc.errors()])
    return JSONResponse(status_code=400, content={'message': error_message})


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: Exception):
    error_message = f'{exc.detail}'
    return JSONResponse(status_code=exc.status_code, content={'message': error_message})


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    error_message = f'Unexpected error occurred: {exc}'
    return JSONResponse(status_code=500, content={'message': error_message})


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True, access_log=True)
