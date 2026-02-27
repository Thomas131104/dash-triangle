import numpy as np

def _safe_acos(x):
    return np.arccos(np.clip(x, -1.0, 1.0))

def _safe_eq(a, b, eps=1e-6):
    return abs(a-b) < eps