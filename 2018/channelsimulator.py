# Written by S. Mevawala, modified by D. Gitzel

import logging
import socket
from collections import deque
from random import randint, choice, uniform

import utils


def random_bytes(n):
    return bytearray([randint(0, 225) for i in xrange(n)])


class ChannelSimulator(object):
    PROTOCOL_VERSION = 3
    BUFFER_SIZE = 1024
    CORRUPTERS = (0, 1, 2, 4, 8, 16, 32, 64, 128, 255)
    FRAME_HEADER = bytearray([170, 170, 170, 170, 170, 170, 170, 171])

    def __init__(self, inbound_port, outbound_port, debug_level=logging.INFO, ip_addr="127.0.0.1"):
        """
        Create a ChannelSimulator
        :param inbound_port: port number for inbound connections
        :param outbound_port: port number of outbound connections
        :param debug_level: debug level for logging (e.g. logging.DEBUG)
        :param ip_addr: destination IP
        """

        self.ip = ip_addr
        self.sndr_socket = None
        self.rcvr_socket = None
        self.swap = deque([random_bytes(ChannelSimulator.BUFFER_SIZE), random_bytes(ChannelSimulator.BUFFER_SIZE)])
        self.debug = debug_level == logging.DEBUG
        if self.debug:
            self.logger = utils.Logger(self.__class__.__name__, debug_level)
        else:
            self.logger = None

        self.sndr_port = outbound_port
        self.rcvr_port = inbound_port

    def sndr_setup(self, timeout):
        """
        Setup the sender socket
        :param timeout: time out value to use, in seconds
        :return:
        """
        self.sndr_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sndr_socket.settimeout(timeout)

    def rcvr_setup(self, timeout):
        """
        Setup the receiver socket
        :param timeout: time out value to use, in seconds
        :return:
        """
        self.rcvr_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rcvr_socket.bind((self.ip, self.rcvr_port))
        self.rcvr_socket.settimeout(timeout)

    def put_to_socket(self, data_bytes):
        """
        (INTERNAL) Put data to the socket
        :param data_bytes: byte array to send to socket
        :return:
        """
        self.sndr_socket.sendto(data_bytes, (self.ip, self.sndr_port))

    def get_from_socket(self):
        """
        (INTERNAL) Get data from socket
        :return: bit string of data from the socket
        """
        while True:
            data, address = self.rcvr_socket.recvfrom(ChannelSimulator.BUFFER_SIZE)  # buffer size is 1024 bytes
            return bytearray(data)

    def corrupt(self, data_bytes, drop_error_prob=0.002, random_error_prob=0.002, swap_error_prob=0.002):
        """
        Corrupt data in the channel with random errors, swaps, and drops.
        :param swap_error_prob: swap frame error probability
        :param random_error_prob: random bit error probability
        :param drop_error_prob: drop frame error probability
        :param data_bytes: byte array (frame) to corrupt
        :return: corrupted byte array
        """
        if self.debug:
            logging.debug("Sending bytes through corrupting channel")
        random_errors = uniform(0, 1)
        swap = uniform(0, 1)
        drop = uniform(0, 1)
        corrupted = bytearray(len(data_bytes))
        if drop < drop_error_prob:
            if self.debug:
                logging.debug("Dropping delayed and swapped frames: {}".format(self.swap))
            self.swap.clear()
            self.swap += [random_bytes(ChannelSimulator.BUFFER_SIZE), random_bytes(ChannelSimulator.BUFFER_SIZE)]
            if self.debug:
                logging.debug("Dropping current frame: {}".format(data_bytes))
            return
        if random_errors < random_error_prob:
            if self.debug:
                logging.debug("Frame before random errors: {}".format(data_bytes))
            for n in xrange(len(data_bytes)):
                corrupted[n] = data_bytes[n] ^ choice(ChannelSimulator.CORRUPTERS)
            if self.debug:
                logging.debug("Frame after random errors: {}".format(corrupted))
        if swap < swap_error_prob:
            if self.debug:
                logging.debug("Frame before swap: {}".format(data_bytes))
            if swap < swap_error_prob / 2:
                corrupted = self.swap.pop()
            else:
                corrupted = self.swap.popleft()
            self.swap.append(data_bytes)
            if self.debug:
                logging.debug("Frame after swap: {}".format(corrupted))
        return corrupted

    def slice_frames(self, data_bytes):
        """
        Slice input into BUFFER_SIZE frames
        :param data_bytes: input bytes
        :return: list of frames of size BUFFER_SIZE
        """
        frames = list()
        num_bytes = len(data_bytes)

        for i in xrange(num_bytes / ChannelSimulator.BUFFER_SIZE):
            # split data into 1024 byte frames
            frames.append(
                data_bytes[
                i * ChannelSimulator.BUFFER_SIZE:
                i * ChannelSimulator.BUFFER_SIZE + ChannelSimulator.BUFFER_SIZE]
            )
        return frames

    def u_send(self, data_bytes):
        """
        Send data through unreliable channel
        :param data_bytes: byte array to send
        :return:
        """

        # split data into 1024 byte frames
        for frame in self.slice_frames(data_bytes):
            self.put_to_socket(self.corrupt(frame))

    def u_receive(self):
        """
        Receive data through unreliable channel
        :return: byte array of data
        """
        return self.get_from_socket()
