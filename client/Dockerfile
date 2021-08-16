FROM python:3.9.6-slim-buster

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "client.py"]