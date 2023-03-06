from aml.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig
from aml.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from aml.components.data_ingestion import DataIngestion
from aml.components.data_validation import DataValidation
from aml.components.data_transformation import DataTransformation
from aml.logger import logging
from aml.exception import AMLException
import sys

class TrainPipeline:
    is_pipeline_running=False

    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config= self.training_pipeline_config)
            logging.info("Starting data ingestion")
            data_ingestion = DataIngestion(data_ingestion_config= self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed and artifact : {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise AMLException(e,sys)
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Start data validation")
            data_validation= DataValidation(data_ingestion_artifact,data_validation_config= self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validate()
            logging.info("Data Validation Completed and artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise AMLException(e,sys)  
        
    def start_data_transformation(self,data_validation_artifact):
        try:
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Start Data transformation ")
            data_transformation=DataTransformation(self.data_transformation_config,data_validation_artifact=data_validation_artifact)
            data_transformation_artifact=data_transformation.initiate_data_tranformation()
            logging.info("Data Transformation phase completed and artifact:{data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise AMLException(e,sys)
        

    def run_pipeline(self):
        try:
            logging.info("Pipeline is start  running")
            TrainPipeline.is_pipeline_running = True
            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()
            logging.info("Data ingestion phase completed")

            data_validation_artifact: DataValidationArtifact = self.start_data_validation(data_ingestion_artifact)
            logging.info("Data validation phase completed")

            data_trasformation_artifact: DataTransformationArtifact = self.start_data_transformation(data_validation_artifact)
            logging.info("Data Transformation phase completed")
        except Exception as e:
            raise AMLException(e,sys)


    