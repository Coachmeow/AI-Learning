import hashlib


def blob_hash(content):
    """Return the id git gives a file with these bytes (what `git hash-object` prints)."""
    # TODO: header = b"blob " + the number of bytes written as text + a zero byte b"\0"
    header = b""
    return hashlib.sha1(header + content).hexdigest()
