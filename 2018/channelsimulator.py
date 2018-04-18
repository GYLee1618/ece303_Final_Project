# Written by S. Mevawala, modified by D. Gitzel

import socket
from random import randint


class ChannelSimulator(object):
    PROTOCOL_VERSION = 2

    def __init__(self, inbound_port, outbound_port, debug, ip_addr="127.0.0.1"):
        self.ip = ip_addr
        self.sndr_socket = None
        self.rcvr_socket = None
        self.swap = None
        self.swap_bool = False
        self.debug = debug

        self.sndr_port = outbound_port
        self.rcvr_port = inbound_port

    # Log internal program state during DEBUG
    def log(self, message):
        if self.debug:
            print(message)

    # Setup the sender socket
    def sndr_setup(self, time):
        self.sndr_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sndr_socket.settimeout(time)

    # Setup the receiver socket
    def rcvr_setup(self, time):
        self.rcvr_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rcvr_socket.bind((self.ip, self.rcvr_port))
        self.rcvr_socket.settimeout(time)

    # Put bits to the socket
    def put_to_socket(self, bits):
        bitstring = bits[2:]
        # bitarray=array.array('i', (0 for i in range ( 0, len(bitstring)/8)))
        b_array = bytearray()
        for n in xrange(0, len(bitstring) / 8):
            b_array.append(int(bitstring[(n * 8):((n * 8) + 8)], 2))
        self.sndr_socket.sendto(b_array, (self.ip, self.sndr_port))

    # Get bits from the socket
    def get_from_socket(self):
        while True:
            data, address = self.rcvr_socket.recvfrom(1024)  # buffer size is 1024 bytes
            b_array = bytearray(data)
            bitstring = "0b"
            for n in xrange(0, len(b_array)):
                bitstring += (bin(b_array[n])[2:].zfill(8))
            return bitstring

    # Corrupt bits in the channel (random, swap, and drop errors)
    def corrupt(self, bits):
        self.log("Sending bits through corrupting channel")
        random_errors = randint(0, 5000)
        swap = randint(0, 5000)
        drop = randint(0, 5000)
        if random_errors <= 10:
            self.log("Bits before swap: " + bits)
            bit_list = list(bits[2:])
            for n in xrange(0, randint(0, len(bit_list) / 3)):
                bit_list[randint(3, len(bit_list)) - 1] = str(randint(0, 1))
            bits = ''.join(bit_list)
            self.log("Bits before swap: " + bits)
        if swap < 10:
            self.swap_bool = True
            self.swap = bits
            return
        if drop <= 10:
            return
        return bits

    # Unreliable Send
    def u_send(self, bits):
        self.put_to_socket(self.corrupt(bits))

    # Unreliable Receive
    def u_receive(self):
        return self.get_from_socket()
