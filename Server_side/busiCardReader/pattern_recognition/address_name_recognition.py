# -*- coding: utf-8 -*-

import os
path = os.path.dirname(os.path.abspath(__file__))

common_address_token = []

with open(path + '/../data/address_token', encoding="utf8") as add_tokens:
    for token in add_tokens:
        normalize = token.strip().lower()
        if len(normalize) > 0:
            common_address_token.append(normalize)


def is_address(line):
    lower_line = line.lower()
    for add_token in common_address_token:
        if lower_line.find(add_token) >= 0:
            return True
    return False
