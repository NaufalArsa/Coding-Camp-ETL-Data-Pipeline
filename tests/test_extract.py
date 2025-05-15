from bs4 import BeautifulSoup
import requests
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.extract import fetch_page_content, extract_product_data, scrape_product_data

# Test untuk fetch_page_content
def test_fetch_page_content_success(monkeypatch):
    class MockResponse:
        status_code = 200
        content = b"<html></html>"

        def raise_for_status(self):
            pass

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    url = "https://example.com"
    content = fetch_page_content(url)
    assert content == b"<html></html>"

def test_fetch_page_content_error(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.RequestException("Failed request")

    monkeypatch.setattr(requests, "get", mock_get)

    url = "https://example.com"
    content = fetch_page_content(url)
    assert content is None

# Test untuk extract_product_data
def test_extract_product_data_complete():
    html = '''
    <div class="product-details">
        <div class="product-title">Cool Shirt</div>
        <div class="price-container"><span class="price">$19.99</span></div>
        <p>Rating: 4.5</p>
        <p>2 Colors</p>
        <p>Size: M</p>
        <p>Gender: Unisex</p>
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    section = soup.find('div', class_='product-details')
    result = extract_product_data(section)
    
    assert result["title"] == "Cool Shirt"
    assert result["price"] == "$19.99"
    assert result["rating"] == "4.5"
    assert result["colors"] == "2 Colors"
    assert result["size"] == "Size: M"
    assert result["gender"] == "Gender: Unisex"
    assert "timestamp" in result

def test_extract_product_data_missing_fields():
    html = '''
    <div class="product-details">
        <div class="product-title">Simple Item</div>
        <div class="price-container"><span class="price">$10</span></div>
        <p>Rating: 5</p>
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    section = soup.find('div', class_='product-details')
    result = extract_product_data(section)

    assert result["title"] == "Simple Item"
    assert result["price"] == "$10"
    assert result["rating"] == "5"
    assert result["colors"] is None
    assert result["size"] is None
    assert result["gender"] is None

def test_extract_product_data_invalid_section():
    html = '<div class="product-details"><p>No title or price</p></div>'
    soup = BeautifulSoup(html, 'html.parser')
    section = soup.find('div', class_='product-details')
    result = extract_product_data(section)
    assert result is None

# Test untuk scrape_product_data
def test_scrape_product_data(monkeypatch):
    sample_html = '''
    <div class="product-details">
        <div class="product-title">Test Product</div>
        <div class="price-container"><span class="price">$99.99</span></div>
        <p>Rating: 4.0</p>
        <p>Black</p>
        <p>L</p>
        <p>Men</p>
    </div>
    '''

    class MockResponse:
        status_code = 200
        content = sample_html.encode("utf-8")

        def raise_for_status(self):
            pass

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    result = scrape_product_data("https://fashion-studio.dicoding.dev", max_pages=2, delay=0)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["title"] == "Test Product"
    assert result[1]["title"] == "Test Product"
