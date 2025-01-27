# Use an official Python image as the base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1  # Prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED 1        # Ensure output is shown in real-time in logs

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    curl \
    cargo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Rust toolchain (required for Rust-based Python dependencies)
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y && \
    source $HOME/.cargo/env

# Create a working directory
WORKDIR /app

# Copy project files to the working directory
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Collect static files (if your project uses Django static files)
RUN python manage.py collectstatic --noinput

# Expose the port your app runs on (adjust this if needed)
EXPOSE 8000

# Command to start the Django application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project_name.wsgi:application"]
