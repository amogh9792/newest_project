import pandas as pd
from source.utility.utility import generate_global_timestamp
from source.entity.config_entity import TrainingPipelineConfig
from source.logger import setup_logger
from source.logger import logging


if __name__ == '__main__':

    global_timestamp = generate_global_timestamp()

    setup_logger(global_timestamp)
    logging.info("logger timestamp setup complete")

    train_pipeline_config_obj = TrainingPipelineConfig(global_timestamp)
    print(train_pipeline_config_obj.__dict__)

    logging.info("training pipeline config created")