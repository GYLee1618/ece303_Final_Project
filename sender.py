import socket

import channelsimulator


class BogoSender(object):

    def __init__(self):
        super(self, BogoSender).__init__()
        self.simulator = channelsimulator.ChannelSimulator(True)  # False for receiver
        self.simulator.sndr_setup(1)
        self.simulator.rcvr_setup(1)

    def send(self):
        while True:
            try:
                self.simulator.u_send(bin(2344))  # send data
                ack = self.simulator.u_receive()  # receive ACK
                print ack
                break
            except socket.timeout:
                pass


if __name__ == "__main__":
    sndr = BogoSender()
    sndr.send()

