from sklearn.impute import SimpleImputer ## HAndling Missing Values
from sklearn.preprocessing import StandardScaler # HAndling Feature Scaling
from sklearn.preprocessing import OrdinalEncoder # Ordinal Encoding
## pipelines
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np 
import warnings
warnings.filterwarnings('ignore')

from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
import os, sys

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os .path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    

    def data_transformation_object(self):
        try:
            logging.info('Data Transformation initiated')
            # Segregating numerical and categorical variables
            categorical_cols = ['cut', 'color','clarity']
            numerical_cols = ['carat', 'depth','table', 'x', 'y', 'z']
            
            # Define the custom ranking for each ordinal variable
            ## For Domain Purpose https://www.americangemsociety.org/ags-diamond-grading-system/
            cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']

            logging.info("Data transformation pipeline initiated")

            ## numeric pipeline 
            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )

            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("OrdinalEncoder",OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories])),
                    ("scaler",StandardScaler())
                    ]
            )

            preprocessor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_cols),
                    ("cat_pipeline",cat_pipeline,categorical_cols)
                ]
            )
            logging.info("Data transformation completed")
            return preprocessor


        except Exception as e:
            logging.error('Error in Data Transformation')
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self, train_path, test_path):
        try:
            logging.info('Data Transformation initiated')
            # Read the data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Data read successfully')
            logging.info(f"train_df head \n {train_df.head().to_string()}")
            logging.info(f"test_df head \n {test_df.head().to_string()}")

            preprocessor_obj=self.data_transformation_object()

            target='price'
            # input_feature=train_df.drop(columns=[target,'id'])
            # target_feature=test_df
            # ## data transformation
            # input_feature_arr=preprocessor_obj.fit(input_feature)
            # target_feature_arr=preprocessor_obj.fit_transform(target_feature)




            
            # Separate features and target variable
            X_train = train_df.drop(columns=[target,'id'])
            y_train = train_df[target]
            X_test = test_df.drop(columns=[target,'id'])
            y_test = test_df[target]

            ## Data transformation
            X_train_transformed=preprocessor_obj.fit_transform(X_train)
            X_test_transformed=preprocessor_obj.transform(X_test)
            
            #y_train_transformed=preprocessor_obj.transform(y_train)
            # y_test_transformed=preprocessor_obj.fit_transform(y_test)

            logging.info('Appling preprocessing on train and test dataset')

            train_arr=np.c_[X_train_transformed,np.array(y_train)]
            test_arr=np.c_[X_test_transformed,np.array(y_test)]    

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_obj

            )

            logging.info('Processsor pickle in created and saved')

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )        



        
        except Exception as e:
            logging.error('Error during data transformation')
            raise CustomException(e, sys)