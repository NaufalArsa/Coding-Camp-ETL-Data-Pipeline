import pytest, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.transform import (
    convert_rating_to_float,
    convert_price_to_rupiah,
    convert_colors_to_int,
    clean_size_and_gender,
    remove_invalid_values,
    remove_duplicates,
    remove_nulls,
    transform_data
)

@pytest.fixture
def sample_data():
    return [
        {
            "title": "T-shirt 2",
            "price": "$10.00",
            "rating": "Not Rated",
            "colors": "3 colors",
            "size": "Size: M",
            "timestamp": "2025-05-10"
        },
        {
            "title": "T-shirt 60",
            "price": "$10.00",
            "rating": "⭐ 4.5 / 5",
            "colors": "3 colors",
            "size": "Size: M",
            "gender": "Gender: Unisex",
            "timestamp": "2025-05-10"
        },
        {
            "title": "Unknown Product",
            "price": "Price Unavailable",
            "rating": "⭐ 3.0 / 5",
            "colors": "5 colors",
            "gender": "Gender: Male",
            "timestamp": "2025-05-10"
        },
        {
            "title": "T-shirt 60",
            "price": "$10.00",
            "rating": "⭐ 4.5 / 5",
            "colors": "4 colors",
            "size": "Size: M",
            "gender": "Gender: Unisex",
            "timestamp": "2025-05-10"
        },
        {
            "title": "T-shirt 30",
            "price": "$10.00",
            "colors": "3 colors",
            "size": None,
            "gender": None,
            "timestamp": "2025-05-10"
        }
        
    ]

def test_convert_rating_to_float(sample_data):
    result = convert_rating_to_float(sample_data.copy())
    assert isinstance(result[2]['rating'], float)
    assert result[2]['rating'] == 3.0

def test_convert_price_to_rupiah(sample_data):
    result = convert_price_to_rupiah(sample_data.copy(), rate=16000)
    assert isinstance(result[0]['price'], float)
    assert result[0]['price'] == 160000.0

def test_convert_colors_to_int(sample_data):
    result = convert_colors_to_int(sample_data.copy())
    assert isinstance(result[0]['colors'], int)
    assert result[0]['colors'] == 3

def test_clean_size_and_gender(sample_data):
    result = clean_size_and_gender(sample_data.copy())
    assert result[1]['size'] == "M"
    assert result[1]['gender'] == "Unisex"

def test_remove_invalid_values(sample_data):
    result = remove_invalid_values(sample_data.copy())
    assert len(result) == 3 

def test_remove_duplicates(sample_data):
    filtered = remove_invalid_values(sample_data.copy())
    result = remove_duplicates(filtered)
    assert len(result) == 1

def test_remove_nulls(sample_data):
    filtered = remove_invalid_values(sample_data.copy())
    cleaned = remove_duplicates(filtered)
    result = remove_nulls(cleaned)
    assert len(result) == 1
    assert result[0]['title'] == "T-shirt 60"

def test_transform_data(sample_data):
    transformed = transform_data(sample_data.copy())
    assert isinstance(transformed, list)
    assert len(transformed) == 1
    item = transformed[0]
    assert isinstance(item['price'], float)
    assert isinstance(item['rating'], float)
    assert isinstance(item['colors'], int)
    assert item['size'] == 'M'
    assert item['gender'] == 'Unisex'
