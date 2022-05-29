FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY ./ ./

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000 

RUN python3 /app/manage.py makemigrations && python3 /app/manage.py migrate && python3 /app/manage.py collectstatic && python3 /app/manage.py load_ingredients
