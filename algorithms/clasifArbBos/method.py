import pandas as pd
import plotly.express as px       
import plotly.graph_objects as go
from dash import dcc, html,dash_table
from . import layout as lay
import dash_bootstrap_components as dbc
import numpy as np 

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn import model_selection



ClasificacionRL = None
X_validation= None
Y_validation = None
Y_ClasificacionRL = None
TypeG = ""

""" Variables predictoras y variables de clase """
def variablesClasePredict(df,columns_values,claseSalida,size,random_s,shuffle):
    print("------------------------------------------------------")
    # Variables predictoras
    X = np.array(df[columns_values])

    #Variable clase
    Y = np.array(df[claseSalida])

    #score = entrenamiento(X,Y,size,random_s,shuffle)

""" Entrenamiendo del modelo """
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



""" Validación del modelo -> dash_app.py.
Se necesitan las columnas seleccionadas para crear los inputs predictores"""
def modelValidation(columns_values):
    global ClasificacionRL,X_validation,Y_validation,Y_ClasificacionRL
    ModeloClasificacion = ClasificacionRL.predict(X_validation)
    Matriz_Clasificacion = pd.crosstab(Y_validation.ravel(), 
                                   ModeloClasificacion, 
                                   rownames=['Reales'], 
                                   colnames=['Clasificación']) 
    
    exactitud = accuracy_score(Y_validation,Y_ClasificacionRL)

    report = classification_report(Y_validation, Y_ClasificacionRL)


    ## ------ Gráficas y Layout
    layout = lay.section_graphs_interactive(exactitud,report,Matriz_Clasificacion,TypeG,X_validation,Y_validation,ClasificacionRL,columns_values,app)

    return layout



