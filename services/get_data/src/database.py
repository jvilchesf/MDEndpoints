import pyodbc
from loguru import logger
from contextlib import contextmanager
import pandas as pd
import gc

class Database:
    def __init__(self, 
        host: str,
        database: str,
        username: str,
        password: str,
        port: int,
        batch_size: int,
    ):
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.port = port
        self.batch_size = batch_size
        self.connection_string = self._build_connection_string()

    
    def _build_connection_string(self):
        return (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={self.host},{self.port};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password};"
            "TrustServerCertificate=yes;"
            "Encrypt=yes;"
            "Connection Timeout=30;"
            "Command Timeout=300;"  # 5 minutes for long operations
            "Trust_Connection=yes"
        )
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = pyodbc.connect(self.connection_string)
            conn.autocommit = False
            #logger.info(f"Successfully connected to database {self.database}")
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def clean_table(self, table_name: str):
        """Clean table with proper connection management"""
        query = f"TRUNCATE TABLE {table_name}"  # TRUNCATE is faster than DELETE
        
        with self.get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
                logger.info(f"Table {table_name} cleaned")
            except pyodbc.Error as e:
                logger.error(f"Error cleaning table {table_name}: {e}")
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

        # Free memory
        del data
        gc.collect()

        # Check which columns exist in both dataframe and database
        available_df_columns = df.columns.tolist()
        valid_columns = [col for col in columns_db if col in available_df_columns]
        
        # Validate database table and data api exctracted have same columns
        if len(columns_db) != len(available_df_columns):
            logger.info(f"{columns_db=}")
            logger.info(f"Available_df_columns: {available_df_columns}")
            logger.info(f"Valid_columns       : {valid_columns}")
            logger.error(f"Database table and data api have different number of columns, it was fixed...")

        df = df[valid_columns]  # This will only keep the specified columns



        total_rows = len(df)
        for i in range(0, total_rows, self.batch_size):

            # Initialize batch start and end for each iteration
            batch_end = min(i + self.batch_size, total_rows)

            # Create batch to insert into the database
            batch = df[i:batch_end]

            # Convert to records with memory optimization
            # Use itertuples instead of to_records for better memory efficiency
            data_as_tuples = [tuple(row[1:]) for row in batch.itertuples()]


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
                cursor.executemany(query, data_as_tuples)
                conn.commit()
                # Clean up
                del data_as_tuples
                gc.collect()

            except Exception as e:
                logger.error(f"Error loading data into the database, table_name: {table_name}, n_rows= {len(data_as_tuples)}")
                logger.error(f"Error type: {type(e).__name__}")
                logger.error(f"Error message: {str(e)}")
                logger.error(f"Query: {query}")
                
                # Try to get more specific error information
                if hasattr(e, 'args') and e.args:
                    logger.error(f"Error args: {e.args}")
                
                return False

#       logger.info(f"Successfully processed all {total_processed:,} rows for {table_name}")
        return True



    def log_status_process(self,
                           table_name: str,
                           start_time_endpoint: str,
                           end_time_endpoint: str, 
                           status: str, 
                           total_rows: int,
                           ) -> bool:

        """
        Save status process in a database table called ep_execution_log
        """

        # Create query - removed extra quote and adjusted parameters
        query = """
            INSERT INTO ep_execution_log (table_name, start_time_endpoint, end_time_endpoint, status, total_rows)
            VALUES (?, ?, ?, ?, ?)
            """
        with self.get_connection() as conn:
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