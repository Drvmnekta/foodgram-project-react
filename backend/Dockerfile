FROM python:3.7-slim

COPY ./ /app

WORKDIR /app

COPY backend/foodgram/requirements.txt pwd

RUN pip3 install --upgrade pip && pip3 install -r /app/backend/requirements.txt --no-cache-dir

RUN python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py collectstatic

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000 