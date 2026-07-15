FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

COPY app.py .

ENV PYTHONBUFFERED = 1

RUN addgroup -g 10001 appgroup && \
    adduser -D -u 10001 -G appgroup appuser && \
    chown -R appuser:appgroup /app

USER 10001

EXPOSE 5000

CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]