from config import Settings
from database import Database
from api import API
from loguru import logger
from datetime import datetime

import time

def main(
    api: API,
    db: Database,
    endpoint_configs: dict,
):

    # 2. Iterate over the endpoint configs and get the data
    for endpoint_name, endpoint_config in endpoint_configs.items():    
        
        table_name = endpoint_config['table_name']

        # Record start time for logs 
        start_time_endpoint = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Format: 2025-05-29 04:34:31.457
        
        try:
            # 2.1 Clean the table in the database
            db.clean_table(table_name)

            # 2.3. Get the data
            success,total_rows = api.get_and_save_data(endpoint_config, db)

            # Data for logs
            end_time_endpoint = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Format: 2025-05-29 04:34:31.457

        except Exception as e:    
            logger.info(f"Error processing table: {table_name}")
            logger.info(f"{e}")
            success = False
            total_rows = 0
            end_time_endpoint = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        # 2.4 Save the status in the database table
        status = "SUCCESS" if success else "FAILED"
        db.log_status_process(table_name, start_time_endpoint, end_time_endpoint, status, total_rows)

        if not success:
            logger.error(f"Error getting data from the API for table {endpoint_config['table_name']}")
            continue
        else:
            logger.info(f"Data saved successfully for table {endpoint_config['table_name']}")
            logger.info(f"------------------------------------------")


if __name__ == "__main__":
    settings = Settings()

    # Initialize the API
    api = API(
        api_tenant_id=settings.API_TENANT_ID,
        api_client_id=settings.API_CLIENT_ID,
        api_client_secret=settings.API_CLIENT_SECRET,
        base_url=settings.BASE_URL,
    )

    # Initialize the database
    db = Database(
        host=settings.SQL_HOST,
        database=settings.SQL_DATABASE,
        username=settings.SQL_USERNAME,
        password=settings.SQL_PASSWORD,
        port=settings.SQL_PORT,
        batch_size=settings.BATCH_SIZE,
    )

    main(
        api,
        db,
        settings.ENDPOINT_CONFIGS,
    )
