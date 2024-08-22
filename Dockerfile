# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY requirements.txt .
COPY main.py .
COPY .env .
RUN chmod +x /app/main.py

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run the application
CMD ["python", "main.py"]

