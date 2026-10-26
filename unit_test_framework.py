"""TRNG Unit test framework; will modify as TRNG is implemented to use its values instead
of PRNG values"""

import unittest
import random
import time
import numpy as np
from scipy import stats
# import other modules as needed once added to TRNG; using PRNG as a placeholder

class TestFramework(unittest.TestCase):
    """Unit test framework for TRNG; will modify as TRNG is implemented to use its values"""
    def test_stat_threshold(self):
        """Framework test case for checking p-value threshold;
        modify to use values from external sources"""
        p_val = 0.04
        alpha = 0.05
        self.assertLess(p_val, alpha, "p-value is greater than alpha threshold, test failed.")

    def test_repetition(self):
        """test case to check if values differ between trng runs;
         modify to use values from external sources"""
        random.seed(time.time())

        # example of first run values; using prng as a placeholder for trng
        first_run_vals = random.choices(range(1, 1001), k=100)

        random.seed(time.time() + 1) # simulate new set of vals
        second_run_vals = random.choices(range(1, 1001), k=100)

        self.assertNotEqual(first_run_vals, second_run_vals, "Values from two runs are the same," \
        "test failed.")

    def test_vals_in_range(self):
        """test case to check if TRNG values are within expected range"""
        # use prng as placeholder for trng
        random.seed(time.time())
        samp_rand_vals = random.choices(range(1, 1001), k=100)
        self.assertTrue(all(1 <= samp_val <= 1000 for samp_val in samp_rand_vals), "Sampled" \
        "random vals are out of expected range, test failed.")

    def test_bit_uniformity(self):
        """test case using Chi-squared test to check if bits are uniformly distributed"""
        # use prng as placeholder for trng
        samples = [random.randint(0, 255) for i in range(100000)]

        observed_freq = np.bincount(samples, minlength=256)
        expected_freq = [len(samples) / 256] * 256

        i, p_val = stats.chisquare(observed_freq, expected_freq)

        self.assertGreater(p_val, 0.01, "Chi-squared test failed; bits aren't uniformly" \
        "distributed")
