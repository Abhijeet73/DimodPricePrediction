import os
import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException


from src.components.data_ingetion import DataIngestion
from src.components.data_transformation import DataTransformation

if __name__ == "__main__":
    obj=DataIngestion()
    train_data_path, test_data_path = obj.initiate_data_ingestion()
    print(train_data_path, test_data_path)
    data_transformation = DataTransformation()
    train_arr,test_arr,obj_path=data_transformation.initiate_data_transformation(train_data_path, test_data_path)