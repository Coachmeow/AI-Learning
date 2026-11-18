import hashlib


def blob_hash(content):
    header = b"blob " + str(len(content)).encode() + b"\0"
    return hashlib.sha256(header + content).hexdigest()
