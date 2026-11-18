import hashlib


def blob_hash(content):
    """Return the id git gives a file with these bytes (what `git hash-object` prints)."""
    header = b"blob " + str(len(content)).encode() + b"\0"
    return hashlib.sha1(header + content).hexdigest()
