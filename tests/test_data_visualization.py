import pytest
import matplotlib.pyplot as plt
from src.data_visualization import SalesVisualizer
from pathlib import Path

def test_sales_visualizer_initialization(test_data_path):
    """Test SalesVisualizer initialization."""
    visualizer = SalesVisualizer(test_data_path)
    assert isinstance(visualizer, SalesVisualizer)
    assert visualizer.data_path == Path(test_data_path)
    assert visualizer.data is None

def test_load_data(test_data_path):
    """Test data loading functionality."""
    visualizer = SalesVisualizer(test_data_path)
    data = visualizer.load_data()
    
    assert data is not None
    assert not data.empty
    assert 'Date' in data.columns
    assert pd.api.types.is_datetime64_any_dtype(data['Date'])

def test_plot_sales_trends(test_data_path, test_output_dir):
    """Test sales trends plotting."""
    visualizer = SalesVisualizer(test_data_path)
    visualizer.load_data()
    
    # Test plotting with save
    visualizer.plot_sales_trends(test_output_dir)
    assert (test_output_dir / 'daily_sales_trend.png').exists()
    assert (test_output_dir / 'category_sales.png').exists()
    
    # Test plotting without save
    plt.close('all')
    visualizer.plot_sales_trends()
    
def test_plot_customer_analysis(test_data_path, test_output_dir):
    """Test customer analysis plotting."""
    visualizer = SalesVisualizer(test_data_path)
    visualizer.load_data()
    
    # Test plotting with save
    visualizer.plot_customer_analysis(test_output_dir)
    assert (test_output_dir / 'regional_distribution.png').exists()
    assert (test_output_dir / 'payment_methods.png').exists()
    
    # Test plotting without save
    plt.close('all')
    visualizer.plot_customer_analysis()

def test_plot_product_analysis(test_data_path, test_output_dir):
    """Test product analysis plotting."""
    visualizer = SalesVisualizer(test_data_path)
    visualizer.load_data()
    
    # Test plotting with save
    visualizer.plot_product_analysis(test_output_dir)
    assert (test_output_dir / 'price_distribution.png').exists()
    assert (test_output_dir / 'price_quantity_relation.png').exists()
    
    # Test plotting without save
    plt.close('all')
    visualizer.plot_product_analysis()

def test_invalid_data_path():
    """Test handling of invalid data path."""
    with pytest.raises(Exception):
        visualizer = SalesVisualizer('nonexistent.csv')
        visualizer.load_data()