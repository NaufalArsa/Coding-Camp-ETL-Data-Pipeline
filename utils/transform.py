import re

def convert_rating_to_float(data_list):
    for item in data_list:
        try:
            if isinstance(item['rating'], str):
                cleaned_rating = re.sub(r'[⭐\s/5]', '', item['rating']).strip()
                item['rating'] = float(cleaned_rating)
        except ValueError:
            item['rating'] = None
        except KeyError:
            print(f"Key 'rating' tidak ditemukan di item {item}")
    return data_list

def convert_price_to_rupiah(data_list, rate=16000):
    for item in data_list:
        try:
            if isinstance(item['price'], str) and item['price'].startswith('$'):
                usd_value = float(item['price'].replace('$', '').strip())
                item['price'] = float(usd_value * rate)
        except ValueError:
            item['price'] = None
        except KeyError:
            print(f"Key 'price' tidak ditemukan di item {item}")
    return data_list

def convert_colors_to_int(data_list):
    for item in data_list:
        try:
            if isinstance(item['colors'], str):
                match = re.search(r"\d+", item['colors'])
                item['colors'] = int(match.group()) if match else None
        except ValueError:
            item['colors'] = None
        except KeyError:
            print(f"Key 'colors' tidak ditemukan di item {item}")
    return data_list

def clean_size_and_gender(data_list):
    for item in data_list:
        try:
            if isinstance(item['size'], str):
                item['size'] = item['size'].replace("Size:", "").strip()
            if isinstance(item['gender'], str):
                item['gender'] = item['gender'].replace("Gender:", "").strip()
        except KeyError:
            print(f"Key 'size' atau 'gender' tidak ditemukan di item {item}")
    return data_list

dirty_patterns = {
    "title": ["Unknown Product"],
    "rating": ["Invalid Rating / 5", "Not Rated"],
    "price": ["Price Unavailable", None]
}

def remove_invalid_values(data_list):
    cleaned_data = []
    for item in data_list:
        try:
            if not isinstance(item, dict):
                continue
            valid = True
            for key, invalid_values in dirty_patterns.items():
                if item.get(key) in invalid_values:
                    valid = False
                    break
            if valid:
                cleaned_data.append(item)
        except Exception as e:
            print(f"Error saat menghapus nilai yang tidak valid: {e}")
    return cleaned_data

def remove_duplicates(data_list):
    seen = set()
    cleaned = []
    for item in data_list:
        try:
            identifier = (item['title'], item['price'], item['rating']) 
            if identifier not in seen:
                seen.add(identifier)
                cleaned.append(item)
        except KeyError:
            print(f"Key 'title', 'price', atau 'rating' tidak ditemukan di item {item}")
    return cleaned

def remove_nulls(data_list):
    cleaned_data = []
    for item in data_list:
        try:
            if all(value is not None and value != "" for value in item.values()):
                cleaned_data.append(item)
        except Exception as e:
            print(f"Error saat menghapus data null: {e}")
    return cleaned_data


def transform_data(data_list):
    try:
        data_list = remove_invalid_values(data_list)
        data_list = remove_nulls(data_list)
        data_list = remove_duplicates(data_list)
        data_list = convert_price_to_rupiah(data_list)
        data_list = convert_rating_to_float(data_list)
        data_list = convert_colors_to_int(data_list)
        data_list = clean_size_and_gender(data_list)
        data_list = remove_nulls(data_list)
    except Exception as e:
        print(f"Error saat mentransformasi data: {e}")
    return data_list