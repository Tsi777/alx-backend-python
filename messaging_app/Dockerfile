# Use an official Python runtime as a slim base image
FROM python:3.10-slim

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set a working directory inside the container
WORKDIR /app

# Install system dependencies required for building some Python packages and MySQL client
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libssl-dev \
    libffi-dev \
    pkg-config \
  && rm -rf /var/lib/apt/lists/*


# Copy requirements.txt from the build context (current directory)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Create a non-root user and switch to it (for better security)
RUN useradd -m django_user
USER django_user

# Expose the port Django uses
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "-p", "8000", "0.0.0.0"]
