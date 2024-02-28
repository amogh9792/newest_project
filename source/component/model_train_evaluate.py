import pickle 
import warnings
import os
import pandas as pd
from source.logger import logging
from source.exception import ChurnException
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report, make_scorer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

warnings.filterwarnings('ignore')


class ModelTrainEvaluate:

    def __init__(self, utility_config):
        self.utility_config = utility_config

        self.models = {
            'LogisticRegression' : LogisticRegression(),
            'SVC' : SVC(),
            'DecisionTreeClassifier' : DecisionTreeClassifier(),
            'RandomForestClassifier' : RandomForestClassifier(),
            'GradientBoostingClassifier' : GradientBoostingClassifier(),
            'AdaBoostClassifier' : AdaBoostClassifier(),
            'GaussianNB' : GaussianNB(),
            'KNeighborsClassifier' : KNeighborsClassifier(),
            'XGBClassifier' : XGBClassifier()
        }

        self.model_evaluation_report = pd.DataFrame(columns = ['model_name', 'accuracy', 'precision', 'recall', 'f1', 'class_report', 'confu_matrix'])

    def model_training(self, train_data, test_data):
        try:
            x_train = train_data.drop('Churn', axis = 1)
            y_train = train_data['Churn']

            test_data = test_data.drop(test_data.index[-2:])

            x_test = test_data.drop('Churn', axis = 1)
            y_test = test_data['Churn']

            dir_path = os.path.dirname(self.utility_config.model_path)
            os.makedirs(dir_path, exist_ok=True)

            for name, model in self.models.items():
                model.fit(x_train, y_train)
                y_pred = model.predict(x_test)

                with open(f"{self.utility_config.model_path}/{name}.pkl", "wb") as f:
                    pickle.dump(model, f)

                self.metrics_and_log(y_test, y_pred, name)

        except ChurnException as e:
            raise e
        
    def metrics_and_log(self, y_test, y_pred, model_name):
        try:
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            class_report = classification_report(y_test, y_pred)
            confu_matrix = confusion_matrix(y_test, y_pred)

            logging.info(f'Model : {model_name}, accuracy : {accuracy}, precision : {precision}, recall : {recall}, f1_score : {f1}, classification_report : {class_report}, confusion_matrix : {confu_matrix}')
            new_row = [model_name, accuracy, precision, recall, f1, class_report, confu_matrix]
            self.model_evaluation_report = self.model_evaluation_report._append(pd.Series(new_row, index = self.model_evaluation_report.columns), ignore_index = True)


        except ChurnException as e:
            raise e

    def initiate_model_training(self):
        try:
            train_data = pd.read_csv(self.utility_config.dt_train_file_path+'/'+self.utility_config.train_file_name, dtype={'TotalCharges':'float64'})
            test_data = pd.read_csv(self.utility_config.dt_test_file_path+'/'+self.utility_config.test_file_name, dtype={'TotalCharges':'float64'})

            self.model_training(train_data, test_data)
            self.model_evaluation_report.to_csv('source/ml/model_evaluation_report.csv', index=False)
            print('Model Train Done')
        except ChurnException as e:
            raise e