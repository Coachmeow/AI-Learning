BYTES_PER_PARAM = {"fp32": 4, "fp16": 2, "bf16": 2, "int8": 1, "int4": 0.5}
PREFERENCE = ["fp32", "fp16", "int8", "int4"]  # most precise first


def best_dtype(params, vram_gb, margin=0.2):
    """Most precise dtype whose weights fit in vram_gb * (1 - margin), or None."""
    raise NotImplementedError
