def compute_strides(shape):
    """Row-major strides, in elements, of a contiguous tensor with this shape."""
    if len(shape) == 0:
        return ()
    strides = [1] * len(shape)
    for i in range(len(shape) - 2, -1, -1):
        strides[i] = strides[i + 1] * shape[i + 1]
    return tuple(strides)
