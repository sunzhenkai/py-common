# coding: utf-8
from time import sleep
import unittest
from tools.perf_counter import Timer


class TestTimer(unittest.TestCase):
    def test_timer(self):
        with Timer() as tm:
            sleep(1)
        print(f"elapsed: {tm.elapsed}")


if __name__ == "__main__":
    unittest.main()
