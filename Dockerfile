FROM python:3.10-slim

# Setup working directory
WORKDIR /app

# Copy requirements and put them under root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-privileged user
RUN addgroup --system app \
 && adduser  --system --ingroup app app

# Copy everything (code and keys)
COPY . .

# Secure the key
RUN chmod 600 serviceAccountKey.json || true \
 && chown -R app:app /app 

# Switch to non-privileged user
USER app

# Export PYTHONPATH so that 'import src...' can work
ENV PYTHONPATH=/app

# Entrypoint
CMD ["python", "-u", "src/app.py"]
