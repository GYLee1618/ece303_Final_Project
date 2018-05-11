# Written by S. Mevawala, modified by D. Gitzel

import logging

import channelsimulator
import packetgen
import utils

import binascii
import struct

packet_size = (4*1024) - 3 - 16
MAX_SEQNUM = 2**24
ack_size = 1024 -3 - 16

import sys
import socket
import math

class Receiver(object):

    def __init__(self, inbound_port=10001, outbound_port=10000, timeout=.001, debug_level=logging.INFO):
        self.logger = utils.Logger(self.__class__.__name__, debug_level)

        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port,
                                                           debug_level=debug_level)
        self.simulator.rcvr_setup(timeout)
        self.simulator.sndr_setup(timeout)

    def receive(self):
        
        rcv_arr = [0]*MAX_SEQNUM
        sn = 0
        total_rcvd = 0
        is_First = True
        earliest_miss = 0
        #3-way handshake
        #Sender sends out how many packets its going to send
        #Receiver echoes this
        #Sender receives echo, compares. If same, sends ack (all 1's).
        while True:
            try:
                rcv = self.simulator.u_receive()
                signal_length = struct.unpack('>L',rcv[-4:len(rcv)])
                signal_length = signal_length[0]
                self.simulator.u_send(rcv)
                break
            except socket.timeout:
                self.logger.info("timed out")

        rcv_vec = [0] * (signal_length)
        rcv_packets = [bytearray([])]*signal_length
        '''
        rcv = self.simulator.u_receive()
        while rcv[3] == 0: #remember to change this
            self.logger.info('shoop')
            signal_length = rcv[-1]
            self.simulator.u_send(rcv)
            rcv = self.simulator.u_receive()
        '''
        self.logger.info(int(signal_length))
            
        while total_rcvd < signal_length:
            #self.logger.info('Receiving')
            try:
                rcv = bytearray([])

                for i in range(0,4):
                    rcv += self.simulator.u_receive()

               # self.logger.info("Length of packet is {}".format(len(rcv)))
                if packetgen.checkpkt(rcv):
                    tmp = struct.unpack('>L',bytearray([0])+rcv[0:3])
                    #self.logger.info('checksum is good')
                    #self.logger.info(earliest_miss)
                    if rcv_vec[tmp[0]] != 1:    
                        self.logger.info("Receiving {}th packet on port: {} and replying with ACK on port: {}".format(tmp[0],self.inbound_port, self.outbound_port))
                        rcv_packets[tmp[0]] = rcv
                        total_rcvd += 1
                        rcv_vec[tmp[0]] = 1
                        if earliest_miss == tmp[0]:
                            for i in range(earliest_miss,signal_length):
                                if rcv_vec[i] == 0:
                                    earliest_miss = i
                                    break
                                if i == signal_length-1:
                                    earliest_miss = signal_length

                        ACK = packetgen.makepkt(bytearray([1])*ack_size,bytearray.fromhex('{:06x}'.format(earliest_miss)))
                        self.simulator.u_send(ACK)
            except socket.timeout:
                #self.logger.info("timed out")
                ACK = packetgen.makepkt(bytearray([1])*ack_size,bytearray.fromhex('{:06x}'.format(earliest_miss)))
                self.simulator.u_send(ACK)
        
        for i in range(0,signal_length):
            if i == signal_length - 1:
                tmp = bytearray([])
                for byte in rcv_packets[i][3:-16]:
                    if byte == 4:
                        break
                    tmp.append(byte)
                sys.stdout.write(tmp)
            else:
                sys.stdout.write(rcv_packets[i][3:-16])
        self.logger.info('All Done')

class BogoReceiver(Receiver):
    ACK_DATA = bytes(123)

    def __init__(self):
        super(BogoReceiver, self).__init__()

    def receive(self):
        self.logger.info("Receiving on port: {} and replying with ACK on port: {}".format(self.inbound_port, self.outbound_port))
        while True:
            try:
                 data = self.simulator.u_receive()  # receive data
                 self.logger.info("Got data from socket: {}".format(
                     data.decode('ascii')))  # note that ASCII will only decode bytes in the range 0-127
	         sys.stdout.write(data)
                 self.simulator.u_send(BogoReceiver.ACK_DATA)  # send ACK
            except socket.timeout:
                sys.exit()

if __name__ == "__main__":
    rcvr = Receiver()
    rcvr.receive()