FROM python:3.7

LABEL authors="sergey.stavichenko@requestum.com"

# create app folder and set working directory
RUN mkdir -p /app
WORKDIR /app

# Add separate layers for dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# Copy all other files
COPY . .

# Add project root to PYTHONPATH env
ENV PYTHONPATH /app

CMD ["python", "-u", "/app/bin/server.py"]