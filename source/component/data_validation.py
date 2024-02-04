import pandas as pd
import numpy as np
from source.exception import ChurnException

class DataValidation:
    def __init__(self, utility_config):
        self.utlity_config = utility_config

    def handle_missing_value(self, data, type):
        try:
            if type == 'train':

                numerical_columns = data.select_dtypes(include=['number']).columns
                numerical_imputation_values = data[numerical_columns].median()
                data[numerical_columns] = data[numerical_columns].fillna(numerical_imputation_values)

                categorical_columns = data.select_dtypes(include=['object']).columns
                categorical_imputation_values = data[categorical_columns].mode().iloc[0]
                data[categorical_columns] = data[categorical_columns].fillna(categorical_imputation_values)

                imputation_values = pd.concat([numerical_imputation_values, categorical_imputation_values])
                imputation_values.to_csv(self.utlity_config.imputation_values_file, header=['imputation_value'])
            else:
                imputation_values = pd.read_csv(self.utlity_config.imputation_values_file, index_col=0)['imputation_value']

                numerical_columns = data.select_dtypes(include=['number']).columns
                data[numerical_columns] = data[numerical_columns].fillna(imputation_values[numerical_columns])

                categorical_columns = data.select_dtypes(include=['object']).columns
                data[categorical_columns] = data[categorical_columns].fillna(imputation_values[categorical_columns].iloc[0])

            return data

        except ChurnException as e:
            raise e

    def initiate_data_validation(self):
        train_data = pd.read_csv(self.utlity_config.train_file_path, dtype={'SeniorCitizen': 'object'})
        test_data = pd.read_csv(self.utlity_config.test_file_path, dtype={'SeniorCitizen': 'object'})

        train_data = self.handle_missing_value(train_data, type='train')
        test_data = self.handle_missing_value(test_data, type='test')


        print('done')