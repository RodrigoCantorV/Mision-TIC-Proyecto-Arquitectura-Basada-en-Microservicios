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
        tiempo_uso = datetime.timedelta(seconds=60*60*24)
        token_acceso = create_access_token(identity=usuario,expires_delta=tiempo_uso)
        return jsonify({"Token de accceso: ":token_acceso, "user_id": usuario["_id"]})
        #return jsonify({"Token de accceso: ": token_acceso, "Usuario": usuario})
    else:
        return jsonify({"mensaje":"Unauthorized> verifique su usuario y contraseña"})


@app.before_request
def before_request_callback():
    endPoint = limpiarURL(request.path)
    excludedRoutes=["/login"]
    if excludedRoutes.__contains__(request.path):
        print("ruta excluida ",request.path)
        pass
    elif verify_jwt_in_request():
        usuario = get_jwt_identity()
        if usuario["rol"]is not None:
            print(endPoint)
            print(usuario["rol"])
            print(request.method)
            tienePersmiso = validarPermiso (endPoint,request.method,usuario["rol"]["_id"])
            if not tienePersmiso:
                return jsonify({"message": "Permission denied error numero 1"}), 401
        else:
            return jsonify({"message": "Permission denied, usuario no tiene rol error numero 2"}), 401

def limpiarURL(url):
    partes = request.path.split("/")
    for laParte in partes:
        if re.search('\\d',laParte):
            url = url.replace(laParte, "?")
    return url

def validarPermiso(endPoint, metodo, idRol):
    dataConfig = loadFileConfig()
    url =  dataConfig['url-ms-usuarios'] + '/asignar/' + str(idRol)
    tienePermiso = False
    #headers= {"Content-Type":"application/json;charset = utf - 8"}
    headers = {'content-type': 'application/json; charset= utf8'}
    body = {
        "url": endPoint,
        "metodo": metodo
            }
    response = requests.get(url, json=body, headers=headers)
    try:
        data = response.json()
        if ("_id" in data):
            tienePermiso = True
    except:
        pass
    return tienePermiso

##############################################PATHS DE PARTIDOS POLITICOS###############################################
@app.route("/partidos",methods=['GET'])
def getPartido():
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"]+'/partidos'
    response = requests.get(url,headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/partidos",methods=['POST'])
def crearPartido():
    dataConfig = loadFileConfig()
    datos = request.get_json()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/partidos'
    response = requests.post(url, headers=headers, json=datos)
    json = response.json()
    return jsonify(json)

@app.route("/partidos/<string:id>",methods=['GET'])
def listarPartido(id):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/partidos/'+ id
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/partidos/<string:id>",methods=['PUT'])
def modificarPartido(id):
    dataConfig = loadFileConfig()
    datos = request.get_json()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/partidos/'+ id
    response = requests.put(url, headers=headers, json=datos)
    json = response.json()
    return jsonify(json)

@app.route("/partidos/<string:id>",methods=['DELETE'])
def eliminarPartido(id):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/partidos/' + id
    response = requests.delete(url, headers=headers)
    json = response.json()
    return jsonify(json)
########################################################################################################################

##############################################PATHS DE PARTIDOS CANDIDATOS##############################################
@app.route("/candidatos",methods=['GET'])
def getCandidato():
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/candidatos'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/candidatos",methods=['POST'])
def crearCandidato():
    dataConfig = loadFileConfig()
    datos = request.get_json()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/candidatos'
    response = requests.post(url, headers=headers, json=datos)
    json = response.json()
    return jsonify(json)

@app.route("/candidatos/<string:id>",methods=['GET'])
def listarCandidato(id):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/candidatos/' + id
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/candidatos/<string:id>",methods=['PUT'])
def modificarCandidato(id):
    dataConfig = loadFileConfig()
    datos = request.get_json()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/candidatos/' + id
    response = requests.put(url, headers=headers, json=datos)
    json = response.json()
    return jsonify(json)

@app.route("/candidatos/<string:id>",methods=['DELETE'])
def eliminarCandidato(id):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/candidatos/' + id
    response = requests.delete(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/candidatos/<string:id_candidato>/partido/<string:id_partido>",methods=['PUT'])
def asignarPartido(id_candidato,id_partido):
    dataConfig = loadFileConfig()
    datos = request.get_json()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/candidatos/' + id_candidato + "/partido/" + id_partido
    response = requests.put(url, headers=headers, json=datos)
    json = response.json()
    return jsonify(json)
########################################################################################################################
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

