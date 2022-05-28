FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY ./ ./

RUN python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py collectstatic && python3 manage.py load_ingredients

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000 
