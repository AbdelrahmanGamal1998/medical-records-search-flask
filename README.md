# Medical Records Search (Flask)

[![Tests](https://github.com/AbdelrahmanGamal1998/medical-records-search-flask/actions/workflows/tests.yml/badge.svg)](https://github.com/AbdelrahmanGamal1998/medical-records-search-flask/actions/workflows/tests.yml)

A small Flask web page that looks up a patient's health record. You enter the patient ID and either a date or an
accident type, and the page shows the patient's details, the matching health record and their medical history.
It started as a university workshop project for a software testing course (2021) and was cleaned up so that it
runs, and is tested, without any outside service.

## Run it

You need Python 3.9 or newer.

```bash
git clone https://github.com/AbdelrahmanGamal1998/medical-records-search-flask.git
cd medical-records-search-flask
pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000>. The app starts with three sample records, so you can try it right away:

| ID | Date         | Accident type   |
| -- | ------------ | --------------- |
| 1  | `2020-12-25` | `Car Accident`  |
| 1  | `2010-11-25` | `Train Accident`|
| 2  | `2011-11-25` | `Bus Accident`  |

## Use a real database (optional)

The records can also come from a Firebase Firestore collection named `HealthRecord`. Install the extra package and
point `FIREBASE_CREDENTIALS` at your service account key file:

```bash
pip install -r requirements-firebase.txt
FIREBASE_CREDENTIALS=path/to/serviceAccountKey.json python app.py
```

Never commit that key file.

## Tests

```bash
python -m unittest discover -s tests -v
```

The 15 tests cover the form helpers, the searches, and the web page itself (found by date, found by accident
type, missing ID, missing date and accident, missing search option, unknown patient).

## Project structure

```
app.py          the Flask app and the form and search helper functions
records.py      where records come from: in-memory sample data, or Firestore
templates/      the search form and the patient card
static/         the stylesheet
tests/          unit tests and web page tests
```

## Notes

- Changes made when the project was cleaned up: the search code now takes a record store, so the tests no longer
  need a live Firebase database (before, the database tests could not pass without one); the two routes for `/` were
  merged; the helper functions were renamed to Python style; and a non-numeric ID or a missing search option now
  returns a message instead of crashing.
- The sample data is made up.

## License

[MIT](LICENSE)