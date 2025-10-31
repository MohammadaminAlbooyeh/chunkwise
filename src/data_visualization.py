

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pathlib import Path
import logging
from typing import Optional, Union, List

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SalesVisualizer:
    """A class for creating visualizations of sales data."""
    
    def __init__(self, data_path: Union[str, Path]):
        """Initialize with the path to the data file."""
        self.data_path = Path(data_path)
        self.data = None
        self._setup_style()
        
    def _setup_style(self) -> None:
        """Set up the plotting style."""
        plt.style.use('seaborn')
        sns.set_palette('deep')
        
    def load_data(self) -> pd.DataFrame:
        """Load the data for visualization."""
        try:
            self.data = pd.read_csv(self.data_path)
            self.data['Date'] = pd.to_datetime(self.data['Date'])
            logger.info(f"Data loaded successfully from {self.data_path}")
            return self.data
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
            
    def plot_sales_trends(self, save_dir: Optional[Path] = None) -> None:
        """Create various sales trend visualizations."""
        if self.data is None:
            self.load_data()
            
        try:
            # Daily sales trend
            plt.figure(figsize=(12, 6))
            daily_sales = self.data.groupby('Date')['Total_Amount'].sum()
            daily_sales.plot(marker='o')
            plt.title('Daily Sales Trend')
            plt.xlabel('Date')
            plt.ylabel('Total Sales ($)')
            plt.grid(True)
            
            if save_dir:
                plt.savefig(save_dir / 'daily_sales_trend.png')
            plt.close()
            
            # Category-wise sales
            plt.figure(figsize=(10, 6))
            category_sales = self.data.groupby('Category')['Total_Amount'].sum()
            category_sales.sort_values().plot(kind='barh')
            plt.title('Sales by Category')
            plt.xlabel('Total Sales ($)')
            
            if save_dir:
                plt.savefig(save_dir / 'category_sales.png')
            plt.close()
            
            logger.info("Sales trends plots created successfully")
            
        except Exception as e:
            logger.error(f"Error creating sales trends plots: {str(e)}")
            raise
            
    def plot_customer_analysis(self, save_dir: Optional[Path] = None) -> None:
        """Create customer-related visualizations."""
        if self.data is None:
            self.load_data()
            
        try:
            # Regional distribution
            plt.figure(figsize=(8, 8))
            self.data['Region'].value_counts().plot(kind='pie', autopct='%1.1f%%')
            plt.title('Sales Distribution by Region')
            
            if save_dir:
                plt.savefig(save_dir / 'regional_distribution.png')
            plt.close()
            
            # Payment methods
            plt.figure(figsize=(10, 6))
            payment_counts = self.data['Payment_Method'].value_counts()
            payment_counts.plot(kind='bar')
            plt.title('Payment Method Distribution')
            plt.xticks(rotation=45)
            
            if save_dir:
                plt.savefig(save_dir / 'payment_methods.png')
            plt.close()
            
            logger.info("Customer analysis plots created successfully")
            
        except Exception as e:
            logger.error(f"Error creating customer analysis plots: {str(e)}")
            raise
            
    def plot_product_analysis(self, save_dir: Optional[Path] = None) -> None:
        """Create product-related visualizations."""
        if self.data is None:
            self.load_data()
            
        try:
            # Price distribution
            plt.figure(figsize=(10, 6))
            sns.boxplot(x='Category', y='Price', data=self.data)
            plt.title('Price Distribution by Category')
            plt.xticks(rotation=45)
            
            if save_dir:
                plt.savefig(save_dir / 'price_distribution.png')
            plt.close()
            
            # Quantity vs Price
            plt.figure(figsize=(10, 6))
            plt.scatter(self.data['Price'], self.data['Quantity'], alpha=0.5)
            plt.title('Price vs Quantity')
            plt.xlabel('Price ($)')
            plt.ylabel('Quantity')
            plt.grid(True)
            
            if save_dir:
                plt.savefig(save_dir / 'price_quantity_relation.png')
            plt.close()
            
            logger.info("Product analysis plots created successfully")
            
        except Exception as e:
            logger.error(f"Error creating product analysis plots: {str(e)}")
            raise

def main():
    """Main function to demonstrate the visualization capabilities."""
    try:
        # Initialize visualizer
        visualizer = SalesVisualizer('../data/processed/cleaned_sales_data.csv')
        
        # Create output directory
        output_dir = Path('../output/figures')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate all plots
        visualizer.plot_sales_trends(output_dir)
        visualizer.plot_customer_analysis(output_dir)
        visualizer.plot_product_analysis(output_dir)
        
        logger.info(f"All visualizations saved to {output_dir}")
        
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")

if __name__ == "__main__":
    main()