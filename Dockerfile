# Use a slim base image with Python and PyMuPDF support
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app (Python code + directories)
COPY . .

# Create output folder if it doesn't exist
RUN mkdir -p input output

# Default command: run the Python script
CMD ["python", "main.py"]
