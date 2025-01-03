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
RUN mkdir -p /data/db


# Start MongoDB and expose the port
EXPOSE 27017
CMD ["mongod", "--bind_ip_all"]

# Set the working directory
WORKDIR /workspace

# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy project files
COPY . /workspace

# Start MongoDB service when the container runs
# CMD ["bash", "-c", "mongod --bind_ip_all & exec bash"]

# Copy project files into the container
# COPY . .

# Install Python dependencies from requirements.txt if it exists
# RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Install additional Python dependencies if not included in requirements.txt
# RUN pip install \
#     notebook==7.0.7 \
#     pandas==2.0.3 \
#     pyarrow==15.0.0 \
#     seaborn==0.13.2 \
#     sweetviz==2.3.1 \
#     pyodbc==5.2.0 \
#     SQLAlchemy==2.0.36

# Set default command
# CMD ["bash"]

