# Written by S. Mevawala, modified by D. Gitzel

import logging

import channelsimulator
import packetgen
import utils

import binascii

packet_size = 1024 - 6 - 32
MAX_SEQNUM = 64

import sys
import socket

class Receiver(object):

    def __init__(self, inbound_port=50005, outbound_port=50006, timeout=10, debug_level=logging.INFO):
        self.logger = utils.Logger(self.__class__.__name__, debug_level)

        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port,
                                                           debug_level=debug_level)
        self.simulator.rcvr_setup(timeout)
        self.simulator.sndr_setup(timeout)

    def receive(self):
        rcv_arr = [0]*MAX_SEQNUM
        exp_sn = 0
        
        signal_length = 0
        
        signal_length_b = self.simulator.u_receive()
        print 'aaaaaa'
        signal_length = packetgen.ba_to_int(signal_length_b)
        self.simulator.u_send(signal_length_b)

        while signal_length == 0:
            signal_length_b = self.simulator.u_receive()
            signal_length = packetgen.ba_to_int(signal_length_b)
            self.simulator.u_send(signal_length_b)

        print signal_length

        while(exp_sn < signal_length):
            rcv_pkt = self.simulator.u_receive(self.simulator)
            if packetgen.checkpkt(rcv_pkt):
                rcv_sn = rcv_pkt[0:int(math.ceil(math.log(MAX_SEQNUM,2)))]
                rcv_arr[rcv_sn] = 1
                data = rcv_pkt[int(math.ceil(math.log(MAX_SEQNUM,2))):len(rcv_pkt)-32]
                self.logger.info("Got data from socket: {}".format(
                     data.decode('ascii')))  # note that ASCII will only decode bytes in the range 0-127
                if rcv_sn == exp_sn:
                    while rcv_arr[exp_sn] == 1:
                        rcv_arr[(exp_sn+3*MAX_SEQNUM/4)%MAX_SEQNUM] = 0
                        exp_sn = (exp_sn + 1) % MAX_SEQNUM
        	sendpkt = exp_sn
        	#generate packet asking for next seq num

        	#NOW send a request for exp_sn packet number
        	rn_packets = packetgen.data_to_packets(exp_sn,packet_size,MAX_SEQNUM)
            self.simulator.u_send(self.simulator,rn_packet[0])








    #def genCheck():		#Generates a checksum for the acknowledgement message.
    					#Send expected sequence number and a checksum for it

    #def sendMessage(seqNum):	#Send a message to sender saying which packet which packet it wants next. Will call genCheck to make checkSum.

    # First take incoming packets and use validPacket(). Return a value 0 for good packet and -1 for bad packet.
    	#If good packet mark that it has been received in receied vector array.
    	#If bad packet don't mark it in the received vector array.
    #Check received vector for the value of first unreceived packet.
    #Use sendMessage to send a request for the the next unreceived packet number (seqNum).



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
    # test out BogoReceiver
    rcvr = Receiver()
    rcvr.receive()