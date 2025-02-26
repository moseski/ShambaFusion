# Use the official Python image from the Docker Hub
FROM python:3.10-slim


# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir --verbose -r requirements.txt/

# #DB pg_service.conf
# ENV PGSERVICE=my_service
# COPY pg_service.conf /pg_service.conf


# Copy the rest of the application code into the container
COPY . .

# Expose the port on which the app will run
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# #dockerize
# RUN apk add --no-cache curl \
#     && curl -sSL https://github.com/jwilder/dockerize/releases/latest/download/dockerize-alpine-linux-amd64 -o /usr/local/bin/dockerize \
#     && chmod +x /usr/local/bin/dockerize
# FROM debian:bookworm

# Update package list and install packages
# RUN apt-get update && apt-get install -y \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# RUN curl -sSL https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz | tar -xz -C /usr/local/bin


# sudo docker run -p 8000:8000 shambaFusion  ==> run with this command
