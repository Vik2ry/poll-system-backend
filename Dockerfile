FROM python:3.10

# Create app directory (consistent with your compose file)
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy all files to /app (not /app/poll_sys)
COPY . .

# Set the working directory for the CMD
WORKDIR /app/poll_sys

EXPOSE 8000

RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
