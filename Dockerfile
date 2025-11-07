# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Define environment variable for the database path and set a default
ENV DATABASE_PATH /data/ollama_hosts.db

# Run the database schema migration to ensure the db is created in the volume
RUN python database.py

# Make port 5000 available to the world outside this container
EXPOSE 5000

# The command to run the application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "provider-service:app"]
