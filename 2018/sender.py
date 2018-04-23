# Written by S. Mevawala, modified by D. Gitzel

import logging
import socket

import channelsimulator
<<<<<<< HEAD
import checksum
=======
import utils
>>>>>>> c7fabdd84265db93c4f623326fbecf613537b087

packet_size = 1024
MAX_SEQNUM = 64

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
        #raise NotImplementedError("The base API class has no implementation. Please override and add your own.")
        num_bytes = 0                                   #number of bytes currently in the packet
        seqnum = 0                                      #sequence number of packet                                  
        for datum in data:
            if num_bytes == 0:
                packet = []
            packet.append(datum)
            if num_bytes == packet_size-1:
                packet.insert(0,bin(seqnum))            #insert sequence number at beginning
                seqnum = (seqnum+1) % MAX_SEQNUM        #increment and divide modulo max sequence number
                chksum = fletch_sum(packet)
                packet.append(bin(chksum))
                ChannelSimulator.u_send(packet)
            num_bytes = (num_bytes + 1) % packet_size   #increment and divide modulo packet size




class BogoSender(Sender):
    TEST_DATA = bytearray([68, 65, 84, 65])  # some bytes representing ASCII characters: 'D', 'A', 'T', 'A'

    def __init__(self):
        super(BogoSender, self).__init__()

    def send(self, data):
        self.logger.info("Sending on port: {} and waiting for ACK on port: {}".format(self.outbound_port, self.inbound_port))
        while True:
            try:
                self.simulator.put_to_socket(data)  # send data
                ack = self.simulator.get_from_socket()  # receive ACK
                self.logger.info("Got ACK from socket: {}".format(
                    ack.decode('ascii')))  # note that ASCII will only decode bytes in the range 0-127
                break
            except socket.timeout:
                pass


if __name__ == "__main__":
    # test out BogoSender
    sndr = BogoSender()
    sndr.send(BogoSender.TEST_DATA)
