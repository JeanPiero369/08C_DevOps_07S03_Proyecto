FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt main.py router.py schemas.py __init__.py ./
COPY controllers ./controllers
COPY utils ./utils

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
