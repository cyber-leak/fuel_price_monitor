FROM python:3.11-slim

# Create app directory
WORKDIR /app

# Install OS packages and Python dependencies
COPY requirements.txt ./
RUN apt-get update \
		&& apt-get install -y --no-install-recommends procps \
		&& rm -rf /var/lib/apt/lists/* \
		&& pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Non-root user
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

ENV PYTHONUNBUFFERED=1

# Healthcheck: проверяет, что процесс с main.py запущен
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
	CMD pgrep -f main.py || exit 1

CMD ["python", "main.py"]
