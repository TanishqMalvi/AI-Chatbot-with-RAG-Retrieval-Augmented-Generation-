FROM python:3.11-slim

# Security: run as non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpoppler-cpp-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Pre-download HuggingFace embedding model
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer(\"sentence-transformers/all-MiniLM-L6-v2\")"
RUN python -c "from sentence_transformers import CrossEncoder; CrossEncoder(\"BAAI/bge-reranker-large\")"

# Download spaCy model at build time (avoid runtime download)
RUN python -m spacy download en_core_web_lg

# Copy application code
COPY app/ ./app/
COPY data/ ./data/
COPY eval/ ./eval/
COPY pyproject.toml .

# Set ownership
RUN mkdir -p /home/appuser/.cache/huggingface && chown -R appuser:appuser /app /home/appuser

USER appuser

# Expose FastAPI port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]