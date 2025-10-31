import pytest
import pandas as pd
import numpy as np
from src.regression_analysis import SalesAnalyzer

def test_sales_analyzer_initialization(test_data_path):
    """Test SalesAnalyzer initialization."""
    analyzer = SalesAnalyzer(test_data_path)
    assert isinstance(analyzer, SalesAnalyzer)
    assert analyzer.data_path == Path(test_data_path)
    assert analyzer.data is None
    assert isinstance(analyzer.features, list)
    assert isinstance(analyzer.target, str)

def test_load_data(test_data_path):
    """Test data loading functionality."""
    analyzer = SalesAnalyzer(test_data_path)
    data = analyzer.load_data()
    
    assert isinstance(data, pd.DataFrame)
    assert not data.empty
    assert all(col in data.columns for col in analyzer.features)
    assert analyzer.target in data.columns

def test_prepare_features(test_data_path):
    """Test feature preparation."""
    analyzer = SalesAnalyzer(test_data_path)
    X_train, X_test, y_train, y_test = analyzer.prepare_features()
    
    # Check shapes
    assert len(X_train) + len(X_test) == len(analyzer.data)
    assert len(y_train) + len(y_test) == len(analyzer.data)
    
    # Check types
    assert isinstance(X_train, np.ndarray) or isinstance(X_train, pd.DataFrame)
    assert isinstance(y_train, np.ndarray) or isinstance(y_train, pd.Series)

def test_train_models(test_data_path):
    """Test model training."""
    analyzer = SalesAnalyzer(test_data_path)
    models = analyzer.train_models()
    
    # Check if models dictionary contains expected keys
    assert 'linear_regression' in models
    assert 'decision_tree' in models
    
    # Check if each model contains expected information
    for model_info in models.values():
        assert 'model' in model_info
        assert 'predictions' in model_info
        assert 'score' in model_info
        assert 'mse' in model_info
        
        # Check if metrics are valid
        assert 0 <= model_info['score'] <= 1  # R² score should be between 0 and 1
        assert model_info['mse'] >= 0  # MSE should be non-negative

def test_save_results(test_data_path, test_output_dir):
    """Test saving analysis results."""
    analyzer = SalesAnalyzer(test_data_path)
    analyzer.train_models()
    analyzer.save_results(test_output_dir)
    
    # Check if results file exists
    results_file = test_output_dir / 'model_performance.csv'
    assert results_file.exists()
    
    # Check if results file contains expected data
    results = pd.read_csv(results_file)
    assert 'Model' in results.columns
    assert 'R2_Score' in results.columns
    assert 'MSE' in results.columns
    
    # Check if all models are included
    assert len(results) == 2  # We expect two models: linear regression and decision tree

def test_invalid_data():
    """Test handling of invalid data."""
    with pytest.raises(Exception):
        analyzer = SalesAnalyzer('nonexistent.csv')
        analyzer.load_data()