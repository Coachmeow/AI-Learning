import hashlib


def blob_hash(content):
    header = b"blob " + str(len(content.decode("utf-8"))).encode() + b"\0"
    return hashlib.sha1(header + content).hexdigest()
