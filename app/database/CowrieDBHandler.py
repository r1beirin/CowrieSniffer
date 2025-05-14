from datetime import datetime
import mysql.connector
from mysql.connector import Error
import time
import contextlib

class CowrieDBHandler:
    def __init__(self, configDB):
        self.configDB = configDB

    @contextlib.contextmanager
    def get_connection(self):
        connection = None
        cursor = None
        try:
            max_retries = 5
            for retry in range(max_retries):
                try:
                    connection = mysql.connector.connect(**self.configDB)
                    cursor = connection.cursor(dictionary=True, buffered=True)
                    break
                except Error as e:
                    print(f"Error connecting to database (attempt {retry+1}/{max_retries}): {e}")
                    if retry == max_retries - 1:
                        raise
                    time.sleep(2)
                    
            yield cursor, connection
            
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
    
    def get_urls_cowrie(self):
        try:
            with self.get_connection() as (cursor, connection):
                query = "SELECT DISTINCT url FROM downloads ORDER BY url"
                cursor.execute(query)
                return cursor.fetchall()
                
        except Error as error:
            print(f"Error executing query on CowrieDB: {error}")
            return []
    
    def get_inputs_cowrie(self):
        try:
            with self.get_connection() as (cursor, connection):
                query = "SELECT DISTINCT input FROM input ORDER BY input"
                cursor.execute(query)
                return cursor.fetchall()
                
        except Error as error:
            print(f"Error executing query on CowrieDB: {error}")
            return []