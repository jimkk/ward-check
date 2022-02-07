# syntax=docker/dockerfile:1

FROM python:3.10.2-alpine
RUN apk add --no-cache make automake gcc g++ libc-dev python3-dev linux-headers git

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py .

CMD ["python", "bot.py"]