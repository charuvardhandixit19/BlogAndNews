# Use an official Python image
FROM python:3.12-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    curl \
    && apt-get clean

# Install Rust toolchain (required by maturin)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal --default-toolchain stable && \
    export PATH="$HOME/.cargo/bin:$PATH"

# Set environment variables
ENV PATH="/root/.cargo/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Run the application using Gunicorn
CMD ["gunicorn", "blogs_news_project.wsgi:application", "--bind", "0.0.0.0:8000"]
