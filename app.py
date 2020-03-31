# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:11:07 2020

@author: ADI
"""

from flask import Flask, request, json
from flask import Response
from scipy.stats import zscore
from scipy.stats import ttest_ind
from scipy.stats import normaltest
from scipy.stats import shapiro
from statsmodels.stats import weightstats as stests
import pandas as pd
import numpy as np
import sys
import services as srv

app = Flask(__name__)

sample = "Do a Post with jsonData E.g {\"Sample 1\": [25.5,65.6,30, 50, 60],\"Sample 2\": [35.5,45.6,60, 70, 80, 90]}"


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/ztest',methods=['GET','POST'])
def ztst():
    if request.method == 'POST':
        try:
            if request.is_json:
                d = request.get_json()
                if len(d.items()) == 1:
                    if len(np.unique(list(d.values())[0])) > 30:
                        d = list( map(int, list(d.values())[0]))
                        ztest, pval = stests.ztest(d, x2=None, value=np.mean(d))
                        return Response(json.dumps({"Z-Test": ztest, "P-Value": pval}), status=200,
                                        mimetype='application/json')
                    else:
                        return "Sample Should Contain Unique values more than 30 OtherWise Use T-Test e.g {\"Sample 1\": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]}"
                elif len(d.items()) == 2:
                    if len(np.unique(list(d.values())[0])) > 30 and len(np.unique(list(d.values())[1])) > 30:
                        d1 = list( map(int, list(d.values())[0]))
                        d2 = list(map(int, list(d.values())[1]))
                        ztest, pval = stests.ztest(d1, d2, value=(np.mean(d1) - np.mean(d2)))
                        return Response(json.dumps({"Z-Test": ztest, "P-Value": pval}), status=200,
                                        mimetype='application/json')
                    else:
                        return "Both Sample Should Contain Unique values more than 30 OtherWise Use T-Test e.g {\"Sample 1\": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]}"
                else:
                    return sample
        except Exception as e:
            return {"Error": str(e)}
    elif request.method == 'GET':
        return sample

@app.route('/ttest-equalvariance', methods=['POST', 'GET'])
def ttest_equalvariance():
    if request.method == 'POST':
        try:
            if request.is_json:
                d = request.get_json()
                if len(d.items()) == 2:
                    result = ttest_ind(list( map(float, list(d.values())[0])), list( map(float, list(d.values())[1])), axis=0, equal_var=True)
                    result = json.dumps({"T-Value": result[0], "P-Value": result[1]})
                    return Response(result, status=200, mimetype='application/json')
                else:
                    return sample
        except Exception as e:
            return {"Error": str(e)}
    elif request.method == 'GET':
        return sample

@app.route('/ttest-unequalvariance', methods=['POST', 'GET'])
def ttest_unequalvariance():
    if request.method == 'POST':
        try:
            if request.is_json:
                d = request.get_json()
                if len(d.items()) == 2:
                    result = ttest_ind(list( map(float, list(d.values())[0])), list( map(float, list(d.values())[1])), axis=0, equal_var=False)
                    result = json.dumps({"T-Value": result[0], "P-Value": result[1]})
                    return Response(result, status=200, mimetype='application/json')
                else:
                    return sample
        except Exception as e:
            return {"Error": str(e)}
    elif request.method == 'GET':
        return sample

@app.route('/normaltest', methods=['POST', 'GET'])
def ntest():
    if request.method == 'POST':
        try:
            if request.is_json:
                d = request.get_json()
                # normality test
                #stat, p = shapiro(data)  shapiro also used for normality test
                listKeys = ['statistic','pvalue']
                d = {k: dict(zip(listKeys, list(normaltest(list(map(float, v)))))) for k, v in d.items() if len(v) > 0}
                return Response(json.dumps(d), status=200, mimetype='application/json')
        except Exception as e:
            return {"Error": str(e)}
    elif request.method == 'GET':
        return sample

#this test used to extract outliers from a data set
@app.route('/outliertest', methods=['POST', 'GET'])
def outliertest():
    if request.method == 'POST':
        try:
            if request.is_json:
                d = request.get_json()
                d = {k: srv.detect_outlier(list( map(float, v))) for k, v in d.items() if len(v) > 0}
                return Response(json.dumps(d), status=200, mimetype='application/json')
        except Exception as e:
            return {"Error": str(e)}
    elif request.method == 'GET':
        return sample

@app.route('/histogram', methods=['POST', 'GET'])
def hist():
    if request.method == 'POST':
        try:
            if request.is_json:
                d = request.get_json()
                names = list(d.keys())
                list1 = [sorted(np.unique(np.array(v))) for k, v in d.items() if len(v) > 0]
                list2 = [np.histogram(list(map(int, sorted(v))), bins=np.array(list(map(int, sorted(v)))).max() + 1)[0] for k, v in d.items() if len(v) > 0]
                list2 = [x[x.nonzero()].tolist() for x in list2]
                i = 0
                resultList = {}
                for x in list1:
                    resultList[names[i]] = str(dict(zip(x, list2[i])))
                    i = i + 1

                return Response(json.dumps(resultList), status=200, mimetype='application/json')
        except Exception as e:
            return {"Error": str(e)}
    elif request.method == 'GET':
        return sample

@app.route('/zvalue', methods=['POST', 'GET'])
def zvalue():
    if request.method == 'POST':
        try:
            if request.is_json:
                d = request.get_json()
                d = {k: list(zscore(list(map(float, v)))) for k, v in d.items() if len(v) > 0}
                return Response(json.dumps(d), status=200, mimetype='application/json')
        except Exception as e:
            return {"Error": str(e)}
    elif request.method == 'GET':
        return sample

@app.route('/max', methods=['POST', 'GET'])
def mx():
    if request.method == 'POST':
        try:
            if request.is_json:
                d = request.get_json()
                return srv.process(d, 'max')
        except Exception as e:
            return {"Error": str(e)}
    elif request.method == 'GET':
        return sample

@app.route('/min', methods=['POST', 'GET'])
def mn():
    if request.method == 'POST':
        try:
            if request.is_json:
                d = request.get_json()
                return srv.process(d, 'min')
        except Exception as e:
            return {"Error": str(e)}
    elif request.method == 'GET':
        return sample


@app.route('/range', methods=['POST', 'GET'])
def rng():
    if request.method == 'POST':
        try:
            if request.is_json:
                d = request.get_json()
                return srv.process(d, 'range')
        except Exception as e:
            return {"Error": str(e)}
    elif request.method == 'GET':
        return sample


@app.route('/kurtosis', methods=['POST', 'GET'])
def kurt():
    if request.method == 'POST':
        try:
            if request.is_json:
                d = request.get_json()
                return srv.process(d, 'kurtosis')
        except Exception as e:
            return {"Error": str(e)}

    elif request.method == 'GET':
        return sample


@app.route('/skew', methods=['POST', 'GET'])
def sk():
    if request.method == 'POST':
        try:
            if request.is_json:
                d = request.get_json()
                return srv.process(d, 'skew')
        except Exception as e:
            return {"Error": str(e)}
    elif request.method == 'GET':
        return sample


@app.route('/variance', methods=['POST', 'GET'])
def variance():
    if request.method == 'POST':
        try:
            if request.is_json:
                d = request.get_json()
                return srv.process(d, 'variance')
        except Exception as e:
            return {"Error": str(e)}

    elif request.method == 'GET':
        return sample


@app.route('/std', methods=['POST', 'GET'])
def std():
    if request.method == 'POST':
        try:
            if request.is_json:
                d = request.get_json()
                return srv.process(d, 'std')
        except Exception as e:
            return {"Error": str(e)}

    elif request.method == 'GET':
        return sample


@app.route('/mean', methods=['POST', 'GET'])
def take_mean():
    if request.method == 'POST':
        try:
            if request.is_json:
                d = request.get_json()
                return srv.process(d, 'mean')
        except Exception as e:
            return {"Error": str(e)}
    elif request.method == 'GET':
        return sample


if __name__ == '__main__':
    app.run()
