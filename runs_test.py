"""implements the runs test for the trng"""

import math
import statistics
from scipy.stats import norm
from entropy import estimate_min_entropy

def runs_test(bits):
    """Calculates the z-statistic for a runs test on a sequence of bits.
    Returns the number of runs and the z-statistic"""
    n = len(bits)
    if n == 0:
        return 0, 0

    median = statistics.median(bits)

    num_runs = 1
    n1 = 0      # vals >= median
    n2 = 0      # vals < median

    if bits[0] > median:
        n1 += 1
    else:
        n2 += 1

    for i in range(1, n):
        if bits[i] >= median:
            n1 += 1
        else:
            n2 += 1

        if (bits[i] >= median and bits[i - 1] < median) or (
            bits[i] < median and bits[i - 1] >= median):
            num_runs += 1

        if n1 == 0 or n2 == 0:
            return 0, 1.0

        exp_runs = ((2 * n1 * n2) / n) + 1
        runs_var = (2 * n1 * n2 * (2 * n1 * n2 - n)) / (((n1 + n2) ** 2)
                    * (n1 + n2 - 1))

        if runs_var <= 0:
            return 0, 1.0

        runs_sd = math.sqrt(runs_var)
        z_stat = (num_runs - exp_runs) / runs_sd

        return num_runs, z_stat


def runs_hypothesis_test(bits, alpha=0.05):
    """Uses the z-statistic from the runs test function to determine if a bits sequence
    is appropriately random. Returns True if sufficiently random (Reject the null hypothesis)
    and False otherwise (Fail to reject the null hypothesis)."""
    num_runs, z_stat = runs_test(bits)
    if num_runs == 0:
        return False

    # run the hypothesis test
    z_crit = abs(norm.ppf(alpha / 2))
    if abs(z_stat) > z_crit:
        return False

    return True
