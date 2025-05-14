import socket
import time
import re

class URLMonitor:
    def __init__(self, cowrie_db, monitoring_db):
        self.cowrie_db = cowrie_db
        self.monitoring_db = monitoring_db
        self.last_known_dowloads_urls_cowrie_db = set()
        self.last_known_input_urls_cowrie_db = set()

    def extract_urls_from_log(self, log_entry):
        """
        Extracts URLs from a given log entry.
        This method uses a regular expression to find all URLs in the provided log entry.
        It then cleans the URLs by removing any trailing semicolons.
        Args:
            log_entry (str): The log entry from which to extract URLs.
        Returns:
            set: A set of cleaned URLs found in the log entry.
        """
        url_pattern = r'https?://[^\s<>\"]+|www\.[^\s<>\"]+' 

        urls = set(re.findall(url_pattern, log_entry))

        cleaned_urls = set(url.rstrip(';') for url in urls)

        return cleaned_urls
    
    def verify_connections(self):
        """
        Verifies the connectivity to a list of URLs retrieved from the monitoring database.
        This method retrieves URLs from the monitoring database, extracts the host and port
        using a regular expression, and attempts to establish a connection to each URL.
        If the connection is successful, it updates the last view timestamp in the database.
        If the connection fails or the URL format is invalid, it logs an appropriate message.
        Raises:
            socket.error: If a connection attempt to a URL fails.
        Notes:
            - The default port is 443 for HTTPS URLs and 80 for HTTP URLs if no port is specified.
            - The connection timeout is set to 5 seconds.
        """
        urls = self.monitoring_db.get_urls_monitoring()

        # Regex for domain/IP and port (if present)
        addrPattern = (
            r'https?:\/\/'  # http or https
            r'((?:\d{1,3}\.){3}\d{1,3}'  # IPv4 address
            r'|'  # or
            r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})'  # domain name
            r'(?::(\d+))?'  # optional port
        )

        for url in urls:
            if url['url']:
                match = re.search(addrPattern, url['url'])
                if match:
                    host = match.group(1)

                    if match.group(2):
                        port = int(match.group(2))
                    else:
                        if url['url'].startswith('https'):
                            port = 443
                        else:
                            port = 80

                    print(f"[VERIFYING CONNECTION] Testing {host}:{port}")

                    try:
                        with socket.create_connection((host, port), timeout=5) as s:
                            print(f"[VERIFYING CONNECTION] Connection {host}:{port} successful")
                            self.monitoring_db.update_last_view(url['url'])
                    except socket.error:
                        print(f"[VERIFYING CONNECTION] Connection to {host}:{port} failed")
                else:
                    print(f"[VERIFYING CONNECTION] Invalid URL format: {url['url']}")
    
    def verify_from_input(self):
        """
        Verifies the current inputs from the Cowrie database and checks for changes.
        If changes are detected, it extracts URLs from the new inputs and inserts them into the monitoring database.
        Updates the last known inputs from the Cowrie database to the current inputs.
        Raises:
            Exception: If there is an error during the verification or URL insertion process.
        """
        current_inputs = set(input['input'] for input in self.cowrie_db.get_inputs_cowrie())

        try:
            if current_inputs != self.last_known_input_urls_cowrie_db:
                print(f"[VERIFYING URL] Change Detect on Input on Cowrie!")

                for input in current_inputs:
                    urls = set(self.extract_urls_from_log(input))
                    if urls:
                        for url in urls:
                            try:
                                self.monitoring_db.insert_url(url)
                            except Exception as e:
                                print(f"[VERIFYING URL] Error adding URL {url}: {str(e)}")

                self.last_known_input_urls_cowrie_db = current_inputs

            else:
                print("[VERIFYING URL] No change on Input on Cowrie!")
                
        except Exception as e:
            print(f"[VERIFYING URL] Error on verifying: {str(e)}")
        
    def verify_download(self):
        """
        Verifies if there are new URLs in the Cowrie database that are not present in the monitoring database.
        This method compares the current URLs from the Cowrie database with the last known URLs and the URLs in the monitoring database.
        If there are new URLs in the Cowrie database, it inserts them into the monitoring database and updates the last known URLs.
        Raises:
            Exception: If there is an error while fetching URLs from the databases or inserting URLs into the monitoring database.
        """
        try:
            current_cowrie_urls = set(url['url'] for url in self.cowrie_db.get_urls_cowrie())
            
            if current_cowrie_urls != self.last_known_dowloads_urls_cowrie_db:
                print(f"[VERIFYING URL] Change Detect on Downloads on Cowrie!")
                
                monitoring_urls = set(url['url'] for url in self.monitoring_db.get_urls_monitoring())
                
                new_urls = current_cowrie_urls - monitoring_urls
                
                if new_urls:
                    for url in new_urls:
                        try:
                            self.monitoring_db.insert_url(url)
                        except Exception as e:
                            print(f"[VERIFYING URL] Error adding URL {url}: {str(e)}")
                
                self.last_known_dowloads_urls_cowrie_db = current_cowrie_urls
                
            else:
                print("[VERIFYING URL] No change on Downloads on Cowrie!")
                
        except Exception as e:
            print(f"[VERIFYING URL] Error on veryfying: {str(e)}")
    
    def populate_urls_monitoring(self):
        """
        Populates the monitoring database with URLs from the Cowrie database.
        This method retrieves URLs from the Cowrie database, stores them in a set,
        and then inserts each URL into the monitoring database. If an error occurs
        during the insertion of a URL, it catches the exception and prints an error message.
        Raises:
            Exception: If there is an error inserting a URL into the monitoring database.
        """
        print("[INIT] Initializing population of monitoringDB")
        urls = self.cowrie_db.get_urls_cowrie()
        initial_urls = set(url['url'] for url in urls)
        self.last_known_dowloads_urls_cowrie_db = initial_urls
        
        for url in initial_urls:
            try:
                self.monitoring_db.insert_url(url)
            except Exception as e:
                print(f"[INIT] Error adding URL {url}: {str(e)}")
    
    def run_periodic_tasks(self):        
        """
        Runs periodic tasks for monitoring and verification.
        This method performs the following steps:
        1. Checks if the monitoring database is empty. If empty, it populates the URLs for monitoring.
        2. If the monitoring database is not empty, it loads the last known URLs from the Cowrie database.
        3. Enters an infinite loop where it periodically:
            - Runs verification tasks for downloads and input.
            - Verifies connections if the monitoring database is not empty.
            - Sleeps for a specified interval before repeating the tasks.
        Prints status messages to indicate the progress of the tasks.
        """
        if self.monitoring_db.url_monitoring_is_empty():
            print("[INIT] MonitoringDB empty")
            self.populate_urls_monitoring()
        else:
            self.last_known_dowloads_urls_cowrie_db = set(url['url'] for url in self.cowrie_db.get_urls_cowrie())
            print(f"[INIT] State loaded: {self.last_known_dowloads_urls_cowrie_db}")
        
        while True:
            print("[PERIODIC TASK] Running...")

            #self.cowrie_db.ensure_connection()
            #self.monitoring_db.ensure_connection()

            self.verify_download()
            self.verify_from_input()
        
            if not self.monitoring_db.url_monitoring_is_empty():
                self.verify_connections()

            #self.cowrie_db.close_connection()
            #self.monitoring_db.close_connection()

            print("[PERIODIC TASK] Finished!", end="\n\n")

            time.sleep(5)
    
    def start(self):
        self.run_periodic_tasks()