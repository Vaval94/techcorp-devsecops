# Image de base officielle. Amélioration possible : figer par digest (@sha256:...).
FROM python:3.11-slim

# Correctifs de sécurité du système de base (réduit les CVE corrigées non appliquées)
RUN apt-get update \
 && apt-get upgrade -y --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app/requirements.txt .
# pip à jour ; setuptools/wheel inutiles à l'exécution et souvent signalés par Trivy
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && pip uninstall -y setuptools wheel || true

COPY app ./app
RUN useradd -r -u 10001 appuser
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health',timeout=2).status==200 else 1)"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
