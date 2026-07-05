import socket
import time
# Importujemy nasz WYGENEROWANY plik protocol.py
from protocol import SensorData

def start_client():
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        # Tworzymy obiekt przy użyciu wygenerowanej klasy
        my_sensor_data = SensorData(sensor_id=42, temperature=23.5, is_active=True)
        
        # Używamy wygenerowanej metody serialize do zamiany na kod binarny!
        binary_data = my_sensor_data.serialize()
        
        print("Wysyłam zserializowane dane binarne do serwera...")
        s.sendall(binary_data)
        time.sleep(1) # Czekamy chwilę przed zamknięciem

if __name__ == "__main__":
    start_client()
