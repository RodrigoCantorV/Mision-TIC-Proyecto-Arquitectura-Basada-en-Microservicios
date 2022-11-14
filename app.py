import datetime
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager
from waitress import serve
import requests
import json

app = Flask(__name__)
cors = CORS(app)
app.config["JWT_SECRET_KEY"] = "hola"
jwt = JWTManager(app)

@app.route("/login",methods = ["POST"])
def inicio_sesion():
    dataConfig = loadFileConfig()
    datosEntrada = request.get_json()
    headers = {'content-type':'application/json; charset= utf8'}
    print(datosEntrada)
    respuesta = requests.post(dataConfig["url-ms-usuarios"]+"/login", json=datosEntrada, headers=headers)
    print(dataConfig["url-ms-usuarios"]+"/login")
    print(respuesta.status_code)
    print(respuesta.json())
    if respuesta.status_code == 200:
        usuario = respuesta.json()
        tiempo_uso = datetime.timedelta(60*60*24)
        token_acceso = create_access_token(identity=usuario,expires_delta=tiempo_uso)
        return jsonify({"Token de accceso: ":token_acceso,"Usuario":usuario})
    else:
        return jsonify({"mensaje":"Unauthorized> verifique su usuario y contraseña"})

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-api-gateway"]+":" + str(dataConfig["puerto-gateway"]))
    serve(app,host=dataConfig["url-api-gateway"],port=dataConfig["puerto-gateway"])

