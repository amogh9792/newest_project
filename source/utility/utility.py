import pandas as pd
import os
from datetime import datetime
from source.exception import ChurnException
global_timestamp = None


def generate_global_timestamp():

    global global_timestamp

    if global_timestamp is None:
        global_timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

    return global_timestamp


def export_data_csv(data, filename, file_path):

    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)

        data.to_csv(os.path.join(file_path, filename), index=False)

    except ChurnException as e:
        raise e


def import_csv_file(filename, file_path):
    try:

        if os.path.exists(file_path):

            return pd.read_csv(file_path + "\\" + filename)

        else:
            print(f"path does not exist: {file_path}")

    except ChurnException as e:
        raise e