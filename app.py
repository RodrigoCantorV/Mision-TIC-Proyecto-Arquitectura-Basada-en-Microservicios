from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager, verify_jwt_in_request, get_jwt_identity
from waitress import serve
import requests
import json
import datetime
import re

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
    respuesta = requests.post(dataConfig["url-ms-usuarios"]+"/usuario"+"/login", json=datosEntrada, headers=headers)
    print(dataConfig["url-ms-usuarios"]+"/usuario"+"/login")
    print(respuesta.status_code)
    print(respuesta.json())
    if respuesta.status_code == 200:
        usuario = respuesta.json()
        tiempo_uso = datetime.timedelta(60*60*24)
        token_acceso = create_access_token(identity=usuario,expires_delta=tiempo_uso)
        return jsonify({"Token de accceso: ":token_acceso,"Usuario":usuario})
    else:
        return jsonify({"mensaje":"Unauthorized> verifique su usuario y contraseña"})


@app.before_request
def before_request_callback():
    endPoint = limpiarURL(request.path)
    excludedRoutes=["/login","/","/partidos"]
    if excludedRoutes.__contains__(request.path):
        print("ruta excluida ",request.path)
        pass
    elif verify_jwt_in_request():
        usuario = get_jwt_identity()
        if usuario["rol"]is not None:
            tienePersmiso = validarPermiso (endPoint,request.method,usuario["rol"]["_id"])
            if not tienePersmiso:
                return jsonify({"message": "Permission denied"}), 401
        else:
            return jsonify({"message": "Permission denied, usuario no tiene rol"}), 401

def limpiarURL(url):
    partes = request.path.split("/")
    for laParte in partes:
        if re.search('\\d',laParte):
            url = url.replace(laParte, "?")
    return url

def validarPermiso(endPoint, metodo, idRol):
    dataConfig = loadFileConfig()
    url = dataConfig["url-ms-usuarios"] + "/asignar/" + str(idRol)
    print(url)
    tienePermiso = False
    headers= {"Content-Type":"application/json;charset = utf - 8"}
    body = {"url": endPoint,"metodo": metodo}
    response = requests.get(url, json=body, headers=headers)
    try:
        data = response.json()
        if ("_id" in data):
            tienePermiso = True
    except:
        pass
    return tienePermiso

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

