#!
# Written by S. Mevawala, modified by D. Gitzel

import logging
import socket

import channelsimulator

import packetgen
#=======
import utils
#>>>>>>> c7fabdd84265db93c4f623326fbecf613537b087

packet_size = 1024 - 6 - 32
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
        packets = packetgen.data_to_packets(data,packet_size,MAX_SEQNUM)

        signal_length = bin(len(packets))
        print signal_length
        len_pkt = packetgen.data_to_packets(signal_length,packet_size,MAX_SEQNUM)
        channelsimulator.ChannelSimulator.u_send(self.simulator,len_pkt[0])

        for i in range(0,len(packets)):
            received = False
            
            while not received:
                channelsimulator.ChannelSimulator.u_send(self.simulator,packets[i])
                try:
                    rcv_pkt = channelsimulator.ChannelSimulator.u_receive(self.simulator)
                    if packetgen.checkpkt(rcv_pkt):
                        if packetgen.get_data(rcv_pkt,packet_size,MAX_SEQNUM) == (i+1) % MAX_SEQNUM:
                            received = True
                except socket.timeout:
                    logging.debug("timed out")


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
    # test out Sender
    sndr = Sender()
    st = raw_input('Message: ')
    bst = '0b'+''.join('{0:08b}'.format(ord(x), 'b') for x in st)

    sndr.send(bst)