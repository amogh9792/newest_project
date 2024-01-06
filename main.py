from source.utility.utility import generate_global_timestamp
import pandas as pd
from source.logger import logging
from source.logger import setup_logger
from source.entity.config_entity import TrainingPipelineConfig
if __name__ == '__main__':

    global_timestamp = generate_global_timestamp()

    logging.info(f"time stamp: {global_timestamp}")
    setup_logger(global_timestamp)

    logging.info("logger timestamp setup complete")

    Train_pipeline_config_obj = TrainingPipelineConfig(global_timestamp)
    print(Train_pipeline_config_obj.__dict__)

    logging.info("training pipeline config created")



