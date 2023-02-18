# Use an official Python image as the base image
FROM python:3.11.0a1-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=service_company_meters.settings
ENV PYTHONUNBUFFERED=1

# Expose port 8000 for the Django development server
EXPOSE 8000




