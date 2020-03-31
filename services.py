import numpy as np
import pandas as pd
from flask import Response

def detect_outlier(data_1):
    threshold = 2
    outliers = []
    mean_1 = np.mean(data_1)
    std_1 = np.std(data_1)
    for y in data_1:
        z_score = (y - mean_1) / std_1
        print(np.abs(z_score))
        if np.abs(z_score) > threshold:
            outliers.append(y)
    return outliers



def process(d, op):
    d = {k: pd.Series(v) for k, v in d.items() if len(v) > 0}
    dtPanda = pd.DataFrame(d)
    dtPanda = dtPanda.astype('float64')
    if op == 'max':
        dtPanda = dtPanda.max(axis=0, skipna=True)
    elif op == 'min':
        dtPanda = dtPanda.min(axis=0, skipna=True)
    elif op == 'range':
        dtPandaMax = dtPanda.max(axis=0, skipna=True)
        dtPandaMin = dtPanda.min(axis=0, skipna=True)
        dtPanda = dtPandaMax.sub(dtPandaMin)
    elif op == 'kurtosis':
        dtPanda = dtPanda.kurt(axis=0, skipna=True)
    elif op == 'skew':
        dtPanda = dtPanda.skew(axis=0, skipna=True)
    elif op == 'variance':
        dtPanda = dtPanda.var(axis=0, skipna=True)
    elif op == 'std':
        dtPanda = dtPanda.std(axis=0, skipna=True)
    elif op == 'mean':
        dtPanda = dtPanda.mean(axis=0, skipna=True)
    return Response(dtPanda.to_json(), mimetype='application/json')
