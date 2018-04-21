# Written by S. Mevawala, modified by D. Gitzel

import channelsimulator
import logging


class Receiver(object):

    def __init__(self, inbound_port=50005, outbound_port=50006, timeout=10, debug=logging.INFO):
        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port,
                                                           debug_level=debug)
        self.simulator.rcvr_setup(timeout)
        self.simulator.sndr_setup(timeout)

    def receive(self):
        raise NotImplementedError("The base API class has no implementation. Please override and add your own.")


class BogoReceiver(Receiver):
    ACK_DATA = bytes(123)

    def __init__(self):
        super(BogoReceiver, self).__init__()

    def receive(self):
        print("Receiving on port: {} and replying with ACK on port: {}".format(self.inbound_port, self.outbound_port))
        while True:
            data = self.simulator.get_from_socket()  # receive data
            print "Got data from socket: {}".format(
                data.decode('ascii'))  # note that ASCII will only decode bytes in the range 0-127
            self.simulator.put_to_socket(BogoReceiver.ACK_DATA)  # send ACK


if __name__ == "__main__":
    # test out BogoReceiver
    rcvr = BogoReceiver()
    rcvr.receive()
