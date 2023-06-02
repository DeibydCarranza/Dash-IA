from sklearn.preprocessing import StandardScaler, MinMaxScaler  

def escalar(df):
       estandarizar = StandardScaler()
       estandarizado = estandarizar.fit_transform(df)  
       return estandarizado
def normalizar(df):
       normalizar = MinMaxScaler()
       estandarizado = normalizar.fit_transform(df)  
       return estandarizado