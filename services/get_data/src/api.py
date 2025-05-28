import requests
import pyodbc
import time
from loguru import logger
from datetime import datetime, timedelta
from database import Database
from process_data import process_result

class API:
    def __init__(self,
        api_tenant_id: str,
        api_client_id: str,
        api_client_secret: str,
        base_url: str,
    ):
        self.api_tenant_id = api_tenant_id
        self.api_client_id = api_client_id
        self.api_client_secret = api_client_secret
        self.base_url = base_url

    def get_token(self) -> str:
        """
        Get a token from the API
        """

        token_url = f"https://login.microsoftonline.com/{self.api_tenant_id}/oauth2/v2.0/token"
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.api_client_id,
            'client_secret': self.api_client_secret,
            'scope': 'https://api.securitycenter.microsoft.com/.default'
        }
        
        try:
            response = requests.post(token_url, data=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            logger.info("Token obtained")
            return response.json()['access_token']            
        except requests.exceptions.RequestException as e:
            logger.error("Failed to get access token", error=str(e))
            raise
    
    def run_query_api(self, 
                    endpoint_config: dict,
                    token: str, 
                    params: dict,
                    next_url: str = None) -> dict:
        """
        Run the query against the API and return the data
        """

        # Get the url and headers - use next_url if provided, otherwise construct from endpoint
        if next_url:
            url = next_url
        else:
            url = f"{self.base_url}/{endpoint_config['endpoint']}"

        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json'
        }

        try:
            # Only use params for the first request, not for next_url requests
            request_params = None if next_url else params

            start_request_time = time.time()

            response = requests.get(url, params=request_params, headers=headers, timeout=60)
            if response.status_code == 401:
                logger.error("Token expired, getting a new one")
                token = self.get_token()
                return self.run_query_api(endpoint_config, token, params, next_url)
            
            end_request_time = time.time()
            total_request_time = end_request_time - start_request_time

            response.raise_for_status()
            data = response.json()

            logger.info(f"Data received from the API: {len(data['value'])} rows, it took {total_request_time} seconds")
            return data['value'], data.get('@odata.nextLink')
        except requests.exceptions.RequestException as e:
            logger.error("API request failed")
            raise

    def get_and_save_data(self,
                        endpoint_config: dict,
                        conn: pyodbc.Connection,
                        db: Database
                        ) -> bool:
        """
        Get data from the API
        """

        # Get the token
        token = self.get_token()

        # Initialize the start date
        start_table_iteration = datetime.now()

                
        # Get the parameters for the query pagesize is important to avoid pagination
        params = {"pagesize": str(endpoint_config['pagesize'])}
        
        # Track the next URL for pagination
        next_url = None

        logger.info("--------------------------------")
        logger.info(f"Starting to get data from the API for table {endpoint_config['table_name']}")

        
        # Iterate over the endpoint config
        while True:

            # Save start date in a variable to look for token expiration
            # If start_table_iteration - now > 45 minutes, get a new token
            if start_table_iteration - datetime.now() > timedelta(minutes=45):
                token = self.get_token()

            # Get the data from the api
            data, next_link = self.run_query_api(endpoint_config, token, params, next_url)

            # process data
            data = process_result(data)

            # Save the data into the mssql databasae
            success = db.save_data(data, endpoint_config, conn)

            # If there is a next link, update the next_url for pagination
            if next_link:
                next_url = next_link
            else:
                break

            # if len data < pagesize, break
            if len(data) < endpoint_config['pagesize']:
                break
        
        return True


            