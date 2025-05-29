import pyodbc
from loguru import logger
import time
import pandas as pd

class Database:
    def __init__(self, 
        host: str,
        database: str,
        username: str,
        password: str,
        port: int,
    ):
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.port = port

    def connect(self
        ) -> pyodbc.Connection:
        """"
        Connects to the database using pyodbc
        """

        # Create the connection string with timeout parameters
        connection_string = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={self.host},{self.port};"  # Use comma for port specification
            f"PORT={self.port};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password};"
            "TrustServerCertificate=yes;"
            "Encrypt=yes;"
            "Connection Timeout=30;"
            "Trust_Connection=yes"
        )
        
        try:
            # Connect to the database
            conn = pyodbc.connect(connection_string)
            logger.info(f"Successfully connected to database {self.database}")
            return conn
        except pyodbc.Error as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise

    def clean_table(self, table_name: str, conn: pyodbc.Connection):
        """
        Cleans the table in the database
        """

        # Create the query
        query = f"DELETE FROM {table_name} where 1=1"
        
        try:
            # Execute the query
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            logger.info("--------------------------------")
            logger.info(f"Table {table_name} cleaned")
        except pyodbc.Error as e:
            logger.error(f"Error cleaning table {table_name}", error=str(e))
            raise

    def get_table_columns(self, 
                    conn: pyodbc.Connection, 
                    table_name: str) -> list:
        """
        Get column names for a table
        """

        query = """
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = ?
        ORDER BY ORDINAL_POSITION
        """
        
        try:
            cursor = conn.cursor()
            cursor.execute(query, (table_name,))
            results = cursor.fetchall()
            return [row[0] for row in results]
        except Exception as e:
            logger.error(f"Error getting columns for table {table_name}: {e}")
            return []
        
    def save_data(self, 
                data: dict, 
                endpoint_config: dict, 
                conn: pyodbc.Connection):
        """
        Save the data into the database 
        """

        table_name = endpoint_config['table_name']

        # Get columns from database
        columns_db = self.get_table_columns(conn, table_name)

        # If you convert to DataFrame first
        df = pd.DataFrame(data)  
        # Check which columns exist in both dataframe and database
        available_df_columns = df.columns.tolist()
        valid_columns = [col for col in columns_db if col in available_df_columns]
        
        # Validate database table and data api exctracted have same columns
        if len(columns_db) != len(available_df_columns):
            logger.info(f"{columns_db=}")
            logger.info(f"Available_df_columns: {available_df_columns}")
            logger.info(f"Valid_columns       : {valid_columns}")
            logger.error(f"Database table and data api have different number of columns, it was fixed...")

        data = df[valid_columns]  # This will only keep the specified columns

        # Convert to list of tuples
        data_as_tuples = data.to_records(index=False).tolist()

        #Creating place holders
        insert_columns = f"({','.join(valid_columns)})"
        place_holders= f"({','.join( '?' for col in valid_columns)})"

        # Create query (removed extra quote)
        query = f"""
        INSERT INTO {table_name} {insert_columns} 
        VALUES {place_holders}
        """

        # Initialize variables 
        cursor = conn.cursor()
        cursor.fast_executemany = True

        try:
            start_load_data = time.time()
            cursor.executemany(query, data_as_tuples)
            conn.commit()

            end_load_data = time.time()
            total_load_data = end_load_data - start_load_data

            logger.info(f"Data loaded into {table_name}: {len(data_as_tuples)} rows in {total_load_data:.2f} seconds")
            return True
        except Exception as e:
            logger.error(f"Error loading data into the database, table_name: {table_name}, n_rows= {len(data_as_tuples)}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error message: {str(e)}")
            logger.error(f"Query: {query}")
            
            # Try to get more specific error information
            if hasattr(e, 'args') and e.args:
                logger.error(f"Error args: {e.args}")
            
            return False


    def log_status_process(self,
                           table_name: str,
                           start_time_endpoint: str,
                           end_time_endpoint: str, 
                           status: str, 
                           total_rows: int,
                           conn: pyodbc.Connection
                           ) -> bool:

        """
        Save status process in a database table called ep_execution_log
        """

        # Create query - removed extra quote and adjusted parameters
        query = """
            INSERT INTO ep_execution_log (table_name, start_time_endpoint, end_time_endpoint, status, total_rows)
            VALUES (?, ?, ?, ?, ?)
            """
        
        # Initialize variables
        cursor = conn.cursor()

        try:
            logger.info(f"Saving process status in the table ep_execution_log with values: {table_name}, {start_time_endpoint}, {end_time_endpoint}, {status}, {total_rows}")
            cursor.execute(query, (table_name, start_time_endpoint, end_time_endpoint, status, total_rows))
            conn.commit()   
            return True
        
        except Exception as e:
            logger.error(f"Error logging status process in the database table {table_name}")
            logger.error(f"error = {e}")
            return False