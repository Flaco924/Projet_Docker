# Base image
FROM python:3.10-slim

# Create working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Default command
CMD ["streamlit", "run", "front_flight_delay/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
