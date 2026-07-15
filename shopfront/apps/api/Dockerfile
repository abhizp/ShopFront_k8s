# ==========================================
# Stage 1: Builder
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .

# Install dependencies into a dedicated target directory
# This eliminates broken symlinks and bypasses /root permission restrictions
RUN pip install --no-cache-dir --target=/app/pkgs -r requirements.txt

# ==========================================
# Stage 2: Runtime
# ==========================================
FROM gcr.io/distroless/python3-debian12:latest AS runtime

WORKDIR /app

# Copy compiled dependencies and explicitly grant ownership to user 65532
COPY --from=builder --chown=65532:65532 /app/pkgs /app/pkgs

# Copy application code with proper ownership
COPY --chown=65532:65532 app.py .

# Tell Python where to find the copied third-party packages
ENV PYTHONPATH=/app/pkgs
ENV PYTHONUNBUFFERED=1

# Run as Google Distroless's built-in non-root security user
USER 65532

EXPOSE 8000

# Execute using Distroless's native Python interpreter
ENTRYPOINT [ "/usr/bin/python3", "/app/app.py" ]