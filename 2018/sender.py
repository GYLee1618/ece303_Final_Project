#!
# Written by S. Mevawala, modified by D. Gitzel

import logging
import socket

import channelsimulator

import packetgen
import utils
import time

packet_size = (32*1024) - 3 - 16
MAX_SEQNUM = 2**24

import sys

class Sender(object):

    def __init__(self, inbound_port=10000, outbound_port=10001, timeout=1, debug_level=logging.INFO):
        self.logger = utils.Logger(self.__class__.__name__, debug_level)

        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port,
                                                           debug_level=debug_level)
        self.simulator.sndr_setup(timeout)
        self.simulator.rcvr_setup(timeout)

    def send(self, data):
        
        packets = packetgen.data_to_packets(data,packet_size,MAX_SEQNUM)
        
        #3-way handshake
        #Sender sends out how many packets its going to send
        #Receiver echoes this
        #Sender receives echo, compares. If same, sends ack (all 1's).

        signal_length = bytearray.fromhex('{:0256x}'.format(len(packets)))
        self.simulator.u_send(signal_length)

        self.logger.info(len(packets))
        rcv = self.simulator.u_receive()

        while not(rcv == signal_length):
            self.simulator.u_send(signal_length)
            rcv = self.simulator.u_receive()

        for i in range(0,len(packets)):
            received = False
            
            while not received:
                self.logger.info('Sending packet {}'.format(i))
                self.simulator.u_send(packets[i])
                try:
                    rcv_pkt = bytearray([])

                    for j in range(0,32):
                        rcv_pkt += self.simulator.u_receive()

                    if packetgen.checkpkt(rcv_pkt):
                        self.logger.info("chksum good")
                        if rcv_pkt[50] == 1 and rcv_pkt[0:3] == packets[i][0:3]:
                            received = True
                            self.logger.info("Got ACK from socket")  # note that ASCII will only decode bytes in the range 0-127

                except socket.timeout:
                    self.logger.info("timed out")
        self.logger.info('Done Sending')
        



class BogoSender(Sender):

    def __init__(self):
        super(BogoSender, self).__init__()

    def send(self, data):
        self.logger.info("Sending on port: {} and waiting for ACK on port: {}".format(self.outbound_port, self.inbound_port))
        while True:
            try:
                self.simulator.u_send(data)  # send data
                ack = self.simulator.u_receive()  # receive ACK
                self.logger.info("Got ACK from socket: {}".format(
                    ack.decode('ascii')))  # note that ASCII will only decode bytes in the range 0-127
                break
            except socket.timeout:
                pass


if __name__ == "__main__":
    # test out Sender

    sndr = Sender()
    
    DATA = bytearray(sys.stdin.read())

    sndr.send(DATA)

    # test out BogoSender
    #DATA = channelsimulator.random_bytes(1024)
    #sndr = BogoSender()
    #sndr.send(DATA)
