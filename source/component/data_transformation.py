import os
import pandas as pd
import pickle
from source.exception import ChurnException
from source.logger import logging
import category_encoders as ce
import warnings
warnings.filterwarnings('ignore')


class DataTransformation:
    def __init__(self, utlity_config):
        self.utlity_config = utlity_config

    def feature_encoding(self, data, target, save_encoder_path=None, load_encoder_path=None, type=None):
        try:
            for col in self.utlity_config.dt_binary_class_col:
                data[col] = data[col].map({'Yes': 1, 'No': 0, 'Male': 1, 'Female': 0})

            if target != '':
                data[self.utlity_config.target_column] = data[self.utlity_config.target_column].map({'Yes': 1, 'No': 0})

            if type == 'test':
                data[self.utlity_config.target_column] = data[self.utlity_config.target_column].map({'Yes': 1, 'No': 0})

            if save_encoder_path:
                encoder = ce.TargetEncoder(cols=self.utlity_config.dt_multi_class_col)
                data_encoded = encoder.fit_transform(data[self.utlity_config.dt_multi_class_col], data[self.utlity_config.target_column])

                with open(save_encoder_path, 'wb') as f:
                    pickle.dump(encoder, f)

            if load_encoder_path:
                with open(load_encoder_path, 'rb') as f:
                    encoder = pickle.load(f)

                data_encoded = encoder.transform(data[self.utlity_config.dt_multi_class_col])

            data = pd.concat([data.drop(columns=self.utlity_config.dt_multi_class_col), data_encoded], axis=1)
            print(data)

            return data

        except ChurnException as e:
            raise e

    def initiate_data_transformation(self):
        train_data = pd.read_csv(self.utlity_config.dv_train_file_path+'\\'+self.utlity_config.train_file_name, dtype={'SeniorCitizen': 'object'})
        test_data = pd.read_csv(self.utlity_config.dv_test_file_path+'\\'+self.utlity_config.test_file_name, dtype={'SeniorCitizen': 'object'})

        train_data = self.feature_encoding(train_data, target='Churn', save_encoder_path=self.utlity_config.dt_multi_class_encoder)
        test_data = self.feature_encoding(test_data, target='', load_encoder_path=self.utlity_config.dt_multi_class_encoder, type='test')

        print('done')