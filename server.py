import socket
# Importujemy nasz WYGENEROWANY plik protocol.py
from protocol import SensorData

def start_server():
    host = '127.0.0.1'
    port = 65432

    # Tworzymy gniazdo TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Serwer nasłuchuje na {host}:{port}...")
        
        conn, addr = s.accept()
        with conn:
            print(f"Połączono z {addr}")
            while True:
                data = conn.recv(1024) # Odbieranie bajtów
                if not data:
                    break
                
                # Używamy wygenerowanej metody deserialize!
                sensor_obj = SensorData.deserialize(data)
                
                print("Odebrano i zdeserializowano dane:")
                print(f"- ID czujnika: {sensor_obj.sensor_id}")
                print(f"- Temperatura: {sensor_obj.temperature}°C")
                print(f"- Czy aktywny: {sensor_obj.is_active}")

if __name__ == "__main__":
    start_server()