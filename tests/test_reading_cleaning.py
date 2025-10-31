import pytest
import pandas as pd
from pathlib import Path
from src.reading_cleaning import DataCleaner

def test_data_cleaner_initialization(test_data_path):
    """Test DataCleaner initialization."""
    cleaner = DataCleaner(test_data_path)
    assert isinstance(cleaner, DataCleaner)
    assert cleaner.input_path == Path(test_data_path)
    assert cleaner.data is None

def test_read_data(test_data_path):
    """Test reading data from CSV."""
    cleaner = DataCleaner(test_data_path)
    data = cleaner.read_data()
    
    assert isinstance(data, pd.DataFrame)
    assert not data.empty
    assert 'Date' in data.columns
    assert 'Product' in data.columns

def test_clean_data(test_data_path):
    """Test data cleaning functionality."""
    cleaner = DataCleaner(test_data_path)
    cleaner.read_data()
    cleaned_data = cleaner.clean_data()
    
    # Check if date is converted to datetime
    assert pd.api.types.is_datetime64_any_dtype(cleaned_data['Date'])
    
    # Check if numeric columns are properly typed
    assert pd.api.types.is_numeric_dtype(cleaned_data['Price'])
    assert pd.api.types.is_numeric_dtype(cleaned_data['Quantity'])
    assert pd.api.types.is_numeric_dtype(cleaned_data['Total_Amount'])
    
    # Check for no negative values in numeric columns
    assert (cleaned_data['Price'] >= 0).all()
    assert (cleaned_data['Quantity'] >= 0).all()
    assert (cleaned_data['Total_Amount'] >= 0).all()

def test_save_data(test_data_path, test_output_dir):
    """Test saving cleaned data."""
    cleaner = DataCleaner(test_data_path)
    cleaner.read_data()
    cleaner.clean_data()
    
    # Test CSV saving
    csv_path = test_output_dir / 'test_cleaned.csv'
    cleaner.save_data(csv_path)
    assert csv_path.exists()
    
    # Test Excel saving
    excel_path = test_output_dir / 'test_cleaned.xlsx'
    cleaner.save_data(excel_path, format='xlsx')
    assert excel_path.exists()

def test_invalid_file_format(test_data_path):
    """Test handling of invalid file formats."""
    cleaner = DataCleaner(test_data_path)
    cleaner.read_data()
    cleaner.clean_data()
    
    with pytest.raises(ValueError):
        cleaner.save_data('invalid.txt', format='txt')