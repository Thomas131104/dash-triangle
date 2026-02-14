import numpy as np

def _safe_acos(x):
    return np.arccos(np.clip(x, -1.0, 1.0))