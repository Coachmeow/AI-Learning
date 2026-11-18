import hashlib


def blob_hash(content):
    header = b"blob " + str(len(content)).encode()
    return hashlib.sha1(header + content).hexdigest()
