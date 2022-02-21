FROM python:3.10-slim AS builder

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
RUN mkdir /app/data

WORKDIR /app

COPY requirements.txt .

ENV PYTHONDONTWRITEBYTECODE 1

RUN python3 -m pip install --user --no-cache-dir --upgrade \
    pip \
    setuptools \
    wheel

RUN python3 -m pip install --user --no-cache-dir \
    -r requirements.txt

FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY kosync.py .

EXPOSE 8081

VOLUME ["/app/data"]

ENV PATH=/root/.local/bin:$PATH

CMD ["uvicorn", "kosync:app", "--host", "0.0.0.0", "--port", "8081"]
