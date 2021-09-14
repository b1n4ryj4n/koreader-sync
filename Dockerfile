FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
RUN mkdir /app/data

WORKDIR /app

COPY requirements.txt .

RUN python3.9 -m pip install --no-cache-dir --upgrade \
    pip \
    setuptools \
    wheel

RUN python3.9 -m pip install --no-cache-dir \
    -r requirements.txt

COPY koreader-flask.py .

EXPOSE 8081

VOLUME ["/app/data"]

CMD ["python3.9", "koreader-flask.py"]
