import requests
import pyodbc
import time
from typing import Tuple
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

    def log_progress(self, current: int, total: int, table_name: str, milestones: dict) -> dict:
        """
        Log progress at 25%, 50%, and 75% milestones
        Returns updated milestones dict
        """
        if total > 0:
            progress_percentage = (current / total) * 100
            
            for milestone in [25, 50, 75]:
                if progress_percentage >= milestone and not milestones[milestone]:
                    logger.info(f"Progress Update: {milestone}% completed for {table_name} "
                              f"({current:,} / {total:,} rows)")
                    milestones[milestone] = True
        
        return milestones

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

            response = requests.get(url, params=request_params, headers=headers, timeout=60)
            if response.status_code == 401:
                logger.error("Token expired, getting a new one")
                token = self.get_token()
                return self.run_query_api(endpoint_config, token, params, next_url)

            response.raise_for_status()
            data = response.json()

            # Handle different response structures based on endpoint
            if 'value' in data:
                # Standard response with 'value' key
                return data['value'], data.get('@odata.nextLink')
                
            elif 'exportFiles' in data and endpoint_config['table_name'] == 'ep_info_gathering':
                list_export_files = []
                # Special case for ep_info_gathering - convert to list format
                for export_file in data['exportFiles']:
                    export_record = {
                        'exportFiles': f"{export_file}",
                        'generatedTime': f"{data['generatedTime']}"
                    }
                    list_export_files.append(export_record)
                return list_export_files, None  # Return as list with single record
                
            elif 'score' in data and endpoint_config['table_name'] == 'ep_exposure_score':
                # Special case for ep_exposure_score
                exposure_record = {
                    'score': data['score'], 
                    'time': data.get('timestamp', data.get('time', ''))  # Handle different timestamp field names
                }
                return [exposure_record], None  # Return as list with single record
                
            elif 'score' in data and endpoint_config['table_name'] == 'ep_device_secure_score':
                # Special case for ep_device_secure_score
                device_score_record = {
                    'score': data['score'], 
                    'time': data.get('timestamp', data.get('time', ''))  # Handle different timestamp field names
                }
                return [device_score_record], None  # Return as list with single record
                
            else:
                # Handle other response structures
                if isinstance(data, dict) and len(data) > 0:
                    # Convert single object to list format, excluding metadata
                    clean_data = {k: v for k, v in data.items() if not k.startswith('@')}
                    if clean_data:
                        return [clean_data], None
                    else:
                        logger.info(f"Empty response from API for endpoint {endpoint_config['endpoint']}")
                        return [], None
                else:
                    logger.info(f"Empty or unexpected response from API for endpoint {endpoint_config['endpoint']}")
                    return [], None

        except requests.exceptions.RequestException as e:
            logger.error("API request failed")
            raise

    def get_and_save_data(self,
                        endpoint_config: dict,
                        conn: pyodbc.Connection,
                        db: Database
                        ) -> Tuple[bool, int]:
        """
        Get data from the API with progress logging at 25%, 50%, and 75%
        """

        # Get the token
        token = self.get_token()

        # Initialize the start date
        start_table_iteration = datetime.now()
                
        # Get the parameters for the query pagesize is important to avoid pagination
        params = {"pagesize": str(endpoint_config['pagesize'])}
        
        # Track the next URL for pagination
        next_url = None

        # Total table rows approximately (from config or estimate)
        estimated_total_rows = endpoint_config.get('total_rows', 0)
        
        # Progress tracking
        progress_milestones = {25: False, 50: False, 75: False}

        logger.info(f"Starting to get data from the API for table {endpoint_config['table_name']}")

        total_rows_processed = 0
        success = False

        #count for debugging
        count = 0 

        
        # Iterate over the endpoint config
        while True:

            # Save start date in a variable to look for token expiration
            # If start_table_iteration - now > 30 minutes, get a new token
            if datetime.now() - start_table_iteration > timedelta(minutes=30):
                token = self.get_token()
                start_table_iteration = datetime.now()  # Reset the timer

            # Get the data from the api
            data, next_link = self.run_query_api(endpoint_config, token, params, next_url)

            # process data
            data = process_result(data)

            # Save total rows processed 
            total_rows_processed += len(data)
            
            # Log progress at 25%, 50%, and 75% milestones
            if estimated_total_rows > 0:
                progress_milestones = self.log_progress(total_rows_processed, estimated_total_rows, endpoint_config['table_name'], progress_milestones)

            # Save the data into the mssql database
            success = db.save_data(data, endpoint_config, conn)
            
            if not success:
                logger.error(f"Failed to save data for {endpoint_config['table_name']}")
                break

            # If there is a next link, update the next_url for pagination
            if next_link:
                next_url = next_link
            else:
                break

            # if len data < pagesize, break
            if len(data) < endpoint_config['pagesize']:
                break
                
            count += 1

            if count == 2:
                return True, total_rows_processed

        # Final completion log
        if success:
            logger.info(f"Completed processing {endpoint_config['table_name']}: {total_rows_processed:,} total rows processed")
        else:
            logger.error(f"Failed processing {endpoint_config['table_name']}: {total_rows_processed:,} rows processed before failure")
        
        return success, total_rows_processed


            