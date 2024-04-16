import os
import pandas as pd
from pandas import DataFrame
from source.exception import ChurnException
from pymongo.mongo_client import MongoClient
from sklearn.model_selection import train_test_split
from source.utility.utility import export_data_csv, upload_artifact_to_s3
from source.logger import logging


class DataIngestion:
    def __init__(self, utility_config):
        self.utility_config = utility_config

    def export_data_into_feature_store(self, key) -> DataFrame:
        try:
            logging.info("start: data load from mongoDB")

            if key == 'train':
                collection_name = self.utility_config.train_collection_name
                feature_store_file_path = self.utility_config.train_feature_store_dir_path
                feature_store_file_name = self.utility_config.train_feature_store_file_name
            else:
                collection_name = self.utility_config.predict_collection_name
                feature_store_file_path = self.utility_config.predict_di_feature_store_file_path
                feature_store_file_name = self.utility_config.predict_di_feature_store_file_name

            client = MongoClient(self.utility_config.mongodb_url_key)
            database = client[self.utility_config.database_name]

            collection = database[collection_name]
            cursor = collection.find()
            data = pd.DataFrame(list(cursor))

            # dir_path = os.path.dirname(feature_store_file_path)
            # os.makedirs(dir_path, exist_ok=True)
            # data.to_csv(feature_store_file_path, index=False)

            # export_data_csv(data, feature_store_file_name, feature_store_file_path)
            upload_artifact_to_s3(data, feature_store_file_name, feature_store_file_path, self.utility_config.aws_bucket_name)

            logging.info("complete: data load from mongoDB")

            return data

        except ChurnException as e:
            logging.error(e)
            raise e

    def split_data_test_train(self, data: DataFrame):
        try:
            logging.info("start: train, test data split")

            train_set, test_set = train_test_split(data, test_size=self.utility_config.train_test_split_ratio, random_state=42)

            logging.info("complete: train, test data split")

            return train_set, test_set

        except ChurnException as e:
            raise e

    def clean_data(self, data, key):
        try:

            logging.info("start: clean data")

            if key == 'train':
                data = data.drop_duplicates()

                data = data.loc[:, data.nunique() > 1]

                drop_column = []

                for col in data.select_dtypes(include=['object']).columns:
                    unique_count = data[col].nunique()

                    if unique_count / len(data) > 0.5:
                        data.drop(col, axis=1, inplace=True)
                        drop_column.append(col)

                logging.info(f"dropped columns: {drop_column}")

            logging.info("complete: clean data")

            return data

        except ChurnException as e:
            raise e

    def process_data(self, data, key):
        try:
            logging.info("start: process data")

            if key == 'train':
                mandatory_cols = self.utility_config.mandatory_col_list.copy()

            if key in ['predict', 'test']:
                mandatory_cols = self.utility_config.mandatory_col_list.copy()

                mandatory_cols.remove('Churn')

                data = data.drop(self.utility_config.di_col_drop_in_clean, axis=1)

            for col in mandatory_cols:

                if col not in data.columns:
                    raise ChurnException(f"missing mandatory column: {col}")

                if data[col].dtype != self.utility_config.mandatory_col_data_type[col]:
                    try:
                        data[col] = data[col].astype(self.utility_config.mandatory_col_data_type[col])
                    except ValueError as e:
                        raise ChurnException(f"ERROR: converting data type for column: {col}")

            data = data[mandatory_cols]

            logging.info("complete: process data")

            return data

        except ChurnException as e:
            raise e

    def initiate_data_ingestion(self, key):
        try:

            logging.info("start: data ingestion")

            data = self.export_data_into_feature_store(key)
            data = self.process_data(data, key)
            data = self.clean_data(data, key)

            if key == 'train':
                train_data, test_data = self.split_data_test_train(data)
                export_data_csv(train_data, self.utility_config.train_file_name, self.utility_config.train_di_train_file_path)
                export_data_csv(test_data, self.utility_config.test_file_name, self.utility_config.train_di_test_file_path)

            if key == 'predict':
                # export_data_csv(data, self.utility_config.predict_file, self.utility_config.predict_file_path)
                upload_artifact_to_s3(data, self.utility_config.predict_file, self.utility_config.predict_file_path, self.utility_config.aws_bucket_name)

            logging.info("complete: data ingestion")
        except ChurnException as e:
            raise e