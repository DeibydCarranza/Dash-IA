from sklearn import model_selection
from sklearn.ensemble import RandomForestRegressor,DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def sanitization(df):
    MatrizDatos = df.drop(columns = ['Volume', 'Dividends', 'Stock Splits'])
    MatrizDatos = MatrizDatos.dropna()
    return MatrizDatos