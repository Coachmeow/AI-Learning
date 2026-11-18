BYTES_PER_PARAM = {"fp32": 4, "fp16": 2, "bf16": 2, "int8": 1, "int4": 0.5}


def weights_gb(params, dtype):
    """GB (10**9 bytes) needed to hold `params` parameters stored as `dtype`."""
    # TODO: multiply the parameter count by the bytes per parameter, then convert to GB
    raise NotImplementedError
