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
def compare_elementos(df_estandar,metric,l,element1,element2):

	if metric == 'euclidean':
		d = distance.euclidean(df_estandar[element1],df_estandar[element2])
	elif metric == 'chebyshev':
		d = distance.chebyshev(df_estandar[element1],df_estandar[element2])
	elif metric == 'cityblock':
		d = distance.cityblock(df_estandar[element1],df_estandar[element2]) 
	elif metric == 'minkowski':
		d = distance.minkowski(df_estandar[element1],df_estandar[element2],p=int(l))
	else:
		d = ''
	return d
