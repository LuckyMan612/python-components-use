import psutil
import time
from datetime import datetime, timedelta
from threading import Thread
from flask import Flask, render_template, jsonify
import speedtest

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

# Stała definiująca maksymalny czas przechowywania danych (24 godziny)
MAX_DATA_AGE = timedelta(hours=24)

# Lista do przechowywania danych
cpu_data = []
ram_data = []
download_data = []
upload_data = []
previous_recv = psutil.net_io_counters().bytes_recv
previous_sent = psutil.net_io_counters().bytes_sent

# Funkcja monitorująca zużycie CPU
def monitor_cpu():
    global cpu_data
    while True:
        cpu_percent = psutil.cpu_percent()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cpu_data.append((timestamp, cpu_percent))
        # Usuwanie starszych danych
        cpu_data = [(t, p) for t, p in cpu_data if datetime.strptime(t, '%Y-%m-%d %H:%M:%S') > datetime.now() - MAX_DATA_AGE]
        time.sleep(1)

# Wątek do monitorowania CPU
cpu_thread = Thread(target=monitor_cpu)
cpu_thread.start()

# Funkcja monitorująca zużycie RAM
def monitor_ram():
    global ram_data
    while True:
        ram_percent = psutil.virtual_memory().percent
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ram_data.append((timestamp, ram_percent))
        # Usuwanie starszych danych
        ram_data = [(t, p) for t, p in ram_data if datetime.strptime(t, '%Y-%m-%d %H:%M:%S') > datetime.now() - MAX_DATA_AGE]
        time.sleep(1)

# Wątek do monitorowania RAM
ram_thread = Thread(target=monitor_ram)
ram_thread.start()

def monitor_internet():
    global download_data, upload_data, previous_recv, previous_sent
    
    while True:
        current_recv = psutil.net_io_counters().bytes_recv
        current_sent = psutil.net_io_counters().bytes_sent
        
        download_speed = (current_recv - previous_recv) / 100000  # przeliczenie na Mbps
        upload_speed = (current_sent - previous_sent) / 100000  # przeliczenie na Mbps
        
        if download_speed > 0 or upload_speed > 0:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            download_data.append((timestamp, download_speed))
            upload_data.append((timestamp, upload_speed))
            
            previous_recv = current_recv
            previous_sent = current_sent
        
        time.sleep(1)  # sprawdzanie co sekundę

# Wątek do monitorowania internetu
internet_thread = Thread(target=monitor_internet)
internet_thread.start()

# Endpoint do zwracania danych o CPU w formacie JSON
@app.route('/cpu_data', methods=['GET'])
def get_cpu_data():
    global cpu_data
    return jsonify(cpu_data)

# Endpoint do zwracania danych o RAM w formacie JSON
@app.route('/ram_data', methods=['GET'])
def get_ram_data():
    global ram_data
    return jsonify(ram_data)

# Endpoint do zwracania danych o zużyciu internetu w formacie JSON
@app.route('/internet_data', methods=['GET'])
def get_internet_data():
    global download_data, upload_data
    return jsonify({
        'download': download_data,
        'upload': upload_data
    })

# Endpoint do renderowania strony z wykresami
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint do wykonania speedtestu
@app.route('/speedtest', methods=['POST'])
def run_speedtest():
    global download_data, upload_data
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1e6  # Mbps
    upload_speed = st.upload() / 1e6  # Mbps
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    download_data.append((timestamp, download_speed))
    upload_data.append((timestamp, upload_speed))
    
    # Usuwanie starszych danych
    download_data = [(t, d) for t, d in download_data if datetime.strptime(t, '%Y-%m-%d %H:%M:%S') > datetime.now() - MAX_DATA_AGE]
    upload_data = [(t, u) for t, u in upload_data if datetime.strptime(t, '%Y-%m-%d %H:%M:%S') > datetime.now() - MAX_DATA_AGE]
    
    return jsonify({
        'download_speed': download_speed,
        'upload_speed': upload_speed
    })

# Uruchomienie aplikacji Flask na porcie 2000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000)
