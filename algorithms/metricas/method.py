from sklearn.preprocessing import StandardScaler, MinMaxScaler  
from scipy.spatial.distance import cdist    # Para el cálculo de distancias
from scipy.spatial import distance
import pandas as pd

def escalar(df):
       estandarizar = StandardScaler()
       estandarizado = estandarizar.fit_transform(df)  
       return estandarizado
def normalizar(df):
       normalizar = MinMaxScaler()
       estandarizado = normalizar.fit_transform(df)  
       return estandarizado

""" ——— Metricas ———"""
def matriz_distancia(type,num,MEstandarizada):
	if type != 'Minkowski':
		DstEuclidiana = cdist(MEstandarizada, MEstandarizada, metric=type)
		M = pd.DataFrame(DstEuclidiana)
		return M
	else:
		DstEuclidiana = cdist(MEstandarizada, MEstandarizada, metric=type,p=num)
		M = pd.DataFrame(DstEuclidiana)
		return M
	