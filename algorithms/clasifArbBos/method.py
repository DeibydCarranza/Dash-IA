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

# max_depth_glo = None
# min_samples_split_glo=None
# min_samples_leaf_glo=None
# random_state_glo=None
# n_estimators_glo=None

""" Variables predictoras y variables de clase """
def variablesClasePredict(df,columns_values,claseSalida,size,random_s,shuffle):
    # Variables predictoras
    X = np.array(df[columns_values])

    #Variable clase
    Y = np.array(df[claseSalida])

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


"""  ---  MODELADO DE ÁRBOLES --- """
""" Entrenamiento de árbol """
def trainingTrees(columns_values, X_train, X_validation, Y_train, Y_validation, depth,samples_split,samples_leaf,random_s):
        # Validar y asignar los valores por defecto si los argumentos son None
    print(depth,samples_split,samples_leaf,random_s)
    if samples_split is None:
        samples_split = 2
    if samples_leaf is None:
        samples_leaf = 1
    # if random_s is None:
    #     random_s = 0
    print("----------")
    print(depth,samples_split,samples_leaf,random_s)
    #Se entrena el modelo a partir de los datos de entrada
    ClasificacionAD = DecisionTreeClassifier(max_depth = depth, min_samples_split = samples_split, 
                                             min_samples_leaf = samples_leaf, random_state = random_s)
    ClasificacionAD.fit(X_train, Y_train)

    #Se etiquetan las clasificaciones
    Y_ClasificacionAD = ClasificacionAD.predict(X_validation)
    ValoresAD = pd.DataFrame(Y_validation, Y_ClasificacionAD)

    #Se calcula la exactitud promedio de la validación
    score = ClasificacionAD.score(X_validation, Y_validation)

    #modelValidation(columns_values)

    print("+++++++++++++++++++++++++++++++")
    print(score)
    print(Y_ClasificacionAD)
    print(ClasificacionAD.fit(X_train, Y_train))







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
    layout = lay.section_graphs_interactive(exactitud,report,Matriz_Clasificacion,TypeG,X_validation,Y_validation,ClasificacionRL,columns_values)

    return layout


# """ Extrayendo valores desde callback para ser usados desde method.py """
# def setterParamsTree(X_t, X_val, Y_t, Y_val,max_depth,min_samples_split,min_samples_leaf,random_state):
#     global max_depth_glo, min_samples_split_glo, min_samples_leaf_glo, random_state_glo
    
#     max_depth_glo = max_depth
#     min_samples_split_glo = min_samples_split
#     min_samples_leaf_glo = min_samples_leaf
#     random_state_glo = random_state

# def setterParamsForest(max_depth,min_samples_split,min_samples_leaf,random_state,n_estimators):
#     global max_depth_glo, min_samples_split_glo, min_samples_leaf_glo, random_state_glo, n_estimators_glo
    
#     max_depth_glo = max_depth
#     min_samples_split_glo = min_samples_split
#     min_samples_leaf_glo = min_samples_leaf
#     random_state_glo = random_state
#     n_estimators_glo = n_estimators