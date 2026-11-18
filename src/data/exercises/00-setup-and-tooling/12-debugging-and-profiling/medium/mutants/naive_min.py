import math


def value_stats(values):
    finite = [x for x in values if math.isfinite(x)]
    return {
        "count": len(values),
        "has_nan": any(math.isnan(x) for x in values),
        "has_inf": any(math.isinf(x) for x in values),
        "min": min(values) if values else None,
        "max": max(values) if values else None,
        "mean": sum(finite) / len(finite) if finite else None,
    }
