import channelsimulator


class BogoReceiver(object):

    def __init__(self):
        super(self, BogoReceiver).__init__()
        self.simulator = channelsimulator.ChannelSimulator(False)  # False for receiver
        self.simulator.rcvr_setup()
        self.simulator.sndr_setup()

    def receive(self):
        while True:
            print self.simulator.u_receive()  # receive data
            self.simulator.u_send(bin(123))  # send ACK


if __name__ == "__main__":
    rcvr = BogoReceiver()
    rcvr.receive()
