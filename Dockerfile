FROM python:3.11.10-alpine3.20 AS builder

WORKDIR /app

COPY . .

FROM python:3.11.10-alpine3.20

RUN apk add --no-cache --virtual .build-deps \  
    build-base \  
    libffi-dev \  
    openssl-dev \  
    curl \
    geos-dev \  
    gcc \
    && apk add --no-cache \  
    libpq 

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


WORKDIR /app

COPY --from=builder /app/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]