FROM python:3.12.0-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

WORKDIR /app

CMD [ "python", "main.py" ]