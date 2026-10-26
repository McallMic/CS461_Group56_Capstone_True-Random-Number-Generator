"""Implementation of a Most Common Value (MCV) estimator 
to calculate min-entropy with a 99% upper confidence bound, and convert to bits."""

import numpy as np

Z = 2.576          # standard deviations from mean for 99% confidence bound
MIN_N = 1000000    # minimum sample count


class EntropyResult:
    # holds the estimated entropy result plus the numbers used to get it, so it can be checked later

    def __init__(self, h_min, h_min_per_bit, p_hat, p_upper, n,
                 most_common_value, estimator, bits_per_sample):
        self.h_min = h_min
        self.h_min_per_bit = h_min_per_bit
        self.p_hat = p_hat                  
        self.p_upper = p_upper
        self.n = n
        self.most_common_value = most_common_value
        self.estimator = estimator
        self.bits_per_sample = bits_per_sample

    def as_dict(self):
        return {
            "h_min": self.h_min,
            "h_min_per_bit": self.h_min_per_bit,
            "p_hat": self.p_hat,
            "p_upper": self.p_upper,
            "n": self.n,
            "most_common_value": self.most_common_value,
            "estimator": self.estimator,
            "bits_per_sample": self.bits_per_sample,
        }

    def __repr__(self):
        return "EntropyResult(" + str(self.as_dict()) + ")"


def check_input(samples, bits_per_sample):
# TO-DO: input validation 

def estimate_min_entropy(samples, bits_per_sample):
    # samples = check_input(samples, bits_per_sample) // Uncomment after finishing check_input
    n = len(samples)

    # count how many times each value appears
    counts = np.bincount(samples.astype(np.int64), minlength=2 ** bits_per_sample)

    # most common value and its frequency
    mcv = int(np.argmax(counts))
    p_hat = counts[mcv] / n

    # 99% upper confidence bound on p_max 
    p_upper = p_hat + Z * np.sqrt(p_hat * (1 - p_hat) / (n - 1))
    if p_upper > 1:
        p_upper = 1.0

    # calculate min-entropy = -log2(p_max)
    h_min = -np.log2(p_upper)

    return EntropyResult(
        h_min=float(h_min),
        h_min_per_bit=float(h_min) / bits_per_sample,
        p_hat=float(p_hat),
        p_upper=float(p_upper),
        n=n,
        most_common_value=mcv,
        estimator="MCV",
        bits_per_sample=bits_per_sample,
    )
