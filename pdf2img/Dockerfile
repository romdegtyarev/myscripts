# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install dependencies for pdf2image (poppler)
RUN apt-get update && apt-get install -y poppler-utils && rm -rf /var/lib/apt/lists/*

# Copy project files into the container
COPY requirements.txt .
COPY main.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run the script
ENTRYPOINT ["python", "/app/main.py"]
