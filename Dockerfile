FROM python:3.11.7-alpine3.18
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["gunicorn"  , "-b", "0.0.0.0:8800", "app:app"]