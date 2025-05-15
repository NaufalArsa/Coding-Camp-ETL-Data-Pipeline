# Menjalankan skrip
python main.py

# Menjalankan unit test pada folder tests
python -m pytest tests

# Menjalankan test coverage pada folder tests
pytest --cov=utils --cov-report=term-missing tests

# Url Google Sheets:
https://docs.google.com/spreadsheets/d/13FCXgeW79tELvuZfUH0088jxphVUnz2iX3r-5EJ43hc/edit?usp=sharing

# Notes
I deleted the google-sheetsh-api.json because it contain a secret key of my Google Console API Service. In this repository, you will also only find a load function to a CSV file, but actually I did load to 3 types of data repository.