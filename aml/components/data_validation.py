import os,sys
from aml.entity.config_entity import DataValidationConfig
from aml.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from aml.exception import AMLException
from aml.logger import logging
from aml.utils.main_utils import read_yaml_file
from aml.constant.training_pipeline import SCHEMA_FILE_PATH
import pandas as pd
class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._shema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise AMLException(e,sys)
    
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            logging.info("Required number of columns:{number_of_columns}")
            logging.info("Data Frame has columns:{len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise AMLException(e,sys)
    
    def is_numerical_column_exist(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns = self._schema_config["numerical_columns"]
            numerical_column_present = True
            missing_numerical_columns = []
            for numerical_column in numerical_columns:
                    if numerical_column not in dataframe.columns:
                        numerical_column_present =  False
                        missing_numerical_columns.append(numerical_column)
            if numerical_column_present:
                return True
            return False
        except Exception as e:
            raise AMLException(e,sys)

    def initiate_data_validate(self)->DataValidationArtifact:
        try:
            dataframe =self.data_ingestion_artifact.feature_store_file_path
            # validate the number of columns
            status = self.validate_number_of_columns(dataframe=dataframe)
            if not status:
                error_message = f"{error_message} dataframe does not contaiin all columns"
            # checking the numerical values 
            status = self.is_numerical_column_exist(dataframe=dataframe)
            if not status:
                error_message = f"{error_message} Train dataframe does not contain all numercical columns"
        except Exception as e:
            raise AMLException(e,sys)
        