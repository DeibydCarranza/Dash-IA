import pandas as pd        
import numpy as np 
from sklearn import model_selection
from sklearn import linear_model
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score  

ClasificacionRL = None
X_validation= None
Y_validation = None
Y_ClasificacionRL = None

# Variables predictoras y variables de clase
def variablesClasePredict(df,columns_values,claseSalida,size,random_s,shuffle):

    #Variables predictoras
    X = np.array(df[columns_values])

    #Variable clase
    Y = np.array(df[claseSalida])

    score = entrenamiento(X,Y,size,random_s,shuffle)
    return score

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
    score = accuracy_score(Y_validation, Y_ClasificacionRL)

    return score
    # X = np.array(BCancer[['Texture', 
    #                   'Area', 
    #                   'Smoothness', 
    #                   'Compactness', 
    #                   'Symmetry', 
    #                   'FractalDimension']])

# Validación del modelo
def modelValidation():
    global ClasificacionRL,X_validation,Y_validation,Y_ClasificacionRL
    ModeloClasificacion = ClasificacionRL.predict(X_validation)
    Matriz_Clasificacion = pd.crosstab(Y_validation.ravel(), 
                                   ModeloClasificacion, 
                                   rownames=['Reales'], 
                                   colnames=['Clasificación']) 
    exactitud = accuracy_score(Y_validation,Y_ClasificacionRL)