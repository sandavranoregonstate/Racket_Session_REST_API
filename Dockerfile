# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for psycopg2 if you're using PostgreSQL
# RUN apt-get update \
#    && apt-get install -y --no-install-recommends libpq-dev \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/*

# Install pip dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the current directory contents into the container
COPY . /app/

EXPOSE 8000

# Specify the command to run on container start using Django's built-in server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
