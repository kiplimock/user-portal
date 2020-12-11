FROM python:3.7-alpine
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
COPY requirements.txt requirements.txt
RUN  pip install -r requirements.txt
ENV FLASK_ENV="docker"
EXPOSE 5000
ADD . .
CMD [ "python","app.py" ]