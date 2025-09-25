FROM python:3.11-slim

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# set work directory
WORKDIR /usr/src/app

# Install system dependencies for psycopg2 and general builds
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN python3 -m pip install --upgrade pip
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project source
COPY . .

# Expose port
EXPOSE 8001

# Default command: run migrations + start server
CMD ["sh", "-c", "python manage.py migrate && gunicorn project.wsgi:application --bind 0.0.0.0:8000"]