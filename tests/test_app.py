import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import (  # noqa: E402
    MUST_CHOOSE_OPTION,
    MUST_ENTER_DATE_OR_ACCIDENT,
    MUST_ENTER_ID,
    NOT_FOUND,
    check_inputs,
    create_app,
    get_accident,
    get_date,
    get_id,
    get_search_option,
    search_by_accident,
    search_by_date,
)
from records import SAMPLE_RECORDS, InMemoryRecordStore  # noqa: E402

JOHN_2020 = SAMPLE_RECORDS[0]
JOHN_2010 = SAMPLE_RECORDS[2]


class FormHelpersTest(unittest.TestCase):
    def test_get_id_reads_a_number(self):
        self.assertEqual(get_id({"id": "1"}), 1)

    def test_get_id_is_none_when_empty_or_not_a_number(self):
        self.assertIsNone(get_id({"id": ""}))
        self.assertIsNone(get_id({"id": "abc"}))
        self.assertIsNone(get_id({}))

    def test_get_date_and_accident(self):
        form = {"date": "2010-11-25", "Accident": "Car Accident"}
        self.assertEqual(get_date(form), "2010-11-25")
        self.assertEqual(get_accident(form), "Car Accident")

    def test_get_search_option(self):
        self.assertEqual(get_search_option({"searchoption": "accidenttype"}), "accidenttype")
        self.assertIsNone(get_search_option({}))

    def test_check_inputs(self):
        self.assertEqual(check_inputs(None, "", ""), MUST_ENTER_ID)
        self.assertEqual(check_inputs(1, "", ""), MUST_ENTER_DATE_OR_ACCIDENT)
        self.assertIsNone(check_inputs(1, "2020-12-25", ""))
        self.assertIsNone(check_inputs(1, "", "Car Accident"))


class SearchTest(unittest.TestCase):
    def setUp(self):
        self.store = InMemoryRecordStore()

    def test_search_by_date(self):
        self.assertEqual(search_by_date(self.store, 1, "2020-12-25"), [JOHN_2020])
        self.assertEqual(search_by_date(self.store, 1, "2010-11-25"), [JOHN_2010])

    def test_search_by_accident(self):
        self.assertEqual(search_by_accident(self.store, 1, "Car Accident"), [JOHN_2020])
        self.assertEqual(search_by_accident(self.store, 1, "Train Accident"), [JOHN_2010])

    def test_nothing_found_for_the_wrong_patient(self):
        self.assertEqual(search_by_date(self.store, 2, "2020-12-25"), [])


class WebPageTest(unittest.TestCase):
    def setUp(self):
        self.client = create_app(InMemoryRecordStore()).test_client()

    def post(self, **form):
        return self.client.post("/", data=form).get_data(as_text=True)

    def test_the_search_form_is_shown(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Search Option", response.get_data(as_text=True))

    def test_a_record_is_found_by_date(self):
        page = self.post(id="1", date="2020-12-25", Accident="", searchoption="date")
        self.assertIn("Patient Info", page)
        self.assertIn("John", page)
        self.assertIn("magdy", page)

    def test_a_record_is_found_by_accident_type(self):
        page = self.post(id="1", date="", Accident="Train Accident", searchoption="accidenttype")
        self.assertIn("Hanan", page)

    def test_a_missing_id_is_rejected(self):
        self.assertEqual(self.post(id="", date="2020-12-25", Accident="", searchoption="date"), MUST_ENTER_ID)

    def test_date_or_accident_is_required(self):
        self.assertEqual(
            self.post(id="1", date="", Accident="", searchoption="date"), MUST_ENTER_DATE_OR_ACCIDENT
        )

    def test_a_search_option_is_required(self):
        self.assertEqual(self.post(id="1", date="2020-12-25", Accident=""), MUST_CHOOSE_OPTION)

    def test_an_unknown_patient_is_reported(self):
        self.assertEqual(self.post(id="99", date="2020-12-25", Accident="", searchoption="date"), NOT_FOUND)


if __name__ == "__main__":
    unittest.main()