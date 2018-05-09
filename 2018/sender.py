#!
# Written by S. Mevawala, modified by D. Gitzel

import logging
import socket

import channelsimulator

import packetgen
import utils
import time

packet_size = 1024 - 6 - 32
MAX_SEQNUM = 64

import sys

class Sender(object):

    def __init__(self, inbound_port=50006, outbound_port=50005, timeout=10, debug_level=logging.INFO):
        self.logger = utils.Logger(self.__class__.__name__, debug_level)

        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port,
                                                           debug_level=debug_level)
        self.simulator.sndr_setup(timeout)
        self.simulator.rcvr_setup(timeout)

    def send(self, data):
        packets = packetgen.data_to_packets(data,packet_size,MAX_SEQNUM)
        print len(packets)
        signal_length = bytearray.fromhex('{:0256x}'.format(len(packets)))
        
        rcv = [0]
        self.simulator.u_send(signal_length)
        #rcv = self.simulator.u_receive()
        print packetgen.ba_to_int(rcv)
        
        while rcv != signal_length:
            self.simulator.u_send(signal_length)
            rcv = self.simulator.u_receive()

        for i in range(0,len(packets)):
            received = False
            
            while not received:
                #print "sending"
                self.simulator.u_send(packets[i])
                try:
                    rcv_pkt = self.simulator.u_receive()
                    if packetgen.checkpkt(rcv_pkt):
                        #if packetgen.get_data(rcv_pkt,packet_size,MAX_SEQNUM) == (i+1) % MAX_SEQNUM:
                        received = True
                except socket.timeout:
                    self.logger.info("timed out")


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
    
    DATA = channelsimulator.random_bytes(1024)
    sndr.send(DATA)

    # test out BogoSender
    DATA = channelsimulator.random_bytes(1024)
    sndr = BogoSender()
    sndr.send(DATA)
