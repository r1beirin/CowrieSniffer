import mysql.connector
from mysql.connector import Error
import time

class CowrieDBHandler:
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
                print(f"Error connecting to Cowrie database: {error}")
                retries += 1
                if retries >= max_retries:
                    print("Max retries reached. Could not connect to the database.")
                    raise
                time.sleep(5)
    
    def get_urls_cowrie(self):
        try:
            self.cursor = self.connection.cursor(dictionary=True, buffered=False)
            self.cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
            
            query = "SELECT DISTINCT url FROM downloads ORDER BY url"
            self.cursor.execute(query)
            
            results = self.cursor.fetchall()
            
            self.cursor.close()
            
            return results
            
        except Error as error:
            print(f"Error executing query on CowrieDB: {error}")
            return []
    
    def get_inputs_cowrie(self):
        try:
            self.cursor = self.connection.cursor(dictionary=True, buffered=False)
            self.cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")

            query = "SELECT DISTINCT input FROM input ORDER BY input"
            self.cursor.execute(query)
            
            results = self.cursor.fetchall()
            
            self.cursor.close()
            
            return results
            
        except Error as error:
            print(f"Error executing query on CowrieDB: {error}")
            return []