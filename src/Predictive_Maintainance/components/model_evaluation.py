import os
import sys
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
import pickle
from src.DimondPricePrediction.utils.utils import load_object
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score, classification_report




class ModelEvaluation:
    def __init__(self):
        pass

    
    def eval_metrics(self,actual, pred):
        scores = []
        acc = accuracy_score(actual, pred) * 100
        prec = precision_score(actual, pred) * 100
        rec = recall_score(actual, pred) * 100
        f1 = f1_score(actual, pred) * 100
        scores.append([acc, prec, rec, f1])
        return acc, prec, rec, f1, scores


    def initiate_model_evaluation(self,train_array,test_array):
        try:
            X_test,y_test=(test_array[:,:-1], test_array[:,-1])

            model_path=os.path.join("artifacts","model.pkl")
            model=load_object(model_path)

        

            mlflow.set_registry_uri("https://dagshub.com/sunny.savita/fsdsmendtoend.mlflow")
            
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
            
            print(tracking_url_type_store)



            with mlflow.start_run():

                predicted_qualities = model.predict(X_test)

                (rmse, mae, r2) = self.eval_metrics(y_test, predicted_qualities)

                mlflow.sklearn.log_model(m, model_name[i])
                mlflow.log_metric("Accuracy", acc)
                mlflow.log_metric("Precision", prec)
                mlflow.log_metric("Recall", rec)
                mlflow.log_metric("F1", f1)


                # this condition is for the dagshub
                # Model registry does not work with file store
                if tracking_url_type_store != "file":

                    # Register the model
                    # There are other ways to use the Model Registry, which depends on the use case,
                    # please refer to the doc for more information:
                    # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                    mlflow.sklearn.log_model(model, "model", registered_model_name="ml_model")
                # it is for the local 
                else:
                    mlflow.sklearn.log_model(model, "model")


                

            
        except Exception as e:
            raise e