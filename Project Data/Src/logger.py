import logging
import os

    # Configures the logging system for the ETL pipeline.
    # Based on official Python Documentation (Logging Cookbook): 
    # https://docs.python.org/3/howto/logging-cookbook.html#multiple-handlers
def setup_logging():
    log_folder = 'Logs'
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_folder, 'pipeline.log')),
            logging.StreamHandler() 
        ]
    )
    return logging.getLogger("ETL_Pipeline")