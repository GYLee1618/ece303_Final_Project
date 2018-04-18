import channelsimulator

class Receiver(object):

    def __init__(self, inbound_port=50005, outbound_port=50006, timeout=10, debug=False):
        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port, debug=debug)
        self.simulator.rcvr_setup(timeout)
        self.simulator.sndr_setup(timeout)

    def receive(self):
        raise NotImplementedError("The base API class has no implementation. Please override and add your own.")

    def validPacket():	#Checks the checksum of the packet to make sure the data wasn't corrupted.

    def genCheck():		#Generates a checksum for the acknowledgement message.

    def sendMessage(seqNum):	#Send a message to sender saying which packet which packet it wants next. Will call genCheck to make checkSum.

    # First take incoming packets and use validPacket(). Return a value 0 for good packet and -1 for bad packet.
    	#If good packet mark that it has been received in receied vector array.
    	#If bad packet don't mark it in the received vector array.
    #Check received vector for the value of first unreceived packet.
    #Use sendMessage to send a request for the the next unreceived packet number (seqNum).



class BogoReceiver(Receiver):
    ACK_DATA = bin(123)

    def __init__(self):
        super(BogoReceiver, self).__init__()

    def receive(self):
        print("Receiving on port: {} and replying with ACK on port: {}".format(self.inbound_port, self.outbound_port))
        while True:
            print self.simulator.u_receive()  # receive data
            self.simulator.u_send(BogoReceiver.ACK_DATA)  # send ACK


if __name__ == "__main__":
    # test out BogoReceiver
    rcvr = BogoReceiver()
    rcvr.receive()