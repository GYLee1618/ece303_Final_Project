# Written by S. Mevawala, modified by D. Gitzel

import socket
import channelsimulator


class Sender(object):

    def __init__(self, inbound_port=50006, outbound_port=50005, timeout=10, debug=False):
        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port, debug=debug)
        self.simulator.sndr_setup(timeout)
        self.simulator.rcvr_setup(timeout)

    def send(self, data):
        raise NotImplementedError("The base API class has no implementation. Please override and add your own.")


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
