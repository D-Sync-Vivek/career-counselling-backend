# Use slim Python image (NOT full python — too heavy)
FROM python:3.11-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (needed for psycopg2, torch, and ML packages)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
# Docker caches this step, so it won't re-download PyTorch every time you change app code!
COPY requirements.txt .

# Install dependencies (this will read the --extra-index-url flag automatically)
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI (Binding to 0.0.0.0 is required for Docker/Cloud deployments)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]