from datetime import datetime
import mysql.connector
from mysql.connector import Error
import time

class MonitoringDBHandler:
    def __init__(self, configDB):
        self.configDB = configDB
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                self.connection = mysql.connector.connect(**self.configDB)
                break
            except Error as error:
                print(f"Error connecting to Monitoring database: {error}")
                retries += 1
                if retries >= max_retries:
                    print("Max retries reached. Could not connect to the database.")
                    break
                time.sleep(5)
    
    def url_monitoring_is_empty(self):
        try:
            self.cursor = self.connection.cursor(dictionary=True, buffered=False)
            
            self.cursor.execute("SELECT COUNT(*) AS count FROM urls")
            result = self.cursor.fetchone()
            
            self.cursor.close()
            
            return result['count'] == 0
            
        except Error as error:
            print(f"Error checking urls: {error}")
            return False
        
    def update_last_view(self, url):
        try:
            self.cursor = self.connection.cursor(dictionary=True, buffered=False)

            self.cursor.execute("SELECT url FROM urls WHERE url = %s", (url,))
            if not self.cursor.fetchone():
                print(f"URL '{url}' does not exist in monitoring.")
                return
            
            currentTime = datetime.now()
            sql = "UPDATE urls SET last_view = %s WHERE url = %s"
            self.cursor.execute(sql, (currentTime, url))
            self.connection.commit()
            
            print(f"Updated URL: {url}")
            
            self.cursor.close()
            
        except Error as error:
            print(f"Error updating URL: {error}")
    
    def insert_url(self, url):
        try:
            self.cursor = self.connection.cursor(dictionary=True, buffered=False)

            self.cursor.execute("SELECT url FROM urls WHERE url = %s", (url,))
            if self.cursor.fetchone():
                print(f"URL '{url}' already exists in monitoring.")
                return
            
            currentTime = datetime.now()
            sql = "INSERT INTO urls (url, first_view, last_view) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (url, currentTime, currentTime))

            self.connection.commit()

            print(f"Inserted URL: {url}")
            self.cursor.close()
            
        except Error as error:
            print(f"Error inserting URL: {error}")
    
    def get_urls_monitoring(self):
        try:
            self.cursor = self.connection.cursor(dictionary=True, buffered=False)
            
            query = "SELECT DISTINCT url FROM urls ORDER BY url"
            self.cursor.execute(query)
            
            results = self.cursor.fetchall()
            
            self.cursor.close()
            
            return results
            
        except Error as error:
            print(f"Error executing query on Monitoring: {error}")
            return []