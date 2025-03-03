from flask import Flask, render_template, request, session
from petprocessing import petcalc
from petprocessingprognose import petcalcprognose
import numpy as np
import Solweig_v2015_metdata_noload as metload
import clearnessindex_2013b as ci
import requests
import json
import base64
import pandas as pd


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "klefiedoedfoiefnnoefnveodf"

result = []

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/petresult', methods=["GET", "POST"])
def petresult():
    return render_template("petresult.html", result=result)

@app.route('/prognoseerror', methods=["GET", "POST"])
def prognoseerror():
    return render_template("prognoseerror.html", result=result)

@app.route('/prognose', methods=["INSERT", "AUTO"])
def prognose():
    if request.method == "GET":
        return render_template("prognose.html")

    if request.method == "POST":
        city = request.form["city"]
        if city == 'Gothenburg, Sweden':
            url = 'https://api.github.com/repos/David-Rayner-GVC/pet_data/contents/json/Gothenburg.json'
        else:
            return render_template("prognoseerror.html", result='Prognose for ' + city + ', not found.')

        # download data from github
        req = requests.get(url)
        if req.status_code == requests.codes.ok:
            req = req.json()  # the response is a JSON
            content = base64.b64decode(req['content'])
        else:
            return render_template("petprognoseresult.html", result='Content was not found.')

        dict_loaded = json.loads(content)

        for key, value in dict_loaded['data_vars'].items():
            dict_loaded['data_vars'][key]['data'] = [np.nan if isinstance(x,str) else x for x in value['data'] ]

        timestamp = dict_loaded['coords']['time']['data']

        tab.columns = ['Day of Year', 'Hour','T_air','RH','Tmrt', 'PET']
        tabhtml = tab.to_html(classes='data', header="true")
        return render_template("petprognoseresult.html", result1=doy, result2=hour, result3=tabhtml)


@app.route('/petprognoseresult', methods=["GET", "POST"])
def petprognoseresult():
    if request.method == "GET":
        return render_template("petprognoseresult.html", result1=result1, result2=result2, result3=result3)

    if request.method == "POST":
        return render_template("petprognoseresult.html", result1=result1, result2=result2, result3=result3)


@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        try:
            doy = int(request.form["doy"])
        except:
            doy = -999
        try:
            year = int(request.form["year"])
        except:
            year = -999
        try:
            hour = int(request.form["hour"])
        except:
            hour = -999
        try:
            Ta = str(request.form["city"])
        except:
            Ta = -999
        try:
            RH = float(request.form["RH"])
        except:
            RH = -999
        try:
            Ws = float(request.form["Ws"])
        except:
            Ws = -999
        sky = request.form["sky"]

        if month > 12 or month < 0:
            return render_template("petresult.html", result="Incorrect month filled in")
        if day > 31 or day < 0:
            return render_template("petresult.html", result="Incorrect day filled in")
        if hour > 23 or hour < 0:
            return render_template("petresult.html", result="Incorrect hour filled in")
        if Ta > 60 or Ta < -60:
            return render_template("petresult.html", result="Unreasonable air temperature filled in")
        if RH > 100 or RH < 0:
            return render_template("petresult.html", result="Unreasonable relative humidity filled in")
        if Ws > 100 or Ws < 0:
            return render_template("petresult.html", result="Unreasonable Wind speed filled in")

        return render_template("petresult.html", result=result)
