import numpy as np

def _format_collection_labels(values):
    mapping = {1: 'Day 1', 2: 'Day 2'}
    return np.asarray([mapping.get(int(v), str(v)) for v in values])
