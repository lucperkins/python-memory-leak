FROM python:3.9.6-slim-buster

# Install OS-level packages
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get upgrade --yes && \
    apt-get install --yes build-essential libpq-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Build C extension
RUN (cd hello && python setup.py build && python setup.py install)

EXPOSE 8080

ENTRYPOINT ["ddtrace-run"]
CMD ["flask", "run", "--port=8080", "--host=0.0.0.0"]