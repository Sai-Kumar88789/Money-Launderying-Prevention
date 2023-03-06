from aml.entity.config_entity import DataIngestionConfig
from aml.entity.artifact_entity import DataIngestionArtifact
from aml.exception import AMLException
from aml.constant.database import DATABASE_NAME
from aml.constant.training_pipeline import TARGET_COLUMN
from aml.data_access.transaction_data import TransactionData
from aml.logger import logging
import sys,os
import pandas as pd
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise AMLException(e,sys)
    def export_data_into_feature_store(self) -> pd.DataFrame:
        """
        Export mongodb collection record as dataframe into feature store
        """
        try:
            logging.info("Exporting data from mongodb database to feature store")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # creating folder 
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok= True)
            transactional_data = TransactionData()
            data_frame = transactional_data.export_collection_as_dataframe(collection_name= self.data_ingestion_config.collection_name)
            data_frame.to_csv(feature_store_file_path,index = False, header = True)
            return data_frame
        except Exception as e:
            raise AMLException(e,sys)
    def split_into_train_test(self,dataframe: pd.DataFrame):
        try:
            logging.info("Split the data into train and test using stratified sampling in data ingestion class")

# Separate the features and target variable
            X = dataframe.drop(TARGET_COLUMN, axis=1)
            y = dataframe[TARGET_COLUMN]
   
            logging.info("Split the data into training and testing sets with stratified sampling")
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.data_ingestion_config.train_test_split_ratio, stratify=y, random_state=42)
        
            # Join the X_train and y_train data into one DataFrame
            training_dataframe = pd.concat([X_train, y_train], axis=1)
            testing_dataframe = pd.concat([X_test, y_test], axis=1)
    
            logging.info("Exited train_test_split method of Data_Ingestion_class")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok= True)
            logging.info('Storing training and testing data in ingested directory')
            training_dataframe.to_csv(self.data_ingestion_config.training_file_path,index =False, header= True)
            testing_dataframe.to_csv(self.data_ingestion_config.testing_file_path,index = False,header = True)
            logging.info('Successfully stored the training and testing data')
        except Exception as e:
            raise AMLException(e,sys)
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info('start the data ingestion phase')
            dataframe = self.export_data_into_feature_store()
            self.split_into_train_test(dataframe=dataframe)
            training_file_path = self.data_ingestion_config.training_file_path
            testing_file_path = self.data_ingestion_config.testing_file_path
            data_ingestion_artifact = DataIngestionArtifact(feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                                                            training_file_path=training_file_path,
                                                            testing_file_path=testing_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise AMLException(e,sys)