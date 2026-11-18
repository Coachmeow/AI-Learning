import json


def _scan(text, drop_commas):
    out, i, n, in_str = [], 0, len(text), False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == '"':
                in_str = False
            i += 1
        elif c == '"':
            in_str = True
            out.append(c)
            i += 1
        elif not drop_commas and text.startswith("//", i):
            while i < n and text[i] != "\n":
                i += 1
        elif not drop_commas and text.startswith("/*", i):
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
        elif drop_commas and c == ",":
            j = i + 1
            while j < n and text[j] in " \t\r\n":
                j += 1
            if not (j < n and text[j] in "}]"):
                out.append(c)
            i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def load_jsonc(text):
    return json.loads(_scan(_scan(text, False), True))
