from utils.extract import scrape_product_data
from utils.transform import transform_data
from utils.load import save_to_csv
import pandas as pd

url = 'https://fashion-studio.dicoding.dev/'

# Data Scraping
product_data = scrape_product_data(url)
 
if product_data:
    # DataFrame sebelum transformasi
    df_raw = pd.DataFrame(product_data)
    print("🟡 DataFrame Sebelum Transformasi:")
    print(df_raw)

    # Transformasi data
    cleaned_data = transform_data(product_data)

    # DataFrame setelah transformasi
    df_cleaned = pd.DataFrame(cleaned_data)
    print("\n🟢 DataFrame Setelah Transformasi:")
    print(df_cleaned)

    # Simpan ke CSV
    save_to_csv(df_cleaned, 'products.csv')

else:
    print("Tidak ada data yang ditemukan.")