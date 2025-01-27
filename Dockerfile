# Use an official Python image
FROM python:3.12-slim

# Install Rust dependencies and build tools (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    curl \
    python3-dev \
    rustc \
    cargo \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy the application files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Start Gunicorn server
CMD ["gunicorn", "blogs_news_project.wsgi:application", "--bind", "0.0.0.0:8000"]
