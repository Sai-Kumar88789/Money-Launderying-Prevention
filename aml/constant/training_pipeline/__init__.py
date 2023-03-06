import os 

# Defining common constant variables for training pipeline

FILE_NAME = "aml.csv"
ARTIFACT_DIR = "artifact"
TARGET_COLUMN = "class"
PIPELINE_NAME = "aml"
ID_COLUMN = 'txid'

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
SAVED_MODEL_DIR = os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"
PREPROCESSING_FILE_NAME = "preprocessing.pkl"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")

"""
Data ingestion related constants start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME: str = "aml"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2
"""
Data Validation related constants start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

"""
Data transformation related constants
"""
DATA_TRANSFORMATION_DIR_NAME = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR = "transformed_objects"
DATA_TRANSFORMATION_TRAIN_TEST_SPLIT_RATIO: float = 0.2