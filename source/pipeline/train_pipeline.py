from source.component.train_data_ingestion import DataIngestion
from source.entity.config_entity import TrainingPipelineConfig


class TrainPipeline:

    def __init__(self, global_timestamp):
        self.train_config = TrainingPipelineConfig(global_timestamp)

    def start_data_ingestion(self):
        data_ingestion_obj = DataIngestion(self.train_config)
        data_ingestion_obj.initiate_data_ingestion()

    def run_train_pipeline(self):
        self.start_data_ingestion()