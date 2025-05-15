import sys, os
import pandas as pd
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.load import save_to_csv, save_to_google_sheets, save_to_postgresql

sample_data = [
    {
        "title": "Test Product",
        "price": "1634440.0",
        "rating": "4.5",
        "colors": "2",
        "size": "M",
        "gender": "Unisex",
        "timestamp": "2025-05-10 12:00:00"
    }
]

def test_save_to_csv(tmp_path):
    filename = tmp_path / "test_output.csv"
    save_to_csv(sample_data, filename=filename)

    assert os.path.exists(filename)
    df = pd.read_csv(filename)
    assert not df.empty
    assert df.iloc[0]['title'] == "Test Product"

@patch('utils.load.Credentials')
@patch('utils.load.build')
def test_save_to_google_sheets(mock_build, mock_credentials):
    mock_service = MagicMock()
    mock_values = MagicMock()
    mock_service.spreadsheets.return_value.values.return_value.update.return_value.execute.return_value = {}
    mock_build.return_value = mock_service

    save_to_google_sheets(sample_data, service_account_file="fake_service_account.json")

    mock_credentials.from_service_account_file.assert_called_once()
    mock_build.assert_called_once_with('sheets', 'v4', credentials=mock_credentials.from_service_account_file.return_value)
    mock_service.spreadsheets.assert_called()

@patch('utils.load.create_engine')
def test_save_to_postgresql(mock_create_engine):
    mock_engine = MagicMock()
    mock_connection = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_connection
    mock_create_engine.return_value = mock_engine

    save_to_postgresql(sample_data, table_name='test_table')

    mock_create_engine.assert_called_once()
    assert mock_connection is not None
