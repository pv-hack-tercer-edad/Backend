# Use an official Python image as the base
FROM --platform=linux/amd64 python:3.11-slim

# Set the working directory
WORKDIR /app

# Set PYTHONUNBUFFERED to 1 to ensure output is displayed immediately
ENV PYTHONUNBUFFERED=1

# Copy the requirements file
COPY requirements.prod.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.prod.txt

# Copy the application code
COPY ./src /app/src

# Run the application
CMD ["fastapi", "run", "src/main.py", "--port", "80", "--host", "0.0.0.0"]
