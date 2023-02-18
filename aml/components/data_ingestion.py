from aml.entity.config_entity import DataIngestionConfig
from aml.entity.artifact_entity import DataIngestionArtifact
from aml.exception import AMLException
from aml.constant.database import KEYSPACE_NAME,LABLED_DATA_COLLECTION_NAME
from aml.data_access.transaction_data import TransactionData
from aml.logger import logging
import sys,os
import pandas as pd

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise AMLException(e,sys)
    def export_data_into_feature_store(self) -> pd.DataFrame:
        """
        Export cassandra collection record as dataframe into feature store
        """
        try:
            logging.info("Exporting data from cassandra to feature store")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # creating folder 
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok= True)
            transactional_data = TransactionData()
            data_frame = transactional_data.export_collection_as_dataframe(save_file_path= feature_store_file_path,keyspace_name=KEYSPACE_NAME,collection_name=LABLED_DATA_COLLECTION_NAME)
            return data_frame
        except Exception as e:
            raise AMLException(e,sys)
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframe = self.export_data_into_feature_store()
            data_ingestion_artifact = DataIngestionArtifact(feature_store_file_paht=self.data_ingestion_config.feature_store_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise AMLException(e,sys)