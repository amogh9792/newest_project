import numpy as np
import os
import pandas as pd
import pickle
import category_encoders as ce
import warnings
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import MinMaxScaler
from source.exception import ChurnException
from source.logger import logging
from source.utility.utility import export_data_csv, import_csv_file, read_csv_from_s3, upload_artifact_to_s3

warnings.filterwarnings('ignore')


class DataTransformation:
    def __init__(self, utility_config):
        self.utility_config = utility_config

    def feature_encoding(self, data, target, save_encoder_path=None, load_encoder_path=None, key=None):

        try:
            for col in self.utility_config.dt_binary_class_col:
                data[col] = data[col].map({'Yes': 1, 'No': 0, 'Male': 1, 'Female': 0})

            if target != '':
                data[self.utility_config.target_column] = data[self.utility_config.target_column].map({'Yes': 1, 'No': 0})

            if key == 'test':
                data[self.utility_config.target_column] = data[self.utility_config.target_column].map({'Yes': 1, 'No': 0})

            if save_encoder_path:
                encoder = ce.TargetEncoder(cols=self.utility_config.dt_multi_class_col)
                data_encoded = encoder.fit_transform(data[self.utility_config.dt_multi_class_col], data[self.utility_config.target_column])

                with open(save_encoder_path, 'wb') as f:
                    pickle.dump(encoder, f)

            if load_encoder_path:
                with open(load_encoder_path, 'rb') as f:
                    encoder = pickle.load(f)

                data_encoded = encoder.transform(data[self.utility_config.dt_multi_class_col])

            data = pd.concat([data.drop(columns=self.utility_config.dt_multi_class_col), data_encoded], axis=1)

            return data

        except ChurnException as e:
            raise e

    def min_max_scaling(self, data, key=None):

        if key == 'train':

            numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns

            scaler = MinMaxScaler()

            scaler.fit(data[numeric_columns])

            scaler_details = pd.DataFrame({'Feature': numeric_columns,
                                           'Scaler_Min': scaler.data_min_,
                                           'Scaler_Max': scaler.data_max_
                                           })
            scaler_details.to_csv('source/ml/scaler_details.csv', index=False)

            scaled_data = scaler.transform(data[numeric_columns])

            data.loc[:, numeric_columns] = scaled_data
            data['Churn'] = self.utility_config.target_column

        else:
            scaler_details = pd.read_csv('source/ml/scaler_details.csv')

            for col in data.select_dtypes(include=['float64', 'int64']).columns:
                data[col] = data[col].astype('float64')

                temp = scaler_details[scaler_details['Feature'] == col]

                if not temp.empty:

                    min = temp.loc[temp.index[0], 'Scaler_Min']
                    max = temp.loc[temp.index[0], 'Scaler_Max']

                    data[col] = (data[col]-min) / (max-min)

                else:
                    print(f"No scaling details available for feature: {col}")

            data['Churn'] = self.utility_config.target_column

        return data

    def oversample_smote(self, data):
        try:

            np.random.seed(42)

            x = data.drop(columns=['Churn'])
            y = data['Churn']

            smote = SMOTE()

            x_resmapled, y_resampled = smote.fit_resample(x, y)

            return pd.concat([pd.DataFrame(x_resmapled, columns=x.columns), pd.DataFrame(y_resampled, columns=['Churn'])], axis=1)

        except ChurnException as e:
            raise e

    def export_data_file(self, data, file_name, path):
        try:

            dir_path = os.path.join(path)
            os.makedirs(dir_path, exist_ok=True)

            data.to_csv(path+'\\'+file_name, index=False)

            logging.info('data transformation file exported')

        except ChurnException as e:
            raise e

    def initiate_data_transformation(self, key):

        if key == 'train':

            logging.info("Start: Data transformation for training")

            train_data = import_csv_file(self.utility_config.train_file_name, self.utility_config.train_dv_train_file_path)
            test_data = import_csv_file(self.utility_config.test_file_name, self.utility_config.train_dv_test_file_path)

            train_data = self.feature_encoding(train_data, target='Churn', save_encoder_path=self.utility_config.dt_multi_class_encoder, key='train')
            test_data = self.feature_encoding(test_data, target='', load_encoder_path=self.utility_config.dt_multi_class_encoder, key='test')

            self.utility_config.target_column = train_data['Churn']
            train_data.drop('Churn', axis=1, inplace=True)
            train_data = self.min_max_scaling(train_data, key='train')

            self.utility_config.target_column = test_data['Churn']
            test_data.drop('Churn', axis=1, inplace=True)
            test_data = self.min_max_scaling(test_data, key='test')

            train_data = self.oversample_smote(train_data)

            export_data_csv(train_data, self.utility_config.train_file_name,  self.utility_config.train_dt_train_file_path)
            export_data_csv(test_data, self.utility_config.test_file_name, self.utility_config.train_dt_test_file_path)

        if key == 'predict':

            logging.info("Start: Data Transformation for prediction")

            # predict_data = import_csv_file(self.utility_config.predict_file, self.utility_config.predict_dv_file_path)
            predict_data = read_csv_from_s3(self.utility_config.aws_bucket_name, self.utility_config.predict_dv_file_path+'/'+self.utility_config.predict_file)
            predict_data = self.feature_encoding(predict_data, target='', load_encoder_path=self.utility_config.dt_multi_class_encoder, key='predict')
            predict_data = self.min_max_scaling(predict_data, key='predict')

            # export_data_csv(predict_data, self.utility_config.predict_file, self.utility_config.predict_dt_file_path)

            upload_artifact_to_s3(predict_data, self.utility_config.predict_file, self.utility_config.predict_dt_file_path, self.utility_config.aws_bucket_name)

        logging.info("Complete: Data Transformation")