

from src.Predictive_Maintainance.components.data_ingestion import DataIngestion
from src.Predictive_Maintainance.components.data_transformation import DataTransformation
from src.Predictive_Maintainance.components.model_trainer import ModelTrainer





import os , sys

from src.Predictive_Maintainance.logger import logging
from src.Predictive_Maintainance.exception import CustomException

import pandas as pd

obj  = DataIngestion()
raw_data_path = obj.initiate_data_ingestion()



data_trainformation = DataTransformation()
df = data_trainformation.initiate_data_transformation(raw_data_path)
 

