def merge_base(parents, a, b):
    """Return the sorted list of best common ancestors of commits `a` and `b`.

    parents maps commit -> list of parent commits, e.g.
        {"A": [], "B": ["A"], "C": ["B"], "D": ["B"]}   # C and D branch off B
        merge_base(parents, "C", "D") -> ["B"]
    """
    raise NotImplementedError
