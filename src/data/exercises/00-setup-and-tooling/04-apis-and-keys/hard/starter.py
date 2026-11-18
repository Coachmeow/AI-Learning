import time

TEMPORARY = {429, 500, 502, 503, 529}


class ApiError(Exception):
    def __init__(self, status, body=None):
        super().__init__(f"HTTP {status}")
        self.status = status
        self.body = body


def call_with_retry(send, request, max_retries=4, base=1.0, sleep=time.sleep):
    """Call send(request) -> (status, headers, body), retrying temporary errors with backoff."""
    raise NotImplementedError
