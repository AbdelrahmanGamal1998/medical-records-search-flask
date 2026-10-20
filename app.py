"""A small web page to look up a patient's health record by ID and either date or accident type."""
from flask import Flask, render_template, request

from records import default_store

MUST_ENTER_ID = "User Must Enter ID"
MUST_ENTER_DATE_OR_ACCIDENT = "You Must Enter Date or Accident"
MUST_CHOOSE_OPTION = "must choose search option"
NOT_FOUND = "user not found"


def get_id(form):
    """The patient ID as a number, or None when it is empty or not a number."""
    try:
        return int(form.get("id", ""))
    except ValueError:
        return None


def get_date(form):
    return str(form.get("date", ""))


def get_accident(form):
    return str(form.get("Accident", ""))


def get_search_option(form):
    return form.get("searchoption")


def check_inputs(record_id, date, accident):
    """An error message when the form is incomplete, otherwise None."""
    if record_id is None:
        return MUST_ENTER_ID
    if date == "" and accident == "":
        return MUST_ENTER_DATE_OR_ACCIDENT
    return None


def search_by_date(store, record_id, date):
    return store.find(id=record_id, Date=date)


def search_by_accident(store, record_id, accident):
    return store.find(id=record_id, Accident=accident)


def create_app(store=None):
    app = Flask(__name__)
    record_store = store if store is not None else default_store()

    @app.route("/", methods=["GET", "POST"])
    def search():
        if request.method == "GET":
            return render_template("searchForm.html")

        form = request.form
        record_id, date, accident = get_id(form), get_date(form), get_accident(form)
        problem = check_inputs(record_id, date, accident)
        if problem:
            return problem

        option = get_search_option(form)
        if option == "date":
            records = search_by_date(record_store, record_id, date)
        elif option == "accidenttype":
            records = search_by_accident(record_store, record_id, accident)
        else:
            return MUST_CHOOSE_OPTION

        if not records:
            return NOT_FOUND
        first = records[0]
        return render_template(
            "card.html",
            HealthRecords=records,
            name=first["name"],
            age=first["age"],
            address=first["address"],
            phone=first["Phone"],
            height=first["height"],
            weight=first["weight"],
        )

    return app


if __name__ == "__main__":
    create_app().run(debug=True)