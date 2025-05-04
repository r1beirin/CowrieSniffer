# CowrieSniffer

CowrieSniffer is a tool designed to monitor and analyze URLs captured by the Cowrie honeypot, checking their availability in real time. The main goal is to assist in threat investigation by tracking malicious addresses used by attackers and providing valuable data for security analysis.

# Technologies Used
* Python – main programming language.
* Docker – ensures easy deployment and portability.
* MySQL – used for storing extracted records from the honeypot.
* Cowrie – honeypot used to capture attacker interactions.

# Installation
1. Clone the repository:
```bash
git clone https://github.com/r1beirin/CowrieSniffer.git
cd CowrieSniffer
```

2. Setup config/config.ini with your informations

3. Set up and start the Docker container
```bash
docker-compose up -d
```

4. Install the requirements and run the tool
```bash
pip install -r requirements.txt
python main.py
```

# Project Structure
```
./
└── main.py
└── app/
    ├── Config.py
    ├── database/
    │   ├── CowrieDBHandler.py
    │   └── MonitoringDBHandler.py
    └── monitoring/
        └── Scheduler.py
```

##### main.py
The `main.py` file serves as the entry point for our honeypot monitoring system. It initializes the core components, establishes database connections, and launches the monitoring scheduler. This orchestrator module imports and integrates all specialized packages, effectively bootstrapping the application by creating instances of database handlers and starting the monitoring process.

##### Config.py
The `Config.py` module manages all system configurations, providing a centralized approach to handling settings for both the Cowrie honeypot and monitoring databases. It abstracts the configuration logic, allowing for easy modifications of database credentials, connection parameters, and other system-wide settings without altering the core application code. This module follows the principle of separation of concerns, making the system more maintainable and adaptable.

##### CowrieDBHandler.py
The `CowrieDBHandler.py` class implements specialized database operations for interacting with the Cowrie honeypot database. It encapsulates methods for querying attack data, session information, and attacker behaviors captured by the Cowrie honeypot. This handler provides an abstraction layer over the raw database operations, offering clean interfaces for retrieving and analyzing honeypot data while hiding the complexity of SQL queries and database structure.

##### MonitoringDBHandler.py
The `MonitoringDBHandler.py` module provides functionality for interacting with the monitoring database, which stores analytical data, alerts, and derived security insights. It implements methods for persistence of processed information, trend analysis, and historical attack pattern storage. This component is crucial for the long-term analysis capabilities of the system, enabling statistical analysis and visualization of security event data over time.

##### Scheduler.py
The `Scheduler.py` component implements the core monitoring logic, orchestrating periodic tasks for data collection, analysis, and alert generation. It utilizes both database handlers to extract data from the Cowrie honeypot and persist analytical results. This module manages the execution cycle of the monitoring system, implementing timing strategies, task prioritization, and failure recovery mechanisms to ensure continuous and reliable security monitoring.

# Contributions
Contributions are welcome! If you would like to suggest improvements, report bugs, or add new features, feel free to open an issue or submit a pull request.

# License
This project is licensed under the [MIT License](LICENSE).
