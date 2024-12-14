# VPS Monitoring and Speedtest Dashboard
This project provides a monitoring and speedtest dashboard for monitoring various metrics of a Virtual Private Server (VPS) and running speedtests. It also serves as an API that can be integrated into other projects.

## Features
- CPU Monitoring: Real-time monitoring of CPU usage.
- RAM Monitoring: Real-time monitoring of RAM usage.
- Internet Usage Monitoring: Real-time monitoring of download and upload speeds for an Ethernet interface.
- Speedtest: Run a speedtest to measure current download and upload speeds.
- Data Visualization: Displays metrics in real-time using charts.
- RESTful API: Provides endpoints to fetch CPU, RAM, and internet usage data as JSON.
## Prerequisites
- Python 3.12 or higher
- Flask
- psutil
- speedtest-cli
## Installation
1. Clone the repository: ``https://github.com/LuckyMan612/python-components-use.git``
``cd python-components-use``
2. Start the Flask server: `python main.py`
3. Access the dashboard:
Open a web browser and go to http://localhost:2000 (or replace localhost with your server's IP address).
## Usage
- Dashboard: View real-time charts for CPU usage, RAM usage, and internet usage (download and upload speeds).
- Speedtest: Click on the "Run Speedtest" button to perform a speedtest and see the results displayed on the dashboard.
- API: Use the following endpoints to fetch data:
  - /cpu_data: Get CPU usage data.
  - /ram_data: Get RAM usage data.
  - /internet_data: Get internet usage data (download and upload speeds).
# Sigma
