import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import shutil
import os

@pytest.fixture(scope="session")
def test_data_path():
    """Fixture that provides the path to test data."""
    return Path(__file__).parent / 'test_data.csv'

@pytest.fixture(scope="session")
def test_output_dir():
    """Fixture that provides a temporary output directory."""
    output_dir = Path(__file__).parent / 'test_output'
    output_dir.mkdir(exist_ok=True)
    yield output_dir
    # Cleanup after tests
    if output_dir.exists():
        shutil.rmtree(output_dir)

@pytest.fixture(scope="session")
def sample_dataframe():
    """Fixture that provides a sample DataFrame."""
    return pd.DataFrame({
        'Date': pd.date_range(start='2025-01-01', periods=3),
        'Product': ['Product A', 'Product B', 'Product C'],
        'Category': ['Electronics', 'Furniture', 'Electronics'],
        'Price': [100.0, 200.0, 150.0],
        'Quantity': [2, 1, 3],
        'Customer_ID': [1001, 1002, 1003],
        'Region': ['North', 'South', 'East'],
        'Payment_Method': ['Credit Card', 'PayPal', 'Debit Card'],
        'Total_Amount': [200.0, 200.0, 450.0],
        'Discount': [0, 10, 20]
    })