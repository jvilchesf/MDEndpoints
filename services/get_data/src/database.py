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
        columns = self.get_table_columns(conn, table_name)

        # Some tables have ID autoincrement, I have to remove it before filter dataframe
        columns = [col for col in columns if col != "ID"]

        # Filter columns in the data dictionary
        # If you convert to DataFrame first
        df = pd.DataFrame(data)

        data = df[columns]  # This will only keep the specified columns

        # Convert to list of tuples
        data_as_tuples = data.to_records(index=False).tolist()

        #Creating place holders
        insert_columns = f"({','.join(columns)})"
        place_holders= f"({','.join( '?' for col in columns)})"

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

            logger.info(f"Data loaded into the mssql database, it took {total_load_data} seconds")
            return True
        except Exception as e:
            logger.info(f"Error loading data into the database, table_name: {table_name}, n_rows= {len(data_as_tuples)}")
            logger.info(f"{e}")
            logger.info(f"{query}")
            return False
