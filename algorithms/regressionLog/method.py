import pandas as pd
import plotly.express as px       
import plotly.graph_objects as go
from dash import dcc, html,dash_table
from . import layout as lay

import numpy as np 
from sklearn import model_selection
from sklearn import linear_model
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve
from sklearn.metrics import RocCurveDisplay
from sklearn.metrics import accuracy_score  
import dash_bootstrap_components as dbc


ClasificacionRL = None
X_validation= None
Y_validation = None
Y_ClasificacionRL = None
TypeG = "Diabetes"

# Variables predictoras y variables de clase
def variablesClasePredict(df,columns_values,claseSalida,size,random_s,shuffle):
    global TypeG
    if claseSalida == 'Diagnosis':
        df = df.replace({'M': 0, 'B': 1})
        TypeG = 'Cáncer'

    #Variables predictoras
    X = np.array(df[columns_values])

    #Variable clase
    Y = np.array(df[claseSalida])

    score = entrenamiento(X,Y,size,random_s,shuffle)

#Entrenamiendo del modelo
def entrenamiento(X,Y,size,random_s,shuffle):
    global ClasificacionRL,X_validation,Y_validation,Y_ClasificacionRL

    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, 
                                                                test_size = size, 
                                                                random_state = random_s,
                                                                shuffle = shuffle)
    #Se entrena el modelo a partir de los datos de entrada
    ClasificacionRL = linear_model.LogisticRegression()
    ClasificacionRL.fit(X_train, Y_train)

    #Predicciones probabilísticas de los datos de prueba
    Probabilidad = ClasificacionRL.predict_proba(X_validation)

    #Clasificación final 
    Y_ClasificacionRL = ClasificacionRL.predict(X_validation)


# Validación del modelo
def modelValidation():
    global ClasificacionRL,X_validation,Y_validation,Y_ClasificacionRL
    ModeloClasificacion = ClasificacionRL.predict(X_validation)
    Matriz_Clasificacion = pd.crosstab(Y_validation.ravel(), 
                                   ModeloClasificacion, 
                                   rownames=['Reales'], 
                                   colnames=['Clasificación']) 
    
    exactitud = accuracy_score(Y_validation,Y_ClasificacionRL)

    report = classification_report(Y_validation, Y_ClasificacionRL)


    ## ------ Gráficas y Layout
    layout = lay.section_graphs_interactive(exactitud,report,Matriz_Clasificacion,TypeG,X_validation,Y_validation,ClasificacionRL)

    return layout



