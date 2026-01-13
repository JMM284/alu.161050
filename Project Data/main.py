import logging
from Src.logger import setup_logging
from Src.extract import run_extract
from Src.validation import run_validation
from Src.transform import run_transform
from Src.load import run_load

# Initialize the monitoring system
logger = setup_logging()

def run_pipeline():
    logger.info("Starting ETL Pipeline")
    
    try:
        # Step 1: Extraction process
        logger.info("Executing: Extract Stage")
        run_extract()
        
        # Step 2: Validation process
        logger.info("Executing: Validation Stage")
        players_validated, teams_validated = run_validation()
        
        # Step 3: Transformation process
        logger.info("Executing: Transform Stage")
        dim_players_table, dim_teams_table, fact_players_table, fact_teams_table = run_transform(players_validated, teams_validated)
        
        # Step 4: Loading process
        logger.info("Executing: Load Stage")
        run_load(dim_players_table, dim_teams_table, fact_players_table, fact_teams_table)
        
        logger.info(" Pipeline completed successfully ")

    except Exception as e:
        logger.critical(f"Pipeline failed! Error details: {e}")

if __name__ == "__main__":
    run_pipeline()