import numpy as np 
import pandas as pd
from . import layout as lay
from sklearn import model_selection
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

isForest = None

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


"""  ---  MODELADO DE ALGORITMOS --- """
""" Entrenamiento de árbol """
def trainingTrees(X_train, X_validation, Y_train, Y_validation, depth,samples_split,samples_leaf,random_s):
    global isForest
    isForest = False

    # Establecer valores por defecto si son None
    print(depth,samples_split,samples_leaf,random_s)
    if samples_split is None:
        samples_split = 2
    if samples_leaf is None:
        samples_leaf = 1
    
    #Se entrena el modelo a partir de los datos de entrada
    PronosticoAD = DecisionTreeRegressor(max_depth = depth, min_samples_split = samples_split, 
                                             min_samples_leaf = samples_leaf, random_state = random_s)
    PronosticoAD.fit(X_train, Y_train)

    #Se etiquetan los pronosticos
    Y_PronosticoAD = PronosticoAD.predict(X_validation)
    ValoresAD = pd.DataFrame(Y_validation, Y_PronosticoAD)

    layout = modelValidation(PronosticoAD, Y_validation,Y_PronosticoAD,isForest)

    print("\nCLASIFICACIÓN Arboles")
    return layout, PronosticoAD

""" Entrenamiento de bosque """
def trainingForest(X_train, X_validation, Y_train, Y_validation, depth,samples_split,samples_leaf,random_s,estimators):
    global isForest
    isForest = True

    # Establecer valores por defecto si son None
    print(depth,samples_split,samples_leaf,random_s)
    if samples_split is None:
        samples_split = 2
    if samples_leaf is None:
        samples_leaf = 1
    if estimators is None:
        estimators = 100

    #Se entrena el modelo a partir de los datos de entrada
    PronosticoBA = RandomForestRegressor(n_estimators=estimators,max_depth = depth, min_samples_split = samples_split, 
                                             min_samples_leaf = samples_leaf, random_state = random_s)
    PronosticoBA.fit(X_train, Y_train)

    #Se etiquetan los pronósticos
    Y_PronosticoBA = PronosticoBA.predict(X_validation)
    ValoresBA = pd.DataFrame(Y_validation, Y_PronosticoBA)

    layout = modelValidation(PronosticoBA, Y_validation,Y_PronosticoBA,isForest)

    print("\nCLASIFICACIÓN BOSQUE")
    return layout, PronosticoBA,Y_PronosticoBA

""" VALIDACIÓN DEL MODELO 
Se necesitan las columnas seleccionadas para crear los inputs predictores"""
def modelValidation(Pronostico,Y_validation, Y_Pronostico,isForest):

    columns_values = ['Open', 'High', 'Low']
    report = lay.pronostic_report(Pronostico,Y_validation,Y_Pronostico)

    ## ------ Gráficas y Layout
    layout = lay.section_graphs_interactive(report, Y_Pronostico, Y_validation, Pronostico, columns_values,isForest)

    return layout

"""" Prónostico con base a los parámetros de entrada """
def pronosticar(Pronostico,open_value, high_value, low_value):
    if open_value is not None and high_value is not None and low_value is not None:
        PrecioAccion = pd.DataFrame({'Open': [open_value],
                                     'High': [high_value],
                                     'Low': [low_value]})
        resultado = Pronostico.predict(PrecioAccion)
        return resultado
    else:
        return None