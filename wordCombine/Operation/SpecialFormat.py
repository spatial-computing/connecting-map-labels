# -*- coding: utf-8 -*-


def single_word(text):
    if len(text.split())>2:
        return True

    buffer = text.replace("°".decode("utf8"), "::::")
    if "::::" in buffer:
        return True

    return False




def filter_coordinates(text):

        # text=text.decode("utf8")
        if not text.endswith("'"):
            return False
        text = text.strip("'")
        text = text.replace("°".decode("utf8"), "::::")
        arr = text.split("::::")
        if len(arr) != 2:
            return False
        if arr[0].isdigit() and arr[1].isdigit():
            return True
        else:
            return False