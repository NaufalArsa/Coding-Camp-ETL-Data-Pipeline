from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine
import pandas as pd

# Nenyimpan file ke CSV
def save_to_csv(data_list, filename='products.csv'):
    try:
        df = pd.DataFrame(data_list)
        df.to_csv(filename, index=False)
        print(f"Data berhasil disimpan ke file CSV: {filename}")
    except Exception as e:
        print(f"Gagal menyimpan ke CSV: {e}")
