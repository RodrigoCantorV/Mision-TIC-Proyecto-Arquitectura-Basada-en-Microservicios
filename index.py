from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from waitress import serve
import json

app = Flask(__name__)
cors = CORS(app)

###################################################################################
# Importar controladores aqui

###################################################################################
@app.route("/",methods=['GET'])
def test():
    json = {}
    json["message"]="Server running ..."
    return jsonify(json)
###################################################################################
#PATHS DE PARTIDOS POLITICOS

###################################################################################
#PATHS DE CANDIDATOS

###################################################################################
#PATHS DE MESAS

###################################################################################
#PATHS DE RESULTADOS

###################################################################################
def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" + str(dataConfig["port"]))
    serve(app,host=dataConfig["url-backend"],port=dataConfig["port"])

