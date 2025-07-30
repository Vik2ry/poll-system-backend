FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc \
    && pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/poll_sys

EXPOSE 8000

# Use build.sh as the container entrypoint script
CMD ["../build.sh"]
