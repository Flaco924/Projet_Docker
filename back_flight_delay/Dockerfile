FROM python:3.10-slim

WORKDIR /app

# Install dependencies including PostgreSQL client for pg_isready
RUN apt-get update && apt-get install -y \
    libgomp1 \
    build-essential \
    libatlas-base-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy application code and requirements
COPY back_flight_delay /app
COPY requirements.txt /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make sure start.sh is executable
COPY back_flight_delay/start.sh /start.sh
RUN chmod +x /start.sh

# Run the custom entrypoint script
CMD ["/start.sh"]
