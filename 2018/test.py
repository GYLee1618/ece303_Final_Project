import logging
import unittest
from copy import deepcopy

from channelsimulator import ChannelSimulator


class TestChannelSimulator(unittest.TestCase):
    @staticmethod
    def setup_channel():
        return ChannelSimulator(inbound_port=44444, outbound_port=55555, debug_level=logging.DEBUG)

    @staticmethod
    def get_test_bytes(n):
        return bytearray([65] * n)

    def test_slice_frames(self):
        c = self.setup_channel()
        frames = c.slice_frames(self.get_test_bytes(4 * ChannelSimulator.BUFFER_SIZE))
        assert len(frames) == 4
        for f in frames:
            assert len(f) == ChannelSimulator.BUFFER_SIZE

    def test_corrupt_none(self):
        c = self.setup_channel()
        test_data = self.get_test_bytes(ChannelSimulator.BUFFER_SIZE)
        corrupted_bytes = c.corrupt(test_data, drop_error_prob=0, swap_error_prob=0, random_error_prob=0)
        assert test_data == corrupted_bytes

    def test_corrupt_drop(self):
        c = self.setup_channel()
        test_data = self.get_test_bytes(ChannelSimulator.BUFFER_SIZE)
        corrupted_bytes = c.corrupt(test_data, drop_error_prob=1, swap_error_prob=0, random_error_prob=0)
        assert corrupted_bytes is None

    def test_corrupt_swap(self):
        c = self.setup_channel()
        test_data = self.get_test_bytes(ChannelSimulator.BUFFER_SIZE)
        swapped = deepcopy(c.swap)
        corrupted_bytes = c.corrupt(test_data, drop_error_prob=0, swap_error_prob=1, random_error_prob=0)
        assert corrupted_bytes in swapped

    def test_corrupt_random(self):
        c = self.setup_channel()
        test_data = self.get_test_bytes(ChannelSimulator.BUFFER_SIZE)
        corrupted_bytes = c.corrupt(test_data, drop_error_prob=0, swap_error_prob=0, random_error_prob=1)
        assert test_data != corrupted_bytes


if __name__ == "__main__":
    unittest.main()
