HEAD
# Written by S. Mevawala, modified by D. Gitzel

import logging

import channelsimulator
import packetgen
import utils

MAX_SEQNUM = 64

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
        ended = False
        while(!ended):
        	rcv_pkt = channelcimulator.ChannelSimulator.u_receive(self.simulator)
        	if ckeckpkt(rcv_pkt):
        		rcv_sn = rcv_pkt[2:2+int(math.ceil(math.log(MAX_SEQNUM,2)))]
        		rcv_arr[rcv_sn] = 1
	        	if rcv_sn == exp_sn:
	        		while rcv_arr[exp_sn] == 1:
	        			rcv_arr[(exp_sn+3*MAX_SEQNUM/4)%MAX_SEQNUM] = 0
	        			exp_sn++ % MAX_SEQNUM
        			sendpkt = exp_sn
        			#generate packet asking for next seq num
        	else:
        		sendpkt = -exp_sn

        	#NOW send a request for exp_sn packet number
        	packetgen(expsn)






    def genCheck():		#Generates a checksum for the acknowledgement message.
    					#Send expected sequence number and a checksum for it

    def sendMessage(seqNum):	#Send a message to sender saying which packet which packet it wants next. Will call genCheck to make checkSum.

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
            data = self.simulator.get_from_socket()  # receive data
            self.logger.info("Got data from socket: {}".format(
                data.decode('ascii')))  # note that ASCII will only decode bytes in the range 0-127
            self.simulator.put_to_socket(BogoReceiver.ACK_DATA)  # send ACK


if __name__ == "__main__":
    # test out BogoReceiver
    rcvr = BogoReceiver()
    rcvr.receive()