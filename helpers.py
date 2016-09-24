# -*- coding: utf-8 -*-
import re


def change_encoding(s, to_enc):
    return s.encode(to_enc)


def get_valid_filename(s):
    s = s.strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w]", "", s)


def skip_read(f, s):
    for i in range(0, s):
        f.readline()


def get_words(s):
    return re.split("\s+", s)


def skip_until_value(f, expected):
    hlen = len(expected)
    while True:
        s = f.readline()
        header = s[:hlen]
        if (header == expected):
            break
    value = s[hlen:]
    return (value.strip())


def get_value(s, expected):
    hlen = len(expected)
    header = s[:hlen]
    value = s[hlen:]
    if (header != expected):
        print(("WARNING: header not found in '%s'" % s.strip()))
    else:
        return (value.strip())


def get_quotedString(s):
    if s:
        return (s.strip())[1:-1].strip()
    else:
        return "**unknown**"


def get_float(s):
    return float(s.replace(",", "."))


def norm_string(x):
    return (str(x).lower().replace(" ", "_"))