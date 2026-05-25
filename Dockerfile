# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for data processing and building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code, models, and data folders into the container
COPY src/ ./src/
COPY models/ ./models/
COPY data/ ./data/

# Set environment variables for the application
ENV PYTHONPATH=/app
ENV ML_MODEL_PATH="/app/models/phishing_risk_model.joblib"

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Run the application with Uvicorn
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
