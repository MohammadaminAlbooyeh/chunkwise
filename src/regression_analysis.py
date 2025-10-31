import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from pathlib import Path
import logging
from typing import Tuple, Dict, Union

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SalesAnalyzer:
    """A class for analyzing sales data using regression techniques."""
    
    def __init__(self, data_path: Union[str, Path]):
        """Initialize with path to the cleaned data."""
        self.data_path = Path(data_path)
        self.data = None
        self.features = ['Price', 'Quantity', 'Discount']
        self.target = 'Total_Amount'
        self.models = {}
        
    def load_data(self) -> pd.DataFrame:
        """Load and prepare the data for analysis."""
        try:
            self.data = pd.read_csv(self.data_path)
            logger.info(f"Data loaded successfully from {self.data_path}")
            return self.data
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
            
    def prepare_features(self) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare features and target variables."""
        if self.data is None:
            self.load_data()
            
        try:
            X = self.data[self.features]
            y = self.data[self.target]
            
            # Split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            logger.info("Features prepared successfully")
            return (X_train, X_test, y_train, y_test)
            
        except Exception as e:
            logger.error(f"Error preparing features: {str(e)}")
            raise
            
    def train_models(self) -> Dict:
        """Train multiple regression models."""
        try:
            X_train, X_test, y_train, y_test = self.prepare_features()
            
            # Linear Regression
            lr_model = LinearRegression()
            lr_model.fit(X_train, y_train)
            lr_pred = lr_model.predict(X_test)
            lr_score = r2_score(y_test, lr_pred)
            
            # Decision Tree Regression
            dt_model = DecisionTreeRegressor(random_state=42)
            dt_model.fit(X_train, y_train)
            dt_pred = dt_model.predict(X_test)
            dt_score = r2_score(y_test, dt_pred)
            
            # Store models and their performances
            self.models = {
                'linear_regression': {
                    'model': lr_model,
                    'predictions': lr_pred,
                    'score': lr_score,
                    'mse': mean_squared_error(y_test, lr_pred)
                },
                'decision_tree': {
                    'model': dt_model,
                    'predictions': dt_pred,
                    'score': dt_score,
                    'mse': mean_squared_error(y_test, dt_pred)
                }
            }
            
            logger.info("Models trained successfully")
            return self.models
            
        except Exception as e:
            logger.error(f"Error training models: {str(e)}")
            raise
            
    def save_results(self, output_dir: Union[str, Path]) -> None:
        """Save analysis results to files."""
        try:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save model performances
            performance_df = pd.DataFrame({
                'Model': list(self.models.keys()),
                'R2_Score': [m['score'] for m in self.models.values()],
                'MSE': [m['mse'] for m in self.models.values()]
            })
            
            performance_df.to_csv(output_dir / 'model_performance.csv', index=False)
            logger.info(f"Results saved to {output_dir}")
            
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            raise

def main():
    """Main function to demonstrate the analysis process."""
    try:
        # Initialize analyzer
        analyzer = SalesAnalyzer('../data/processed/cleaned_sales_data.csv')
        
        # Train models
        models = analyzer.train_models()
        
        # Save results
        analyzer.save_results('../output/analysis')
        
        # Print model performances
        for name, model_info in models.items():
            print(f"\n{name.replace('_', ' ').title()}:")
            print(f"R² Score: {model_info['score']:.4f}")
            print(f"MSE: {model_info['mse']:.4f}")
        
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")

if __name__ == "__main__":
    main()