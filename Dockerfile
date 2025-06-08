FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app

# Install system dependencies and Python dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    build-essential \
    python3-dev \
    wget \
    curl

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Expose port for Dash application
EXPOSE 8080

# Run the application
CMD ["python", "-m", "app.main", "--mode", "dashboard", "--port", "8080"]