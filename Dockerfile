FROM python:3.9.5-slim-buster

ADD . ./app

WORKDIR /app

RUN pip install -r "requirements.txt"

EXPOSE 8500

CMD [ "python","app.py" ]