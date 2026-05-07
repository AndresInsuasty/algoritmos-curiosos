from __future__ import annotations

import math
import struct


def fast_inverse_sqrt(number: float, iterations: int = 1) -> float:
    if number <= 0:
        raise ValueError("number must be positive")

    x2 = number * 0.5
    y = number
    i = struct.unpack("I", struct.pack("f", y))[0]
    i = 0x5F3759DF - (i >> 1)
    y = struct.unpack("f", struct.pack("I", i))[0]

    for _ in range(max(0, iterations)):
        y = y * (1.5 - (x2 * y * y))

    return y


def exact_inverse_sqrt(number: float) -> float:
    if number <= 0:
        raise ValueError("number must be positive")
    return 1.0 / math.sqrt(number)
