from chatbox.data_classes import *

bool_ = cBool()
byte_ = cByte()
short_ = cShort()
int_ = cInt()
float_ = cFloat()
double_ = cDouble()
string_ = cString()

class Packet:
    def __init__(self, data_arry):
        self._store = data_arry

    def read(self, packet):
        out = []
        rest = packet
        for data in self._store:
            point, rest = data.read(rest)
            out.append(point)
        return out, rest

    def build(self, *args):
        out = bytearray()
        for i in range(len(args)):
            data = self._store[i].build(args[i])
            out.extend(data)
        return out

__all__ = ['bool_', 'byte_', 'short_', 'int_', 'float_', 'double_', 'string_', 'Packet']