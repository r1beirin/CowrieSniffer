from datetime import datetime
import mysql.connector
from mysql.connector import Error
import time
import contextlib

class MonitoringDBHandler:
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
    
    def url_monitoring_is_empty(self):
        try:
            with self.get_connection() as (cursor, connection):
                cursor.execute("SELECT COUNT(*) AS count FROM urls")
                result = cursor.fetchone()
                return result['count'] == 0
                
        except Error as error:
            print(f"Error checking if urls table is empty: {error}")
            return False
    
    def update_last_view(self, url):
        try:
            with self.get_connection() as (cursor, connection):
                cursor.execute("SELECT url FROM urls WHERE url = %s", (url,))
                if not cursor.fetchone():
                    print(f"URL '{url}' does not exist in monitoring.")
                    return
                
                currentTime = datetime.now()
                sql = "UPDATE urls SET last_view = %s WHERE url = %s"
                cursor.execute(sql, (currentTime, url))
                connection.commit()
                
                print(f"Updated URL: {url}")
                
        except Error as error:
            print(f"Error updating URL: {error}")
    
    def insert_url(self, url):
        try:
            with self.get_connection() as (cursor, connection):
                cursor.execute("SELECT url FROM urls WHERE url = %s", (url,))
                if cursor.fetchone():
                    print(f"URL '{url}' already exists in monitoring.")
                    return
                
                currentTime = datetime.now()
                sql = "INSERT INTO urls (url, first_view, last_view) VALUES (%s, %s, %s)"
                cursor.execute(sql, (url, currentTime, currentTime))
                connection.commit()
                
                print(f"Inserted URL: {url}")
                
        except Error as error:
            print(f"Error inserting URL: {error}")
    
    def get_urls_monitoring(self):
        try:
            with self.get_connection() as (cursor, connection):
                query = "SELECT DISTINCT url FROM urls ORDER BY url"
                cursor.execute(query)
                return cursor.fetchall()
                
        except Error as error:
            print(f"Error getting URLs from monitoring: {error}")
            return []