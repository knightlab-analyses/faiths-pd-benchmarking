import numpy as np
import os

def to_dense(vec):
    """Converts a row/col vector to a dense numpy array.
    Always returns a 1-D row vector for consistency with numpy iteration
    over arrays.
    """
    dense_vec = np.asarray(vec.todense())

    if vec.shape == (1, 1):
        # Handle the special case where we only have a single element, but
        # we don't want to return a numpy scalar / 0-d array. We still want
        # to return a vector of length 1.
        return dense_vec.reshape(1)
    else:
        return np.squeeze(dense_vec)

def safe_dir(directory):
    if directory is not None:
        if not os.path.exists(directory):
            os.makedirs(directory)
    else:
        directory = os.path.curdir
    return directory

class temporary_seed:
    """
    citations=['https://stackoverflow.com/a/49557099/11364334']
    """
    def __init__(self, seed):
        self.seed = seed
        self.backup = None

    def __enter__(self):
        self.backup = np.random.randint(2**32-1, dtype=np.uint32)
        np.random.seed(self.seed)

    def __exit__(self, *_):
        np.random.seed(self.backup)
