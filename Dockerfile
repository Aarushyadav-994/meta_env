FROM python:3.9-slim

WORKDIR /app

COPY environment.py inference.py openenv.yaml requirements.txt README.md /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app
ENV PORT=8000
EXPOSE 8000

CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8000"]
