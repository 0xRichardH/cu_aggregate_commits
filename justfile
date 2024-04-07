set shell := ["fish", "-c"]

export FLASK_APP := 'src/app.py'

venv:
  python3 -m venv venv && . venv/bin/activate.fish && pip install -r requirements.txt

run: venv
  flask run
