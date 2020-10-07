FROM python:3.6.9

WORKDIR /code
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
COPY . /code
CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
