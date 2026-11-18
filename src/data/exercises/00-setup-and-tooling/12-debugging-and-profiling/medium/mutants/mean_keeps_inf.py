import math


def value_stats(values):
    finite = [x for x in values if math.isfinite(x)]
    no_nan = [x for x in values if not math.isnan(x)]
    return {
        "count": len(values),
        "has_nan": any(math.isnan(x) for x in values),
        "has_inf": any(math.isinf(x) for x in values),
        "min": min(finite) if finite else None,
        "max": max(finite) if finite else None,
        "mean": sum(no_nan) / len(no_nan) if no_nan else None,
    }
