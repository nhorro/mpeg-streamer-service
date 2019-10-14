FROM continuumio/miniconda3

RUN pip install Flask pyzmq

COPY app /app

WORKDIR /app

EXPOSE 5000

CMD python3 app.py