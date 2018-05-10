# Written by S. Mevawala, modified by D. Gitzel

import logging
import socket
from collections import deque
from random import randint, choice, uniform
from copy import deepcopy

import utils

# region Helper Functions


def random_bytes(n):
    return bytearray([randint(0, 255) for i in xrange(n)])


def slice_frames(data_bytes):
    """
    Slice input into BUFFER_SIZE frames
    :param data_bytes: input bytes
    :return: list of frames of size BUFFER_SIZE
    """
    frames = list()
    num_bytes = len(data_bytes)
    extra = 1 if num_bytes % ChannelSimulator.BUFFER_SIZE else 0

    for i in xrange(num_bytes / ChannelSimulator.BUFFER_SIZE + extra):
        # split data into 1024 byte frames
        frames.append(
            data_bytes[
                i * ChannelSimulator.BUFFER_SIZE:
                i * ChannelSimulator.BUFFER_SIZE + ChannelSimulator.BUFFER_SIZE
            ]
        )
    return frames
# endregion Helper Functions


class ChannelSimulator(object):

    # region Constants

    PROTOCOL_VERSION = 5
    BUFFER_SIZE = 1024
    CORRUPTERS = (0, 1, 2, 4, 8, 16, 32, 64, 128, 255)
    # endregion Constants

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
        self.swap_queue = deque([random_bytes(ChannelSimulator.BUFFER_SIZE), random_bytes(ChannelSimulator.BUFFER_SIZE)])
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

    def corrupt(self, data_bytes, drop_error_prob=0.005, random_error_prob=0.005, swap_error_prob=0.005):
        """
        Corrupt data in the channel with random errors, swaps, and drops.
        In this implementation, random errors will manifest as single byte errors most of the time. Occasionally, an
        entire byte's bits may be flipped.
        Swap errors are implemented via a queue that holds two old frames which are randomly swapped into the channel.
        The queue is initialized with two random frames.
        Drop errors drop the current frame and all the frames "delayed" in the swap queue.

        :param swap_error_prob: swap frame error probability
        :param random_error_prob: random bit error probability
        :param drop_error_prob: drop frame error probability
        :param data_bytes: byte array (frame) to corrupt
        :return: corrupted byte array
        """
        if self.debug:
            logging.debug("Sending bytes through corrupting channel")
        p_error = uniform(0, 1)
        p_swap = uniform(0, 1)
        p_drop = uniform(0, 1)
        corrupted = deepcopy(data_bytes)
        if p_drop < drop_error_prob:
            if self.debug:
                logging.debug("Dropping delayed and swapped frames: {}".format(self.swap_queue))
            # drop all the delayed frames in the swap queue
            self.swap_queue.clear()
            self.swap_queue += [random_bytes(ChannelSimulator.BUFFER_SIZE), random_bytes(ChannelSimulator.BUFFER_SIZE)]
            if self.debug:
                logging.debug("Dropping current frame: {}".format(data_bytes))
            return None
        if p_error < random_error_prob:
            # insert random errors into the frame
            if self.debug:
                logging.debug("Frame before random errors: {}".format(data_bytes))
            for n in xrange(len(data_bytes)):
                # XOR a random corrupter byte to change a single bit, none of the bits, or all the bits
                corrupted[n] ^= choice(ChannelSimulator.CORRUPTERS)
            if self.debug:
                logging.debug("Frame after random errors: {}".format(corrupted))
        if p_swap < swap_error_prob:
            if self.debug:
                logging.debug("Frame before swap: {}".format(data_bytes))
            # swap packets with an earlier packet by popping it off the swap queue
            if p_swap < swap_error_prob / 2:
                corrupted = self.swap_queue.pop()
            else:
                corrupted = self.swap_queue.popleft()
            # store the current packet in the queue
            self.swap_queue.append(data_bytes)
            if self.debug:
                logging.debug("Frame after swap: {}".format(corrupted))
        return corrupted

    def u_send(self, data_bytes):
        """
        Send data through unreliable channel
        :param data_bytes: byte array to send
        :return:
        """

        # split data into 1024 byte frames
        for frame in slice_frames(data_bytes):
            corrupted = self.corrupt(frame)
            # put corrupted frame into socket if it wasn't dropped
            if corrupted:
                self.put_to_socket(corrupted)

    def u_receive(self):
        """
        Receive data through unreliable channel
        :return: byte array of data
        """
        return self.get_from_socket()
