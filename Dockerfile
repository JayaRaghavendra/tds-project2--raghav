# Use an official Python base image (Debian-based)
FROM python:3.12-slim

# Install essential system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    ca-certificates \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js via NodeSource setup
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install Prettier globally so it is available in the container
RUN npm install -g prettier@3.4.2

# Set the working directory
WORKDIR /app

# Copy the entire project into /app, preserving the project structure
COPY . /app

# Install Python dependencies using the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your FastAPI app listens on
EXPOSE 8000

# Set the default command to run your FastAPI app via uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]