from aml.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from aml.entity.artifact_entity import DataIngestionArtifact
from aml.components.data_ingestion import DataIngestion
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
        

    def run_pipeline(Self):
        try:
            logging.info("Pipeline is start  running")
            TrainPipeline.is_pipeline_running = True
            data_ingestion_artifact: DataIngestionArtifact = Self.start_data_ingestion()
            logging.info("Data ingestion phase completed")
            
            
        except Exception as e:
            raise AMLException(e,sys)


    