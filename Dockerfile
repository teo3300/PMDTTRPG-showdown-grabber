# Base python image
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install requirements (add gnuicorn)
RUN pip install --no-cache-dir -r requirements.txt

# Copy content of folder
COPY . .

# Expose port
EXPOSE 8000

# Start
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "serv:app"]
