import configparser

class Config:
    def __init__(self, config_file='config/config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_cowrie_db_config(self):
        return {
            'host': self.config.get('CowrieDB', 'host'),
            'user': self.config.get('CowrieDB', 'user'),
            'password': self.config.get('CowrieDB', 'password'),
            'database': self.config.get('CowrieDB', 'database')
        }

    def get_monitoring_db_config(self):
        return {
            'host': self.config.get('MonitoringDB', 'host'),
            'user': self.config.get('MonitoringDB', 'user'),
            'password': self.config.get('MonitoringDB', 'password'),
            'database': self.config.get('MonitoringDB', 'database')
        }