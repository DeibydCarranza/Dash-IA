import pandas as pd
import plotly.graph_objects as go
from apyori import apriori

# Gráfica de frecuencias de las transacciones
def graphFrecu(transac_data):
    #Se incluyen todas las transacciones en una sola lista
    Transacciones = transac_data.values.reshape(-1).tolist() 

    #Se crea una matriz (dataframe) usando la lista y se incluye una columna 'Frecuencia'
    Lista = pd.DataFrame(Transacciones)
    Lista['Frecuencia'] = 1

    #Se agrupa los elementos
    Lista = Lista.groupby(by=[0], as_index=False).count().sort_values(by=['Frecuencia'], ascending=True) #Conteo
    Lista['Porcentaje'] = (Lista['Frecuencia'] / Lista['Frecuencia'].sum()) #Porcentaje
    Lista = Lista.rename(columns={0 : 'Item'})

    return img_gen(Lista)


def img_gen(Lista):
    fig = go.Figure([go.Bar(x=Lista['Frecuencia'], y=Lista['Item'], 
                    orientation='h',marker=dict(color='green'))])
    fig.update_layout(
        title='Distribución de los datos',
        xaxis_title='Frecuencia',
        yaxis_title='Elemento',
        height=1000,
        font=dict(
            family='Arial',
            size=12
        )
    )
    return fig

# Cálculo de las reglas de acuerdo a los parámetros de entrada
def application(dataSet, support, confidence, lift):
    dataSet = dataSet.stack().groupby(level=0).apply(list).tolist() 
    ReglasC1 = apriori(dataSet, 
                   min_support=support, 
                   min_confidence=confidence, 
                   min_lift=lift)
    ResultadosC1 = list(ReglasC1)
    resultados = []
    for item in ResultadosC1:
        Emparejar = item[0]
        items = [x for x in Emparejar]
        regla = ', '.join(items).strip('{}')
        antecedente = ', '.join(item[2][0][0]).strip('{}')
        consecuente = ', '.join(item[2][0][1]).strip('{}')
        resultados.append({
            'Regla': regla,
            'Antecedente': antecedente,
            'Consecuente': consecuente,
            'Soporte': "{:.3f}%".format(item[1] * 100),
            'Confianza': "{:.3f}%".format(item[2][0][2] * 100),
            'Elevación': "{:.3f}".format(item[2][0][3])
        })
    
    df_resultados = pd.DataFrame(resultados)
    return df_resultados


