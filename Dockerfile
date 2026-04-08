FROM python:3.11-slim

WORKDIR /app

COPY __init__.py client.py environment.py inference.py models.py openenv.yaml pyproject.toml README.md requirements.txt uv.lock /app/
COPY graders /app/graders
COPY server /app/server
COPY tasks /app/tasks

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn inference:app --host 0.0.0.0 --port ${PORT:-8000}"]
