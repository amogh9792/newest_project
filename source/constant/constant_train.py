

# Common constants
TARGET_COLUMN = 'Churn'
TRAIN_PIPELINE_NAME = 'train_pipeline'
ARTIFACT_DIR = 'artifact'
FILE_NAME = 'training_data.csv'

TRAIN_FILE_NAME = 'train.csv'
TEST_FILE_NAME = 'test.csv'

MONGODB_URL_KEY = "MONGODB_KEY"
DATABASE_NAME = 'dataset'

# Data ingestion constant
DI_COLLECTION_NAME = 'telco-customer-churn'
DI_DIR_NAME = 'data_ingestion'
DI_FEATURE_STORE_DIR = 'feature_store'
DI_INGESTED_DIR = 'ingested'
DI_TRAIN_TEST_SPLIT_RATIO = 0.2

DI_MANDATORY_COLUMN_LIST = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
                       'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
                       'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
                       'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
                       'MonthlyCharges', 'TotalCharges', 'Churn']


DI_MANDATORY_COLUMN_DATA_TYPE = {'gender': 'object', 'SeniorCitizen': 'object', 'Partner': 'object',
                              'Dependents': 'object', 'tenure': 'int64', 'PhoneService': 'object',
                              'MultipleLines': 'object', 'InternetService': 'object', 'OnlineSecurity': 'object',
                              'OnlineBackup': 'object', 'DeviceProtection': 'object', 'TechSupport': 'object',
                              'StreamingTV': 'object', 'StreamingMovies': 'object', 'Contract': 'object',
                              'PaperlessBilling': 'object', 'PaymentMethod': 'object', 'MonthlyCharges': 'float64',
                              'TotalCharges': 'float64', 'Churn': 'object'}