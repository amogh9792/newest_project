import os
from source.constant import constant


class PipelineConfig:
    def __init__(self, global_timestamp):
        self.artifact_dir = os.path.join(constant.ARTIFACT_DIR, global_timestamp)
        self.global_timestamp = global_timestamp
        self.target_column = constant.TARGET_COLUMN
        self.train_pipeline = constant.TRAIN_PIPELINE_NAME

        # Data Ingestion constant
        self.train_di_dir = os.path.join(self.artifact_dir, constant.DI_DIR_NAME)
        self.train_feature_store_dir_path = os.path.join(self.train_di_dir, constant.DI_FEATURE_STORE_DIR, constant.FILE_NAME)
        self.train_file_path = os.path.join(self.train_di_dir, constant.DI_INGESTED_DIR, constant.TRAIN_FILE_NAME)
        self.test_file_path = os.path.join(self.train_di_dir, constant.DI_INGESTED_DIR, constant.TEST_FILE_NAME)
        self.train_test_split_ratio = constant.DI_TRAIN_TEST_SPLIT_RATIO
        self.mongodb_url_key = os.environ[constant.MONGODB_URL_KEY]
        self.database_name = constant.DATABASE_NAME
        self.train_collection_name = constant.TRAIN_DI_COLLECTION_NAME
        self.mandatory_col_list = constant.DI_MANDATORY_COLUMN_LIST
        self.mandatory_col_data_type = constant.DI_MANDATORY_COLUMN_DATA_TYPE

        # data validation
        self.imputation_values_file = constant.DV_IMPUTATION_VALUES_FILE_NAME
        self.outlier_params_file = constant.DV_OUTLIER_PARAMS_FILE

        self.train_file_name = constant.TRAIN_FILE_NAME
        self.test_file_name = constant.TEST_FILE_NAME

        self.dv_train_file_path = os.path.join(self.artifact_dir, constant.DV_DIR_NAME)
        self.dv_test_file_path = os.path.join(self.artifact_dir, constant.DV_DIR_NAME)

        # data transformation
        self.dt_binary_class_col = constant.DT_BINARY_CLASS_COL
        self.dt_multi_class_col = constant.DT_MULTI_CLASS_COL
        self.dt_multi_class_encoder = constant.DT_ENCODER_PATH
        self.dt_train_file_path = os.path.join(self.artifact_dir, constant.DT_DIR_NAME)
        self.dt_test_file_path = os.path.join(self.artifact_dir, constant.DT_DIR_NAME)

        # model train and evaluate
        self.model_path = os.path.join(constant.MODEL_PATH)
        self.final_model_path = os.path.join(constant.FINAL_MODEL_PATH)

        self.predict_di_dir = os.path.join(self.artifact_dir, constant.PREDICT_PIPELINE_NAME, constant.DI_DIR_NAME)
        self.predict_di_feature_store_file_path = os.path.join(self.predict_di_dir, constant.DI_FEATURE_STORE_DIR, constant.PREDICT_DATA_FILE_NAME)
        self.predict_collection_name = constant.PREDICT_DI_COLLECTION_NAME
        self.di_col_drop_in_clean = constant.DI_COL_DROP_IN_CLEAN
        self.predict_file = constant.PREDICT_FILE
        self.predict_file_path = os.path.join(self.predict_di_dir, constant.DI_INGESTED_DIR)