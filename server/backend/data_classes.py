import numpy as np
import struct

class cBool:
    def read(self, packet):
        return (bool(packet[0]), packet[1:])

    def build(self, value):
        value = bool(value)
        if value:
            return (1).to_bytes(1, byteorder='big')
        else:
            return (0).to_bytes(1, byteorder='big')

class cByte:
    def read(self, packet):
        return (packet[0], packet[1:])

    def build(self, value):
        return value.to_bytes(1, byteorder='big', signed=True)

class cShort:
    def read(self, packet):
        return (struct.unpack('>h', packet[:2])[0], packet[2:])

    def build(self, value):
        return value.to_bytes(2, byteorder='big', signed=True)

class cInt:
    def read(self, packet):
        return (int.from_bytes(packet[:4], byteorder="big", signed=True), packet[4:])

    def build(self, value):
        return value.to_bytes(4, byteorder='big', signed=True)

class cFloat:
    def read(self, packet):
        return (struct.unpack('>f', packet[:4])[0], packet[4:])

    def build(self, value):
        packet = bytearray(struct.pack(">f", np.float32(value)))
        return bytes(packet)


class cDouble:
    def read(self, packet):
        return (struct.unpack('>d', packet[:8])[0], packet[8:])

    def build(self, value):
        packet = bytearray(struct.pack(">d", np.float64(value)))
        return bytes(packet)

class cString:
    def read(self, packet):
        length, rest = (struct.unpack('>h', packet[:2])[0], packet[2:])
        string = rest[:length]
        return (string.decode("UTF-8"), rest[length:])

    def build(self, value):
        length = len(value)
        encoded = value.encode('UTF-8')
        varIntLen = length.to_bytes(2, byteorder='big', signed=True)
        packet = bytearray()
        packet.extend(varIntLen)
        packet.extend(encoded)
        return bytes(packet)
    