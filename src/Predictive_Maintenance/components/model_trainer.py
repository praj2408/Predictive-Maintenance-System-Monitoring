import os
import sys
import pandas as pd
import numpy as np
import pickle

from dataclasses import dataclass


from src.Predictive_Maintenance.exception import CustomException
from src.Predictive_Maintenance.logger import logging

import mlflow
import mlflow.sklearn
from evidently import ColumnMapping
from evidently.test_suite import TestSuite
from evidently.test_preset import DataStabilityTestPreset

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset, ClassificationPreset
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score, classification_report


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


lr = LogisticRegression()
svc = SVC()
dt = DecisionTreeClassifier()
rf = RandomForestClassifier()

models = [lr, svc, dt, rf]
model_name = ["Logistic Regression", "SVC", "Decision Tree", "Random Forest"]


@dataclass
class ModelTrainerConfig:
    model_path_1: str = os.path.join("artifacts", "model1", "model_1.pkl") # for machine failure
    model_path_2: str = os.path.join("artifacts", "model2", "model_2.pkl") # type of failure
    
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        
        
    def Model1(self, df):
        
        X = df.drop(["Machine failure", "type_of_failure"], axis=1)
        y = df["Machine failure"]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scores1 = []
        
        for i, m in enumerate(models):
            m.fit(X_train, y_train)
            y_pred = m.predict(X_test)
            acc = accuracy_score(y_test, y_pred) * 100
            prec = precision_score(y_test, y_pred) * 100
            rec = recall_score(y_test, y_pred) * 100
            f1 = f1_score(y_test, y_pred) * 100
            scores1.append([acc, prec, rec, f1])
            
            with mlflow.start_run():
                mlflow.sklearn.log_model(m, model_name[i])
                mlflow.log_metric("Accuracy", acc)
                mlflow.log_metric("Precision", prec)
                mlflow.log_metric("Recall", rec)
                mlflow.log_metric("F1", f1)
                
            
        
        scores_df = pd.DataFrame(columns=["Model"], data=["Logistic Regression", "SVC", "Decision Tree", "Random Forest"])
        scores_df = pd.concat([scores_df, pd.DataFrame(scores1, columns=["Accuracy", "Precision", "Recall", "F1"])], axis=1)
        
        best_model_idx = scores_df["F1"].idxmax()
        best_model_name = scores_df.loc[best_model_idx, 'Model']
        best_model = models[best_model_idx]

        y_pred = best_model.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)
        report = pd.DataFrame(report).transpose()
        
        logging.info('MODEL 1')
        logging.info("Best Model: {} ".format(best_model))
        logging.info(f"Classification Report:\n{report}")
        
        
        return scores_df, best_model, best_model_name, report


    def Model2(self, df):
            
            X = df.drop(["Machine failure", "type_of_failure"], axis=1)
            y = df["type_of_failure"]
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            scores1 = []
            
            for i, m in enumerate(models):
                m.fit(X_train, y_train)
                y_pred = m.predict(X_test)
                acc = accuracy_score(y_test, y_pred) * 100
                prec = precision_score(y_test, y_pred,average='macro') * 100
                rec = recall_score(y_test, y_pred,average='macro') * 100
                f1 = f1_score(y_test, y_pred,average='macro') * 100
                scores1.append([acc, prec, rec, f1])
                
                with mlflow.start_run():
                    mlflow.sklearn.log_model(m, model_name[i])
                    mlflow.log_metric("Accuracy", acc)
                    mlflow.log_metric("Precision", prec)
                    mlflow.log_metric("Recall", rec)
                    mlflow.log_metric("F1", f1)
                    
                logging.info(f'model {i} logged to mlflow')
                
            
            scores_df = pd.DataFrame(columns=["Model"], data=["Logistic Regression", "SVC", "Decision Tree", "Random Forest"])
            scores_df = pd.concat([scores_df, pd.DataFrame(scores1, columns=["Accuracy", "Precision", "Recall", "F1"])], axis=1)
            
            best_model_idx = scores_df["F1"].idxmax()
            best_model_name = scores_df.loc[best_model_idx, 'Model']
            best_model = models[best_model_idx]

            y_pred = best_model.predict(X_test)
            report = classification_report(y_test, y_pred, output_dict=True)
            report = pd.DataFrame(report).transpose()
            
            logging.info('MODEL 2: ')
            logging.info("Best Model: {}".format(best_model))
            logging.info(f"Classification Report:\n{report}")
            
            return scores_df, best_model, best_model_name, report
    
    
    
    def initiate_model_training(self,df):
        try:
            
            _,model1,_,_= self.Model1(df)
            
            with open(self.model_trainer_config.model_path_1, 'wb') as f:
                pickle.dump(model1, f)
                
                
            _,model2,_,_= self.Model2(df)
            
            with open(self.model_trainer_config.model_path_2, 'wb') as f:
                pickle.dump(model2, f)
                
            
        except Exception as e:
            raise CustomException(e, sys)