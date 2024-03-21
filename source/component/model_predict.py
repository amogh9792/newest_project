import pickle
import pymongo
from pymongo import MongoClient

from source.exception import ChurnException
from source.utility.utility import export_data_csv
from source.utility.utility import import_csv_file

class ModelPrediction:

    def __init__(self, utility_config):

        self.utility_config = utility_config

    def clean_data(self, data):

        data = data.loc[0:1000]
        data = data.iloc[: 0:19]
        return data

    def load_model_pickle(self):

        try:
            with open(self.utility_config.final_model_path + '\\' + self.utility_config.final_model_file_name, 'rb') as file:

                return pickle.load(file)

        except ChurnException as e:
            raise e

    def make_predict(self, model, data):
        try:
            return model.predict(data)
        except ChurnException as e:
            raise e

    def export_prediction_into_db(self, data):
        try:
            with MongoClient(self.utility_config.mongodb_url_key) as client:

                database = client[self.utility_config.database_name]
                collection = database[self.utility_config.prediction_collection_name]

                bulk_operation = []

                for index, row in data.iterrows():

                    cust_id = row['customerID']
                    churn_value = row['Churn']

                    bulk_operation.append(

                        pymongo.UpdateOne({'CustomerID' : cust_id}, {"$set" : {'Churn' : churn_value}})
                    )

                    if bulk_operation:
                        collection.bulk_write(bulk_operation)


        except ChurnException as e:
            raise e

    def initiate_model_prediction(self):

        predict_data = import_csv_file(self.utility_config.predict_file, self.utility_config.predict_dt_file_path)

        predict_data = self.clean_data(predict_data)

        model = self.load_model_pickle()

        prediction = self.make_predict(model, predict_data)

        feature_data = import_csv_file(self.utility_config.predict_di_feature_store_file_name, self.utility_config.predict_di_feature_store_file_path)

        feature_data['Churn'] = self.make_predict(model, predict_data)

        feature_data['Churn'] = feature_data['Churn'].map({1: 'Yes', 0: 'No'})

        self.export_prediction_into_db(feature_data)

        export_data_csv(feature_data, self.utility_config.predict_mp_file_path)

        print('done')