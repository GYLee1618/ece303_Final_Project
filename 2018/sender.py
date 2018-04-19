# Written by S. Mevawala, modified by D. Gitzel

import socket
import channelsimulator
import checksum

packet_size = 1024
MAX_SEQNUM = 64

class Sender(object):

    def __init__(self, inbound_port=50006, outbound_port=50005, timeout=10, debug=False):
        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port, debug=debug)
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
                packet.insert(0,seqnum)                 #insert sequence number at beginning
                seqnum = (seqnum+1) % MAX_SEQNUM        #increment and divide modulo max sequence number
                
                ChannelSimulator.u_send(packet)
            num_bytes = (num_bytes + 1) % packet_size   #increment and divide modulo packet size




class BogoSender(Sender):

    def __init__(self):
        super(BogoSender, self).__init__()

    def send(self, data):
        print("Sending on port: {} and waiting for ACK on port: {}".format(self.inbound_port, self.outbound_port))
        while True:
            try:
                self.simulator.u_send(data)  # send data
                ack = self.simulator.u_receive()  # receive ACK
                print(ack)
                break
            except socket.timeout:
                pass


if __name__ == "__main__":
    # test out BogoSender
    sndr = BogoSender()
    sndr.send(bin(2344))
