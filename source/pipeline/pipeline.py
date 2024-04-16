from source.component.data_ingestion import DataIngestion
from source.component.data_validation import DataValidation
from source.component.model_predict import ModelPrediction
from source.component.data_transformation import DataTransformation
from source.component.model_train_evaluate import ModelTrainEvaluate
from source.entity.config_entity import PipelineConfig


class DataPipeline:

    def __init__(self, global_timestamp):
        self.utility_config = PipelineConfig(global_timestamp)

    def start_data_ingestion(self, key):
        data_ingestion_obj = DataIngestion(self.utility_config)
        data_ingestion_obj.initiate_data_ingestion(key)

    def start_data_validation(self, key):
        data_validation_obj = DataValidation(self.utility_config)
        data_validation_obj.initiate_data_validation(key)

    def start_data_transformation(self, key):
        data_trans_obj = DataTransformation(self.utility_config)
        data_trans_obj.initiate_data_transformation(key)

    def start_model_train_evaluate(self):
        model_train_eval_obj = ModelTrainEvaluate(self.utility_config)
        model_train_eval_obj.initiate_model_training()

    def start_model_prediction(self):

        model_predict_obj = ModelPrediction(self.utility_config)
        model_predict_obj.initiate_model_prediction()

    def run_train_pipeline(self):
        self.start_data_ingestion('train')
        self.start_data_validation('train')
        self.start_data_transformation('train')
        self.start_model_train_evaluate()

    def run_predict_pipeline(self):
        self.start_data_ingestion('predict')
        self.start_data_validation('predict')
        self.start_data_transformation('predict')
        self.start_model_prediction()