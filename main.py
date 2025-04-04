from app.Config import Config
from app.database.MonitoringDBHandler import MonitoringDBHandler
from app.database.CowrieDBHandler import CowrieDBHandler
from app.monitoring.Scheduler import Scheduler

def main():
    config = Config()
    cowrie_db_config = config.get_cowrie_db_config()
    monitoring_db_config = config.get_monitoring_db_config()

    cowrie_db = CowrieDBHandler(cowrie_db_config)
    monitoring_db = MonitoringDBHandler(monitoring_db_config)

    scheduler = Scheduler(cowrie_db, monitoring_db)
    scheduler.start()

if __name__ == '__main__':
    main()
