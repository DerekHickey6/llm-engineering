# Base Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src/ folder
COPY src/ .

# Expose to the right port
EXPOSE 8000

# Run the Uvicorn server
CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "8000"]