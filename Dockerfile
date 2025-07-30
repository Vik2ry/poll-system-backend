FROM python:3.10

# Set working dir
WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    pip install --upgrade pip

# Requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app files
COPY . .

# Copy build script & make executable
COPY poll_sys/build.sh /app/build.sh
RUN chmod +x /app/build.sh

# Working directory for script
WORKDIR /app/poll_sys

# Run the script as the container entrypoint
CMD ["../build.sh"]
