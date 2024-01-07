from source.utility.utility import generate_global_timestamp
from source.entity.config_entity import TrainingPipelineConfig
from source.logger import setup_logger
from source.logger import logging
from source.pipeline.train_pipeline import TrainPipeline



if __name__ == '__main__':

    global_timestamp = generate_global_timestamp()

    setup_logger(global_timestamp)
    logging.info("logger timestamp setup complete")

    #train_pipeline_config_obj = TrainingPipelineConfig(global_timestamp)
    #print(train_pipeline_config_obj.__dict__)

    logging.info("training pipeline config created")

    train_pipeline_obj = TrainPipeline(global_timestamp)
    train_pipeline_obj.run_train_pipeline()