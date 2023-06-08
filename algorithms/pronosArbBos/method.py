import numpy as np 
import pandas as pd
from . import layout as lay
from sklearn import model_selection
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

"""" Suprimiendo columnas innecesarias y quitando valores nulos"""
def sanitizationDataFrame(df):
    MatrizDatos = df.drop(columns = ['Volume', 'Dividends', 'Stock Splits'])
    MatrizDatos = MatrizDatos.dropna()
    return MatrizDatos

""" Variables predictoras y variables de clase """
def variablesClasePredict(df,size,random_s,shuffle):

    MatrizDatos = sanitizationDataFrame(df)

    # Variables predictoras
    X = np.array(MatrizDatos[['Open',
                     'High',
                     'Low']])

    #Variable clase
    Y = np.array(MatrizDatos[['Close']])

    #Entrenando el modelo
    X_t, X_val, Y_t, Y_val = modelCreation(X,Y,size,random_s,shuffle)

    return X_t, X_val, Y_t, Y_val

""" Creacion del modelo """
def modelCreation(X,Y,size,random_s,shuffle):

    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, 
                                                                test_size = size, 
                                                                random_state = random_s,
                                                                shuffle = shuffle)
    return X_train, X_validation, Y_train, Y_validation

