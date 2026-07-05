import struct

# Ten plik został wygenerowany automatycznie. Nie edytuj go ręcznie!

class SensorData:
    def __init__(self, sensor_id, temperature, is_active, history):
        
        self.sensor_id = sensor_id
        
        self.temperature = temperature
        
        self.is_active = is_active
        
        self.history = history
        

    def serialize(self):
        payload = bytearray()
        
        
        payload += struct.pack('i', self.sensor_id)
        
        
        
        payload += struct.pack('f', self.temperature)
        
        
        
        payload += struct.pack('?', self.is_active)
        
        
        
        if self.history is None:
            self.history = []
        payload += struct.pack('I', len(self.history))
        for item in self.history:
            payload += struct.pack('i', item)
        
        
        return bytes(payload)

    @staticmethod
    def deserialize(data):
        offset = 0
        values = {}
        
        
        value, = struct.unpack_from('i', data, offset)
        offset += struct.calcsize('i')
        values['sensor_id'] = value
        
        
        
        value, = struct.unpack_from('f', data, offset)
        offset += struct.calcsize('f')
        values['temperature'] = value
        
        
        
        value, = struct.unpack_from('?', data, offset)
        offset += struct.calcsize('?')
        values['is_active'] = value
        
        
        
        count, = struct.unpack_from('I', data, offset)
        offset += struct.calcsize('I')
        values['history'] = []
        for _ in range(count):
            item, = struct.unpack_from('i', data, offset)
            offset += struct.calcsize('i')
            values['history'].append(item)
        
        
        return SensorData(**values)