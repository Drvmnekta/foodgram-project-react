FROM python:3.7-slim

WORKDIR /app

COPY /foodgram/requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY ./ ./

# RUN python3 /app/foodgram/manage.py makemigrations && python3 /app/foodgram/manage.py migrate && python3 /app/foodgram/manage.py collectstatic && python3 /app/foodgram/manage.py load_ingredients

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000 
