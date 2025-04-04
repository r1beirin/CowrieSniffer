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

# Use Cases
* Identifying malicious sources and analyzing the lifespan of attacker-used URLs.
* Integration with Threat Intelligence systems to enhance security databases.

# Contributions
Contributions are welcome! If you would like to suggest improvements, report bugs, or add new features, feel free to open an issue or submit a pull request.

# License
This project is licensed under the [MIT License](LICENSE).
