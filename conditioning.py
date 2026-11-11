import hashlib
import math

import numpy as np

from entropy import estimate_min_entropy

def sha256_condition(bits, entropy_per_bit):
    """bits: expecting an array of 0s and 1s.
    entropy_per_bit: expected output from entropy.py (h_min_per_bit) on the RAW bits.
    Returns conditioned bits """
    bits = np.asarray(bits, dtype=np.uint8)
 
    # how many raw bits we need to collect: 256 + 64 bits of entropy
    chunk = math.ceil((256 + 64) / entropy_per_bit)
 
    out = []
    for start in range(0, len(bits) - chunk + 1, chunk):
        raw_bytes = np.packbits(bits[start:start + chunk]).tobytes()
        digest = hashlib.sha256(raw_bytes).digest()
        out.append(np.unpackbits(np.frombuffer(digest, dtype=np.uint8)))
 
    if not out:
        raise ValueError(f"need at least {chunk} raw bits for one output block")
    return np.concatenate(out)
 
