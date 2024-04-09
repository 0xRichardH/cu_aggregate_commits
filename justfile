set shell := ["fish", "-c"]

set dotenv-load

export FLASK_APP := 'src/app.py'

venv:
  python3 -m venv venv && . venv/bin/activate.fish && pip install -r requirements.txt

run: venv
  flask run

fetch: venv
  python src/fetch.py

db: venv
  flask --app src/fetch.py db init
