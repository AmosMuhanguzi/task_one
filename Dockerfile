FROM python:3.8-slim-buster

WORKDIR /app

COPY app.py /app/

RUN pip install Flask

EXPOSE 5000

CMD ["python", "app.py"]