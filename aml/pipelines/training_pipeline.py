from aml.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelEvaluationConfig,ModelPusherConfig,ModelTrainerConfig
from aml.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelEvaluationArtifact,ModelTrainerArtifact,ModelPusherArtifact
from aml.components.data_ingestion import DataIngestion
from aml.components.data_validation import DataValidation
from aml.components.data_transformation import DataTransformation
from aml.components.model_trainer import ModelTrainer
from aml.components.model_evaluation import ModelEvaluation
from aml.components.model_pusher import ModelPusher
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
        
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            TrainPipeline.is_pipeline_running=True
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info("Model Trainer artifact completed:{model_trainer_artifact}")
            return model_trainer_artifact
        except  Exception as e:
            raise  AMLException(e,sys)
        
    def start_model_evaluation(self,data_validation_artifact:DataValidationArtifact,
                                 model_trainer_artifact:ModelTrainerArtifact,
                                ):
        try:
            model_evaluation_config = ModelEvaluationConfig(self.training_pipeline_config)
            model_evaluation = ModelEvaluation(model_evaluation_config, data_validation_artifact, model_trainer_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact
        except  Exception as e:
            raise  AMLException(e,sys)
    
    def start_model_pusher(self,model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            model_pusher_config = ModelPusherConfig(training_pipeline_config= self.training_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config= model_pusher_config,
                                            model_evaluation_artifact= model_evaluation_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            logging.info("Model pusher completed: {model_pusher_artifact}")
            return model_pusher_artifact
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

            data_transformation_artifact: DataTransformationArtifact = self.start_data_transformation(data_validation_artifact)
            logging.info("Data Transformation phase completed")

            model_trainer_artifact: ModelTrainerArtifact = self.start_model_trainer(data_transformation_artifact= data_transformation_artifact)
            logging.info("Model trainer phase completed")

            model_evaluation_artifact = self.start_model_evaluation(data_validation_artifact, model_trainer_artifact)
            if not model_evaluation_artifact.is_model_accepted:
                raise Exception("Trained model is not better than the best model")
            logging.info("Model evaluation completed")

            model_pusher_artifact: ModelPusherArtifact = self.start_model_pusher(model_evaluation_artifact= model_evaluation_artifact)
            TrainPipeline.is_pipeline_running=False
            logging.info("Model pusher completed ")

        except Exception as e:
            raise AMLException(e,sys)
        


    