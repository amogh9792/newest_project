import logging
import pickle
import pymongo
from pymongo import MongoClient

from source.exception import ChurnException
from source.utility.utility import import_csv_file, export_data_csv, read_csv_from_s3, upload_artifact_to_s3


class ModelPrediction:

    def __init__(self, utility_config):
        self.utility_config = utility_config

    def clean_data(self, data):
        data = data.iloc[0:1000]
        data = data.iloc[:, 0:19]
        return data

    def load_model_pickle(self):
        try:

            with open(self.utility_config.final_model_path +'\\'+ self.utility_config.final_model_file_name, 'rb') as file:

                return pickle.load(file)

        except ChurnException as e:
            raise e

    def make_prediction(self, model, data):
        try:

            return model.predict(data)

        except ChurnException as e:
            raise e

    def export_prediction_into_db(self, data):
        try:

            with MongoClient(self.utility_config.mongodb_url_key) as client:

                database = client[self.utility_config.database_name]
                collection = database[self.utility_config.predict_collection_name]

                bulk_operation = []

                for index, row in data.iterrows():
                    cust_id = row['customerID']
                    churn_value = row['Churn']

                    bulk_operation.append(
                        pymongo.UpdateOne({"customerID": cust_id}, {"$set": {"Churn": churn_value}})
                    )

                if bulk_operation:
                    collection.bulk_write(bulk_operation)

        except ChurnException as e:
            raise e

    def initiate_model_prediction(self):

        logging.info("Start: Model prediction")

        # predict_data = import_csv_file(self.utility_config.predict_file, self.utility_config.predict_dt_file_path)

        predict_data = read_csv_from_s3(self.utility_config.aws_bucket_name, self.utility_config.predict_dt_file_path+'/'+self.utility_config.predict_file)

        predict_data = self.clean_data(predict_data)

        model = self.load_model_pickle()

        # feature_data = import_csv_file(self.utility_config.predict_di_feature_store_file_name, self.utility_config.predict_di_feature_store_file_path)
        feature_data = read_csv_from_s3(self.utility_config.aws_bucket_name, self.utility_config.predict_di_feature_store_file_path+'/'+self.utility_config.predict_di_feature_store_file_name)

        feature_data['Churn'] = self.make_prediction(model, predict_data)

        feature_data['Churn'] = feature_data['Churn'].map({1: "Yes", 0: "No"})

        self.export_prediction_into_db(feature_data)
        # export_data_csv(feature_data, self.utility_config.predict_file, self.utility_config.predict_mp_file_path)

        upload_artifact_to_s3(feature_data, self.utility_config.predict_file, self.utility_config.predict_mp_file_path, self.utility_config.aws_bucket_name)

        logging.info("Complete: Model Prediction")