# Menjalankan skrip
python main.py

# Menjalankan unit test pada folder tests
python -m pytest tests

# Menjalankan test coverage pada folder tests
pytest --cov=utils --cov-report=term-missing tests

# Notes
I deleted the google-sheets-api.json because it contain a secret key of my Google Console API Service. In this repository, you will also only find a load function to a CSV file, but actually I did load to 3 types of data repository.
