from aml.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from aml.entity.config_entity import DataTransformationConfig
from aml.exception import AMLException
from aml.constant.training_pipeline import TARGET_COLUMN  ,ID_COLUMN
from aml.utils.main_utils import save_numpy_array_data,save_object
from aml.ml.model.estimator import TargetValueMapping
import sys,os
import numpy as np 
import pandas as pd
from aml.logger import logging
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,data_validation_artifact:DataValidationArtifact):

        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise AMLException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise AMLException(e, sys)

    def preproccessing(self,X,y):
        try:
            
            smt = SMOTETomek(random_state = 42,sampling_strategy = 'minority', n_jobs = -1)
            # Fit the model to generate the data
            X_res,y_res = smt.fit_resample(X,y)
            return X_res,y_res
        except Exception as e:
            raise AMLException(e,sys)
    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            robust_scaler = RobustScaler()
            simple_imputer = SimpleImputer(strategy= "constant",fill_value= 0)
            
            preprocessor = Pipeline(
                steps= [
                    ("Imputer",simple_imputer), # replace missing value with zeros
                    ("RobustScaler",robust_scaler) #keep every feature in same range and handle outliers
                ]
            )
            return preprocessor
        except Exception as e:
            raise AMLException(e, sys) from e


    def initiate_data_tranformation(self) -> DataTransformationArtifact:
        try:
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            preprocessor = self.get_data_transformer_object()
            
            #training dataframe 
            input_feature_train_df = train_df.drop(columns = [TARGET_COLUMN],axis =1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.map(TargetValueMapping().to_dict())

            #testing dataframe 
            input_feature_test_df = test_df.drop(columns = [TARGET_COLUMN],axis =1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.map(TargetValueMapping().to_dict())

            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_features = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_features  = preprocessor_object.transform(input_feature_test_df)

            smt = SMOTETomek(sampling_strategy="minority")

            input_feature_train_final,target_feature_train_final = smt.fit_resample(
                transformed_input_train_features,target_feature_train_df
            )

            input_feature_test_final,target_feature_test_final = smt.fit_resample(
                transformed_input_test_features,target_feature_test_df
            )
            
            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final) ]
            test_arr = np.c_[ input_feature_test_final, np.array(target_feature_test_final) ]

            #save numpy array data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array= train_arr,)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array = test_arr,)
    
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor)

            #preparing artifact
            data_transfomation_artifact = DataTransformationArtifact(transformed_object_file_path= self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path= self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path= self.data_transformation_config.transformed_test_file_path,
            )
            logging.info("Data transformation artifact :{data_transformation_artifact}")
            return data_transfomation_artifact
        except Exception as e:
            raise AMLException(e,sys)

        
