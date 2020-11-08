import re


def check_input_format(input_string):
    return bool(re.match("^[A-Za-z]{3}-*$", input_string))
