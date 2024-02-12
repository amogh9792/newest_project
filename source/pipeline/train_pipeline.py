from source.component.train_data_ingestion import DataIngestion
from source.component.data_validation import DataValidation
from source.entity.config_entity import TrainingPipelineConfig
from source.component.data_transformation import DataTransformation

class TrainPipeline:

    def __init__(self, global_timestamp):
        self.utility_config = TrainingPipelineConfig(global_timestamp)

    def start_data_ingestion(self):
        data_ingestion_obj = DataIngestion(self.utility_config)
        data_ingestion_obj.initiate_data_ingestion()


    def start_data_validation(self):
        data_validation_obj = DataValidation(self.utility_config)
        data_validation_obj.initiate_data_validation()

    def start_data_transformation(self):
        data_trans_obj = DataTransformation(self.utility_config)
        data_trans_obj.initiate_data_transformation()

    def run_train_pipeline(self):
        self.start_data_ingestion()
        self.start_data_validation()
        self.start_data_transformation()
        