import struct

# Ten plik został wygenerowany automatycznie. Nie edytuj go ręcznie!

class SensorData:
    def __init__(self, sensor_id, temperature, is_active):
        
        self.sensor_id = sensor_id
        
        self.temperature = temperature
        
        self.is_active = is_active
        

    def serialize(self):
        # Pakowanie danych do formatu binarnego. Użyty format: if?
        return struct.pack('if?', self.sensor_id, self.temperature, self.is_active)

    @staticmethod
    def deserialize(data):
        # Rozpakowywanie danych z formatu binarnego
        unpacked = struct.unpack('if?', data)
        return SensorData(*unpacked)
    