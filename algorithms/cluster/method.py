from sklearn.preprocessing import StandardScaler, MinMaxScaler  
from scipy.spatial.distance import cdist    # Para el cálculo de distancias
from scipy.spatial import distance
import pandas as pd
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering
from .import tool as tl

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

def creat_cluster_tags(df,MEstandarizada,numClusters,metrica):	
	MJerarquico = AgglomerativeClustering(n_clusters=int(numClusters), linkage='complete', metric=metrica)
	MJerarquico.fit_predict(MEstandarizada)
	MJerarquico.labels_
	df['clusterH'] = MJerarquico.labels_
	render = tl.render_results(df)
	return df,render 

def panorama_general_cluster(df):
	centroidesH = {}

	# Calcular el valor promedio de cada columna en cada cluster
	for col in df.columns[1:]:
		centroidesH[col] = df.groupby('clusterH')[col].mean()

	# Crear el dataframe a partir del diccionario
	centroidesH_df = pd.DataFrame(centroidesH)

	# Eliminar el índice generado y reemplazarlo con la columna 'clusterH'
	centroidesH_df = centroidesH_df.reset_index(drop=True)
	print(centroidesH_df)
	return centroidesH_df
