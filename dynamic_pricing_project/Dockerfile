FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE TRUE
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /dynamic_pricing/requirements.txt

# Set working directory
WORKDIR /dynamic_pricing

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl

# Copy project
COPY . /dynamic_pricing
RUN chmod +x /dynamic_pricing/entrypoint.sh

ENTRYPOINT /dynamic_pricing/entrypoint.sh
