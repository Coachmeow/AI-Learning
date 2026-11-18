BYTES_PER_PARAM = {"fp32": 4, "fp16": 2, "bf16": 2, "int8": 1, "int4": 0.5}
PREFERENCE = ["fp32", "fp16", "int8", "int4"]


def best_dtype(params, vram_gb, margin=0.2):
    if not 0 <= margin < 1:
        raise ValueError(margin)
    budget = vram_gb * (1 - margin)
    for dtype in PREFERENCE:
        if params * BYTES_PER_PARAM[dtype] / 1e9 < budget:
            return dtype
    return None
