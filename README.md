Assuming you have Python installed, following steps should get you up and going.

The app currently works off of SQLite for simplicity and verification of functionality of the API calls without the need to setup a database to do so. Realistically would use a PostgreSQL database for long-term usage and scalability.

Instructions:
1. Install requirements with `pip install requirements.txt`
2. To start the app, run `python start.py`
3. Then from a seperate terminal, run `python test/api_tests.py` to see the API calls in action.

- API Tests script can be edited to make different calls.