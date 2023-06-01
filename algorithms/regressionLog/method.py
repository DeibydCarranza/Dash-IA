import pandas as pd        
import numpy as np 
from sklearn import model_selection
from sklearn import linear_model
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score  

# Variables predictoras y variables de clase
def variablesClasePredict(df,columns_values,clase):
    print("----------")
    X = np.array(df[columns_values])
    Y = np.array(df[clase])
    
def entrenamiento(X,Y):
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, 
                                                                test_size = 0.2, 
                                                                random_state = 1234,
                                                                shuffle = True)