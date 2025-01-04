# Use the Python 3.11 image with useful data libraries
FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# Set working directory
WORKDIR /workspace

# Import the public key used by the package management system
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-6.0.gpg

# Create a list file for MongoDB
RUN echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/debian bullseye/mongodb-org/6.0 main" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Update the repository and install MongoDB
RUN apt-get update && apt-get install -y mongodb-org && rm -rf /var/lib/apt/lists/*

# Ensure MongoDB data directory exists
RUN mkdir -p /data/db /var/lib/mongodb && chown -R mongodb:mongodb /data/db /var/lib/mongodb

# Start MongoDB during the build process to avoid errors on first run
RUN mongod --dbpath /var/lib/mongodb --fork --logpath /var/log/mongodb.log || echo "MongoDB already running"

# Expose MongoDB port
EXPOSE 27017

# Set the working directory
WORKDIR /workspace

# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy project files
COPY . /workspace

# Start MongoDB in the background and keep the container alive with bash
CMD ["bash", "-c", "mongod --dbpath /var/lib/mongodb --fork --logpath /var/log/mongodb.log && python manage.py runserver 0.0.0.0:8000"]
