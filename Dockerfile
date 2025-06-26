FROM python:3.10-slim

WORKDIR /app

# Копируем только зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение (включая serviceAccountKey.json, если он рядом)
COPY . .

# Делаем serviceAccountKey.json недоступным для чтения остальными, но доступным внутри
RUN chmod 600 serviceAccountKey.json || true

CMD ["python", "-u", "src/app.py"]
