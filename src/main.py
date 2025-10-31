import logging
from pathlib import Path
from reading_cleaning import DataCleaner
from data_visualization import SalesVisualizer
from regression_analysis import SalesAnalyzer
import pandas as pd

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sales_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SalesAnalysisApp:
    """Main application class for sales data analysis."""
    
    def __init__(self):
        """Initialize paths and create necessary directories."""
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / 'data'
        self.raw_data_dir = self.data_dir / 'raw'
        self.processed_data_dir = self.data_dir / 'processed'
        self.output_dir = self.base_dir / 'output'
        self.figures_dir = self.output_dir / 'figures'
        self.analysis_dir = self.output_dir / 'analysis'
        
        # Create necessary directories
        self._create_directories()
        
    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        dirs = [
            self.data_dir,
            self.raw_data_dir,
            self.processed_data_dir,
            self.output_dir,
            self.figures_dir,
            self.analysis_dir
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {dir_path}")
            
    def clean_data(self) -> None:
        """Clean the raw sales data."""
        try:
            raw_data_path = self.raw_data_dir / 'sales_data.csv'
            cleaned_data_path = self.processed_data_dir / 'cleaned_sales_data.csv'
            
            logger.info("Starting data cleaning process...")
            cleaner = DataCleaner(raw_data_path)
            cleaner.read_data()
            cleaner.clean_data()
            cleaner.save_data(cleaned_data_path)
            logger.info("Data cleaning completed successfully")
            
        except Exception as e:
            logger.error(f"Error in data cleaning: {str(e)}")
            raise
            
    def create_visualizations(self) -> None:
        """Create all visualizations."""
        try:
            cleaned_data_path = self.processed_data_dir / 'cleaned_sales_data.csv'
            
            logger.info("Starting visualization process...")
            visualizer = SalesVisualizer(cleaned_data_path)
            visualizer.plot_sales_trends(self.figures_dir)
            visualizer.plot_customer_analysis(self.figures_dir)
            visualizer.plot_product_analysis(self.figures_dir)
            logger.info("Visualizations created successfully")
            
        except Exception as e:
            logger.error(f"Error in visualization creation: {str(e)}")
            raise
            
    def perform_analysis(self) -> None:
        """Perform regression analysis."""
        try:
            cleaned_data_path = self.processed_data_dir / 'cleaned_sales_data.csv'
            
            logger.info("Starting regression analysis...")
            analyzer = SalesAnalyzer(cleaned_data_path)
            models = analyzer.train_models()
            analyzer.save_results(self.analysis_dir)
            
            # Print summary of results
            results_path = self.analysis_dir / 'model_performance.csv'
            if results_path.exists():
                results = pd.read_csv(results_path)
                logger.info("\nModel Performance Summary:")
                logger.info(results.to_string())
                
            logger.info("Analysis completed successfully")
            
        except Exception as e:
            logger.error(f"Error in regression analysis: {str(e)}")
            raise
            
    def run_full_analysis(self) -> None:
        """Run the complete analysis pipeline."""
        try:
            logger.info("Starting full analysis pipeline...")
            
            # Step 1: Clean Data
            self.clean_data()
            
            # Step 2: Create Visualizations
            self.create_visualizations()
            
            # Step 3: Perform Analysis
            self.perform_analysis()
            
            logger.info("Full analysis pipeline completed successfully")
            
        except Exception as e:
            logger.error(f"Error in analysis pipeline: {str(e)}")
            raise

def main():
    """Main function to run the analysis."""
    try:
        # Create and run the application
        app = SalesAnalysisApp()
        app.run_full_analysis()
        
        # Print success message
        logger.info("""
        ========================================
        Sales Analysis Completed Successfully!
        ----------------------------------------
        Results can be found in:
        - Cleaned data: data/processed/
        - Visualizations: output/figures/
        - Analysis results: output/analysis/
        - Logs: sales_analysis.log
        ========================================
        """)
        
    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
