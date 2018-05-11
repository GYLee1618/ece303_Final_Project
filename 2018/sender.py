#!
# Written by S. Mevawala, modified by D. Gitzel

import logging
import socket

import channelsimulator

import packetgen
import utils
import time

packet_size = (4*1024) - 3 - 16
MAX_SEQNUM = 2**24

import sys
import struct

class Sender(object):

    def __init__(self, inbound_port=10000, outbound_port=10001, timeout=.001, debug_level=logging.INFO):
        self.logger = utils.Logger(self.__class__.__name__, debug_level)

        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port,
                                                           debug_level=debug_level)
        self.simulator.sndr_setup(timeout)
        self.simulator.rcvr_setup(timeout)

    def send(self, data):
        
        packets = packetgen.data_to_packets(data,packet_size,MAX_SEQNUM)
        
        rcv_vec = [0]*len(packets)
        done = [1]*len(packets)
        max_rcv = 0
        #3-way handshake
        #Sender sends out how many packets its going to send
        #Receiver echoes this
        #Sender receives echo, compares. If same, sends ack (all 1's).

        signal_length = bytearray.fromhex('{:0256x}'.format(len(packets)))
        self.simulator.u_send(signal_length)

        time.sleep(.5)
        self.logger.info(len(packets))
        rcv = self.simulator.u_receive()

        while not(rcv == signal_length):
            self.simulator.u_send(signal_length)
            rcv = self.simulator.u_receive()
        for i in range(0,len(packets),4):
            for j in range(0,4):
                t = j
                if i+j >= len(packets):
                    break
                #self.logger.info('Sending packet {}'.format(i+j))
                self.simulator.u_send(packets[i+j])
            
            while max_rcv < min(i+4,len(packets)):
                #self.logger.info([max_rcv,len(packets)])
                try:     
                    rcv_pkt = self.simulator.u_receive()

                    if packetgen.checkpkt(rcv_pkt):
                        #self.logger.info("chksum good")
                        tmp = struct.unpack('>L',bytearray([0])+rcv_pkt[0:3])
                        if tmp[0] > max_rcv:
                            max_rcv = tmp[0]

                except socket.timeout:
                   # self.logger.info(max_rcv)
                    if max_rcv < len(packets):
                        self.logger.info('Sending packet {}'.format(max_rcv))
                        self.simulator.u_send(packets[max_rcv])

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
