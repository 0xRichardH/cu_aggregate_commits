FROM python:3.12.2-slim-bullseye

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=src/app.py

EXPOSE 8000

CMD [ "python3", "-m" , "gunicorn", "-b", "0.0.0.0:8000", "src.app:app"]
