import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Optional, Union, Dict

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCleaner:
    """A class for reading and cleaning sales data."""
    
    def __init__(self, input_path: Union[str, Path]):
        """Initialize with the path to the data file."""
        self.input_path = Path(input_path)
        self.data = None
        
    def read_data(self) -> pd.DataFrame:
        """Read data from CSV or Excel file."""
        try:
            if self.input_path.suffix.lower() == '.csv':
                self.data = pd.read_csv(self.input_path)
            elif self.input_path.suffix.lower() in ['.xlsx', '.xls']:
                self.data = pd.read_excel(self.input_path)
            else:
                raise ValueError(f"Unsupported file format: {self.input_path.suffix}")
            
            logger.info(f"Successfully read data from {self.input_path}")
            return self.data
            
        except Exception as e:
            logger.error(f"Error reading data: {str(e)}")
            raise
    
    def clean_data(self, config: Optional[Dict] = None) -> pd.DataFrame:
        """Clean the data based on configuration."""
        if self.data is None:
            self.read_data()
            
        try:
            # Remove duplicates
            initial_rows = len(self.data)
            self.data.drop_duplicates(inplace=True)
            logger.info(f"Removed {initial_rows - len(self.data)} duplicate rows")
            
            # Handle missing values
            if config and config.get('fill_missing'):
                self.data.fillna(config['fill_missing'], inplace=True)
            else:
                self.data.dropna(inplace=True)
            
            # Convert date column
            if 'Date' in self.data.columns:
                self.data['Date'] = pd.to_datetime(self.data['Date'])
            
            # Standardize categorical columns
            categorical_cols = ['Category', 'Region', 'Payment_Method']
            for col in categorical_cols:
                if col in self.data.columns:
                    self.data[col] = self.data[col].str.strip().str.title()
            
            # Validate numeric columns
            numeric_cols = ['Price', 'Quantity', 'Total_Amount']
            for col in numeric_cols:
                if col in self.data.columns:
                    self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
                    self.data = self.data[self.data[col] >= 0]  # Remove negative values
            
            logger.info("Data cleaning completed successfully")
            return self.data
            
        except Exception as e:
            logger.error(f"Error cleaning data: {str(e)}")
            raise
    
    def save_data(self, output_path: Union[str, Path], format: str = 'csv') -> None:
        """Save the cleaned data to a file."""
        if self.data is None:
            raise ValueError("No data to save. Run clean_data first.")
            
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if format.lower() == 'csv':
                self.data.to_csv(output_path, index=False)
            elif format.lower() in ['xlsx', 'excel']:
                self.data.to_excel(output_path, index=False)
            else:
                raise ValueError(f"Unsupported output format: {format}")
                
            logger.info(f"Data saved successfully to {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            raise

def main():
    """Main function to demonstrate the data cleaning process."""
    try:
        # Initialize data cleaner
        cleaner = DataCleaner('../data/raw/sales_data.csv')
        
        # Read and clean data
        cleaner.read_data()
        cleaned_data = cleaner.clean_data()
        
        # Save cleaned data
        cleaner.save_data('../data/processed/cleaned_sales_data.csv')
        
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")

if __name__ == "__main__":
    main()



