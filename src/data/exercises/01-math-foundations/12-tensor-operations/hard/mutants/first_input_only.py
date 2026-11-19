from itertools import product


def _shape(a):
    shape = []
    while isinstance(a, list):
        shape.append(len(a))
        a = a[0] if a else None
    return shape


def _get(a, idx):
    for i in idx:
        a = a[i]
    return a


def _zeros(shape):
    return 0.0 if not shape else [_zeros(shape[1:]) for _ in range(shape[0])]


def einsum(subscripts, *arrays):
    """Einstein summation over nested lists, for subscripts written with '->'."""
    inputs, out = subscripts.replace(" ", "").split("->")
    terms = inputs.split(",")
    if len(terms) != len(arrays):
        raise ValueError("one subscript term per array")
    sizes = {}
    for term, arr in zip(terms, arrays):
        shape = _shape(arr)
        if len(shape) != len(term):
            raise ValueError(f"'{term}' needs {len(term)} axes, got {len(shape)}")
        for letter, n in zip(term, shape):
            if sizes.setdefault(letter, n) != n:
                raise ValueError(f"letter '{letter}' has sizes {sizes[letter]} and {n}")
    if any(letter not in sizes for letter in out):
        raise ValueError("every output letter must appear in an input")
    letters = sorted(sizes)
    result = _zeros([sizes[c] for c in out])
    if not out:
        result = 0.0
    for combo in product(*(range(sizes[c]) for c in letters)):
        env = dict(zip(letters, combo))
        value = _get(arrays[0], [env[c] for c in terms[0]])
        if not out:
            result += value
        else:
            target = _get(result, [env[c] for c in out[:-1]])
            target[env[out[-1]]] += value
    return result
