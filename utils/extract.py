import requests, time
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetch_page_content(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengambil {url}: {e}")
        return None

def extract_product_data(section):
    try:
        title = section.find(class_='product-title').text.strip()  # Mengambil data Title

        # Mengambil data Price
        price = None
        price_container = section.find('div', class_='price-container')
        if price_container:
            price_tag = price_container.find(class_='price')
        else:
            price_tag = section.find('p', class_='price')

        if price_tag:
            price = price_tag.text.strip()

        # Mengambil seluruh <p> detail
        details = section.find_all('p')

        # Mengambil data Rating
        rating = None
        for detail in details:
            if "Rating:" in detail.text:
                rating = detail.text.replace("Rating:", "").strip()
                break

        # Mengambil data lainnya berdasarkan urutan atau kata kunci
        colors = next((p.text.strip() for p in details if "Color" in p.text), None)
        size = next((p.text.strip() for p in details if "Size:" in p.text), None)
        gender = next((p.text.strip() for p in details if "Gender:" in p.text), None)

        # Menambahkan timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "title": title,
            "price": price,
            "rating": rating,
            "colors": colors,
            "size": size,
            "gender": gender,
            "timestamp": timestamp
        }

    except Exception as e:
        print(f"Error saat mengekstrak data produk: {e}")
        return None

def scrape_product_data(url, max_pages=50, delay=2):
    data = []

    for page_number in range(1, max_pages + 1):
        page_url = url if page_number == 1 else f"{url}page{page_number}"
        print(f"Scraping halaman {page_number}: {page_url}")

        try:
            content = fetch_page_content(page_url)
            if not content:
                break

            soup = BeautifulSoup(content, 'html.parser')
            product_sections = soup.find_all('div', class_='product-details')
            if not product_sections:
                break

            for section in product_sections:
                product_data = extract_product_data(section)
                if product_data:
                    data.append(product_data)

            time.sleep(delay)

        except Exception as e:
            print(f"Terjadi kesalahan di halaman {page_number}: {e}")
            break

    return data
