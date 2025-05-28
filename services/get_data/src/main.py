from config import Settings
from database import Database
from api import API
from loguru import logger

def main(
    api: API,
    db: Database,
    endpoint_configs: dict,
):

    # 1. Connect to the SQL Server
    conn = db.connect()

    # 2. Iterate over the endpoint configs and get the data
    for endpoint_name, endpoint_config in endpoint_configs.items():    

        # 2.0 Clean the table in the database
        db.clean_table(endpoint_config['table_name'], conn)

        # 2.1. Get the data
        success = api.get_and_save_data(endpoint_config, conn, db)

        if not success:
            logger.error(f"Error getting data from the API for table {endpoint_config['table_name']}")
            break
        else:
            logger.info(f"Data saved successfully for table {endpoint_config['table_name']}")
            logger.info("--------------------------------")


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
    )

    main(
        api,
        db,
        settings.ENDPOINT_CONFIGS,
    )
