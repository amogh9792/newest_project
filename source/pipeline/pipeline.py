from source.component.data_ingestion import DataIngestion
from source.component.data_validation import DataValidation
from source.entity.config_entity import PipelineConfig
from source.component.data_transformation import DataTransformation
from source.component.model_train_evaluate import ModelTrainEvaluate
class DataPipeline:

    def __init__(self, global_timestamp):
        self.utility_config = PipelineConfig(global_timestamp)

    def start_data_ingestion(self, key):
        data_ingestion_obj = DataIngestion(self.utility_config)
        data_ingestion_obj.initiate_data_ingestion(key)


    def start_data_validation(self):
        data_validation_obj = DataValidation(self.utility_config)
        data_validation_obj.initiate_data_validation()

    def start_data_transformation(self):
        data_trans_obj = DataTransformation(self.utility_config)
        data_trans_obj.initiate_data_transformation()

    def start_model_train_evaluate(self):
        model_train_evaulate_obj = ModelTrainEvaluate(self.utility_config)
        model_train_evaulate_obj.initiate_model_training()

    def run_train_pipeline(self):
        self.start_data_ingestion('train')
        self.start_data_validation()
        self.start_data_transformation()
        self.start_model_train_evaluate()

    def run_predict_pipeline(self):
        self.start_data_ingestion('predict')
        self.start_data_validation()
        self.start_data_transformation()
        self.start_model_train_evaluate()
        