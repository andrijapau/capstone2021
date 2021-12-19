import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import *

import random

# Initiate some data, giving some randomness using random.random().

# Define a function (quadratic in our case) to fit the data with.
def lin_func(p, x):
     m, c = p
     return m*x + c

def linfit(x, y, xerr, yerr, guess = 1):
# Create a model for fitting.
    lin_model = Model(lin_func)

    # Create a RealData object using our initiated data from above.
    data = RealData(x, y, sx=xerr, sy=yerr)

    # Set up ODR with the model and data.
    odr = ODR(data, lin_model, beta0=[guess, 1])

    # Run the regression.
    out = odr.run()

    return [out.beta[0], out.beta[1], out.sd_beta[0], out.sd_beta[1], out.res_var]
    # Use the in-built pprint method to give us results.

    '''Beta: [ 1.01781493  0.48498006]
    Beta Std Error: [ 0.00390799  0.03660941]
    Beta Covariance: [[ 0.00241322 -0.01420883]
     [-0.01420883  0.21177597]]
    Residual Variance: 0.00632861634898189
    Inverse Condition #: 0.4195196193536024
    Reason(s) for Halting:
      Sum of squares convergence'''