

from src.Predictive_Maintainance.components.data_ingestion import DataIngestion



import os , sys

from src.Predictive_Maintainance.logger import logging
from src.Predictive_Maintainance.exception import CustomException

import pandas as pd

obj  = DataIngestion()

raw_data_path = obj.initiate_data_ingestion()