from collections import defaultdict


def human(n):
    """du -h style size: '512B', '1.5K', '14G' (base 1024)."""
    raise NotImplementedError


def space_hogs(files, max_depth, top):
    """[(human_size, folder), ...] for the `top` largest folders no deeper than `max_depth`."""
    raise NotImplementedError
