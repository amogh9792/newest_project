from datetime import datetime

global_timestamp = None


def generate_global_timestamp():

    global global_timestamp

    if global_timestamp is None:
        global_timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

    return global_timestamp