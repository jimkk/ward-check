# syntax=docker/dockerfile:1

FROM python:latest
# RUN apk add --no-cache make automake gcc g++ libc-dev python3-dev linux-headers git

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]