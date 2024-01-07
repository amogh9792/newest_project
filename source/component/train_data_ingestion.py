import os
import pandas as pd
from source.exception import ChurnException
from pymongo.mongo_client import MongoClient
from source.logger import logging


class DataIngestion:
    def __init__(self, train_config):
        self.train_config = train_config

    def export_data_into_feature_store(self):
        try:
            logging.info("start: data load from mongoDB")

            client = MongoClient(self.train_config.mongodb_url_key)
            database = client[self.train_config.database_name]
            collection = database[self.train_config.collection_name]

            cursor = collection.find()

            data = pd.DataFrame(list(cursor))

            dir_path = os.path.dirname(self.train_config.feature_store_dir_path)
            os.makedirs(dir_path, exist_ok=True)
            data.to_csv(self.train_config.feature_store_dir_path, index=False)

            logging.info("complete: data load from mongoDB")

        except ChurnException as e:
            logging.error(e)
            raise e

    def split_data_test_train(self):
        try:
            pass
        except ChurnException as e:
            raise e

    def initiate_data_ingestion(self):
        self.export_data_into_feature_store()
        self.split_data_test_train()