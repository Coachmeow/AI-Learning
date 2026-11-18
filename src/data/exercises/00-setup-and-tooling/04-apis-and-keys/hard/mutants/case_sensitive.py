import time

TEMPORARY = {429, 500, 502, 503, 529}


class ApiError(Exception):
    def __init__(self, status, body=None):
        super().__init__(f"HTTP {status}")
        self.status = status
        self.body = body


def call_with_retry(send, request, max_retries=4, base=1.0, sleep=time.sleep):
    for attempt in range(max_retries + 1):
        status, headers, body = send(request)
        if 200 <= status < 300:
            return body
        if status not in TEMPORARY:
            raise ApiError(status, body)
        if attempt == max_retries:
            break
        wait = headers.get("retry-after")
        sleep(float(wait) if wait is not None else base * 2 ** attempt)
    raise ApiError(status, body)
