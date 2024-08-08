FROM python:3.12.5-alpine
RUN apk update --no-cache && apk add --no-cache bash
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /mdcatalog
COPY requirements.txt .
RUN pip install pip --upgrade && pip install --no-cache-dir -r requirements.txt


# apk update && apk --no-cache add \
#     libressl-dev libffi-dev gcc musl-dev python3-dev openssl-dev cargo

# RUN pip install pip --upgrade && pip install --no-cache-dir -r requirements.txt \
#    && rm -rf /var/cache/apt/archives /var/lib/apt/lists/*
