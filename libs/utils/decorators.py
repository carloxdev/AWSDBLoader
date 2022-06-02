# Python's Libraries
import logging


logger = logging.getLogger(__name__)


def build_Message(_args, _message):
    qty = 0
    params = ""

    for param in _args:
        qty += 1

        if qty == 1:
            continue

        if param is None:
            value = "None"
        else:
            value = param

        if qty == len(_args):
            param_value = str(value) if isinstance(value, int) else value
            params += f"{type(value).__name__}: {param_value}"
        else:
            params += f"{type(value).__name__}: {value}, "

    return f"{_message} Params: {{{params}}}"


def step(_message):
    def inner(func):
        def wrapper(*args, **kwargs):

            msg = build_Message(args, _message)

            logging.info(msg)
            response = func(*args, **kwargs)
            logging.info(f"{_message} OK")
            return response

        return wrapper
    return inner
