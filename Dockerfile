FROM python:3.9-slim

WORKDIR /app

COPY environment.py metadata.json requirements.txt README.md /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

CMD ["python", "-c", "from environment import SimpleReachEnv; env = SimpleReachEnv(); obs, info = env.reset(); print({'observation': obs.tolist(), 'info': info})"]
