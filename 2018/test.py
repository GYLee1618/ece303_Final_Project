import channelsimulator

if __name__ == "__main__":
    # test out corrupt()
    test_data = bytearray([76, 65, 75, 88, 95, 102, 66, 82, 75, 103, 55, 92])
    c = channelsimulator.ChannelSimulator(inbound_port=44444, outbound_port=55555, debug_level=logging.DEBUG)
    print c.corrupt(test_data, drop_error_prob=0, swap_error_prob=0, random_error_prob=1)