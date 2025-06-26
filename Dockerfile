FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod 600 serviceAccountKey.json || true

# Добавляем /app в PYTHONPATH, чтобы 'import src.…' работал
ENV PYTHONPATH=/app

CMD ["python", "-u", "src/app.py"]
