FROM python:3.11

WORKDIR /code

COPY ./src/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src/main /code/main

CMD ["uvicorn", "main.server.fastapi_config:app", "--host", "0.0.0.0", "--port", "80"]
