import numpy as np
import cmath
import itertools
from defaults import FOURIER_DT


# Given a finite list of integer frequencies n in [0, -1, 1, -2, 2, ...], and the corresponding Fourier weights of c_n,
# reconstruct the original curve of f(t) at time t (0<=t<1) by Fourier synthesis.
# Mathematically,
# f(t) = sum(c_n*e^(n*2*pi*i*t)
# The more frequencies (cycles) we have, the closer f(t) will be to the original curve.
# For drawing purposes, the function returns with the cumulative list of points at the given time t, starting with the
# origin. Thus, the returning list of points will gives us the series of line segments we want to draw.
def fourier_synthesis(frequencies, weights, t):
    origin = [complex(0, 0)]
    components = origin + [cn * cmath.exp(n*2*cmath.pi*1j*t) for n, cn in zip(frequencies, weights)]
    return list(itertools.accumulate(components))


# Given a set of complex points representing a closed curve,
# and a finite list of integer frequencies n in [0, -1, 1, -2, 2, ...],
# calculate the coefficients (weights) of the Fourier series.
# Mathematically, if f(t) is a complex function of time (0<=t<1),
# then for each cycle frequency of n, the n-th weight denoted by c_n is:
# c_n = int_0^1 f(t)*e^(-n*2*pi*i*t)dt
# The more frequencies (cycles) we have, the closer f(t) can reconstructed by Fourier synthesis.
def fourier_analysis(frequencies, points):
    weights = []

    # Select the matching point of the list of points, according to t, if 0<=t<1.
    def f(t):
        idx = min(len(points) - 1, max(0, round(t * len(points))))
        return points[idx]

    for n in frequencies:
        # We calculate the integral numerically:
        # cn = sum_t f(t)*e^(-n*2*pi*i*t)*dt, where t goes from 0 to 1 discretely, with a step size of dt
        cn = sum([f(t) * cmath.exp(-n*2*cmath.pi*1j*t) * FOURIER_DT for t in np.arange(0, 1, FOURIER_DT)])
        weights.append(cn)

    return weights
