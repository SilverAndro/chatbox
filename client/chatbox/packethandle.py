from chatbox.packets import *


class Protocol:
    def __init__(self):
        self.match = {
            # Connection request
            # Username
            b'\x00': Packet([string_]),

            # Connection response
            # Allowed
            b'\x01': Packet([bool_]),

            # Message send request
            # Message to send
            b'\x02': Packet([string_]),

            # Inbound message
            # Username, message, important
            b'\x03': Packet([string_, string_, bool_]),

            # Server close
            # Manual
            b'\xfe': Packet([bool_]),

            # Kick
            # Reason
            b'\xff': Packet([string_]),
        }

    def read(self, packet):
        packet_id, rest = packet[0], packet[1:]
        packet_id = bytes([packet_id])
        if packet_id in self.match.keys():
            func = self.match[packet_id]
            data, rest = func.read(rest)
            return data, rest
        else:
            raise IOError("Unknown packet ID on read")

    def build(self, packet_id, *args):
        if packet_id in self.match.keys():
            func = self.match[packet_id]
            packet = bytearray()
            packet.extend(packet_id)
            packet.extend(func.build(*args))
            return packet
        else:
            raise IOError("Unknown packet ID on build")