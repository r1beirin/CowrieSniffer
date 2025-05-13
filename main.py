from app.Config import Config
from app.database.MonitoringDBHandler import MonitoringDBHandler
from app.database.CowrieDBHandler import CowrieDBHandler
from app.monitoring.URLMonitor import URLMonitor

def main():
    config = Config()
    cowrie_db_config = config.get_cowrie_db_config()
    monitoring_db_config = config.get_monitoring_db_config()

    cowrie_db = CowrieDBHandler(cowrie_db_config)
    monitoring_db = MonitoringDBHandler(monitoring_db_config)

    monitor = URLMonitor(cowrie_db, monitoring_db)
    monitor.start()

if __name__ == '__main__':
    main()
