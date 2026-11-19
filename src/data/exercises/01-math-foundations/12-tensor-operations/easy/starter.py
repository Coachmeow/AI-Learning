def compute_strides(shape):
    """Row-major strides, in elements, of a contiguous tensor with this shape."""
    if len(shape) == 0:
        return ()
    strides = [1] * len(shape)
    for i in range(len(shape) - 2, -1, -1):
        pass  # TODO: strides[i] from strides[i + 1] and the size of axis i + 1
    return tuple(strides)
