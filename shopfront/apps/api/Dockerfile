FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

# Stage - 2

FROM gcr.io/distroless/python3-debian12:latest AS runtime

WORKDIR /app

COPY --from=builder /usr/lib/aarch64-linux-gnu/libpq.so* /usr/lib/aarch64-linux-gnu/ 2>/dev/null || \
COPY --from=builder /usr/lib/x86_64-linux-gnu/libpq.so* /usr/lib/x86_64-linux-gnu/

COPY --from=builder /root/.local /root/.local
COPY app.py .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/root/.local/lib/python3.11/site-packages
ENV PYTHONUNBUFFERED=1

USER 65532

EXPOSE 8000

ENTRYPOINT [ "/usr/bin/python3", "/app/app.py" ]