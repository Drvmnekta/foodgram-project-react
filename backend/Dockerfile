FROM python:3.7-slim

WORKDIR /app

COPY /foodgram/requirements.txt .

RUN pip install -r /app/foodgram/requirements.txt --no-cache-dir

COPY ./ ./

RUN python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py collectstatic && python3 manage.py load_ingredients

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000 
