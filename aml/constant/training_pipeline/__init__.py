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

"""
Model Trainer related constants
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str ="trained_models"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.75
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD: float = 0.05

"""
Model Evaluation related constants start with MODEL EVALUATION VAR NAME
"""
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
MODEL_EVALUATION_DIR_NAME: str = "model_evaluation"
MODEL_EVALUATION_REPORT_NAME: str = "report.yaml"

"""
Model pusher related constanst start with MODEL PUSHER
"""
MODEL_PUSHER_DIR_NAME: str = "model_pusher"
MODEL_PUSHER_SAVED_MODEL_DIR: str = SAVED_MODEL_DIR


