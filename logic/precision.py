# logic/precision.py
 
import math

EPSILON = 1e-4  # Small value to avoid division by zero

def arctan_quadratic(x):
    """Quadratic approximation of arctan."""
    x_1 = (2*x-1)
    return 2*x*x / x_1*x_1 + 1