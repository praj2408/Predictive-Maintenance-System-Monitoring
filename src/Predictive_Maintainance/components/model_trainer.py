import os
import sys
import pandas as pd
import numpy as np

from dataclasses import dataclass
from src.Predictive_Maintainance.exception import CustomException
from src.Predictive_Maintainance.logger import logging


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score, classification_report






@dataclass
class ModelTrainerConfig:
    trained_model_file_path_1: str = os.path.join("artifacts", "model_1.pkl") # binary classification
    trained_model_file_path_2: str = os.path.join("artifacts", "model_2.pkl") # type of failure
    
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_training(self, train_array, test_array):
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys)