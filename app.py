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

##################################################PATHS DE CANDIDATOS###################################################
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

#####################################################PATHS DE MESAS#####################################################
@app.route("/mesas",methods=['GET'])
def getMesas():
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/mesas'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/mesas",methods=['POST'])
def crearMesa():
    dataConfig = loadFileConfig()
    datos = request.get_json()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/mesas'
    response = requests.post(url, headers=headers, json=datos)
    json = response.json()
    return jsonify(json)

@app.route("/mesas/<string:id>",methods=['GET'])
def getMesa(id):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/mesas/' + id
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/mesas/<string:id>",methods=['PUT'])
def modificarMesa(id):
    dataConfig = loadFileConfig()
    datos = request.get_json()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/mesas/' + id
    response = requests.put(url, headers=headers, json=datos)
    json = response.json()
    return jsonify(json)

@app.route("/mesas/<string:id>",methods=['DELETE'])
def eliminarMesa(id):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/mesas/' + id
    response = requests.delete(url, headers=headers)
    json = response.json()
    return jsonify(json)
########################################################################################################################

##################################################PATHS DE RESULTADOS###################################################
@app.route("/resultados",methods=['GET'])
def getResultados():
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/resultados'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/resultado/candidato/<string:id_candidato>/mesa/<string:id_mesa>",methods=['POST'])
def crearResultado(id_candidato,id_mesa):
    dataConfig = loadFileConfig()
    datos = request.get_json()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/resultados/cansidato/' + id_candidato + '/mesa/' + id_mesa
    response = requests.put(url, headers=headers, json=datos)
    json = response.json()
    return jsonify(json)

@app.route("/resultado/<string:id>",methods=['GET'])
def getResultado(id):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/resultado/' + id
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/resultado/<string:id_resultado>/candidato/<string:id_candidato>/mesa/<string:id_mesa>",methods=['PUT'])
def modificarResultado(id_resultado,id_candidato,id_mesa):
    dataConfig = loadFileConfig()
    datos = request.get_json()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/resultado/' + id_resultado + '/candidato/' + id_candidato + '/mesa/' + id_mesa
    response = requests.put(url, headers=headers, json=datos)
    json = response.json()
    return jsonify(json)

@app.route("/resultado/<string:id>",methods=['DELETE'])
def eliminarResultado(id):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/resultado/' + id
    response = requests.delete(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/resultado/consulta",methods=['GET'])
def getConsultaf():
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-registraduria"] + '/resultado/consulta'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)
########################################################################################################################

##################################################PATHS DE USUARIOS#####################################################

@app.route("/usuario/listar",methods = ["GET"])
def listarUsuarios():
    dataConfig = loadFileConfig()
    headers = {'content-type':'application/json; charset= utf8'}
    response = requests.get(dataConfig["url-ms-usuarios"]+"/usuario"+"/listar", headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/usuario/crear",methods = ["POST"])
def crearUsuarios():
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    datos = request.get_json()
    url = dataConfig["url-ms-usuarios"] + '/usuario/crear'
    response = requests.post(url, headers=headers, json=datos)
    json = response.json()
    return jsonify(json)

@app.route("/usuario/actualizar/<string:id_usuario>",methods = ["PUT"])
def actualizarUsuarios(id_usuario):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    datos = request.get_json()
    url = dataConfig["url-ms-usuarios"] + '/usuario/actualizar/' + id_usuario
    response = requests.put(url, headers=headers, json=datos)
    json = response.json()
    return jsonify(json)

@app.route("/usuario/<string:id_usuario>/rol/<string:id_rol>",methods = ["PUT"])
def asignarRol(id_usuario,id_rol):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-usuarios"] + '/usuario/' + id_usuario+ '/rol/' + id_rol
    response = requests.put(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/usuario/eliminar/<string:id_usuario>",methods = ["DELETE"])
def eliminarUsuario(id_usuario):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-usuarios"] + '/usuario/eliminar?idUsuario=' + id_usuario
    response = requests.delete(url, headers=headers)
    return jsonify({"mensaje":"Usuario con id " + id_usuario + " eliminado"})
########################################################################################################################

##################################################PATHS DE ROLES########################################################

@app.route("/rol/listar",methods = ["GET"])
def listarRoles():
    dataConfig = loadFileConfig()
    headers = {'content-type':'application/json; charset= utf8'}
    url = dataConfig["url-ms-usuarios"] + '/rol/listar'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/rol/crear",methods = ["POST"])
def crearRol():
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-usuarios"] + '/rol/crear'
    datos = request.get_json()
    response = requests.post(url, headers=headers, json=datos)
    json = response.json()
    return jsonify(json)

@app.route("/rol/actualizar/<string:id_rol>",methods = ["PUT"])
def actualizarRol(id_rol):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    datos = request.get_json()
    url = dataConfig["url-ms-usuarios"] + '/rol/actualizar/' + id_rol
    response = requests.put(url, headers=headers, json=datos)
    json = response.json()
    return jsonify(json)

@app.route("/rol/eliminar/<string:id_rol>",methods = ["DELETE"])
def eliminarRol(id_rol):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-usuarios"] + '/rol/eliminar?idRol=' + id_rol
    response = requests.delete(url, headers=headers)
    return jsonify({"mensaje": "Rol con id " + id_rol + " eliminado"})
########################################################################################################################

##################################################PATHS DE PERMISOS#####################################################

@app.route("/permisos/listar",methods = ["GET"])
def listarPermisos():
    dataConfig = loadFileConfig()
    headers = {'content-type':'application/json; charset= utf8'}
    url = dataConfig["url-ms-usuarios"] + '/permisos/listar'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/permisos/crear",methods = ["POST"])
def crearPermisos():
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-usuarios"] + '/permisos/crear'
    datos = request.get_json()
    response = requests.post(url, headers=headers, json=datos)
    json = response.json()
    return jsonify(json)

@app.route("/permisos/actualizar/<string:id_permiso>",methods = ["PUT"])
def actualizarPermiso(id_permiso):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    datos = request.get_json()
    url = dataConfig["url-ms-usuarios"] + '/permisos/actualizar/' + id_permiso
    response = requests.put(url, headers=headers, json=datos)
    json = response.json()
    return jsonify(json)

@app.route("/permisos/eliminar/<string:id_permiso>",methods = ["DELETE"])
def eliminarPermiso(id_permiso):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-usuarios"] + '/permisos/eliminar/' + id_permiso
    response = requests.delete(url, headers=headers)
    return jsonify({"mensaje": "Permiso con id " + id_permiso + " eliminado"})
########################################################################################################################

###################################################PATHS DE ASIGNAR#####################################################

@app.route("/asignar",methods = ["GET"])
def listarAsignaciones():
    dataConfig = loadFileConfig()
    headers = {'content-type':'application/json; charset= utf8'}
    url = dataConfig["url-ms-usuarios"] + '/asignar'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/asignar/rol/<string:id_rol>/permiso/<string:id_permiso>",methods = ["POST"])
def asignarPermisos(id_rol,id_permiso):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-usuarios"] + '/asignar/' + id_rol + '/' + id_permiso
    response = requests.post(url, headers=headers)
    json = response.json()
    return jsonify(json)

@app.route("/asignar/<string:id_asignar>/rol/<string:id_rol>/permiso/<string:id_permiso>",methods = ["PUT"])
def actualizarAsignacion(id_asignar,id_rol,id_permiso):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    datos = request.get_json()
    url = dataConfig["url-ms-usuarios"] + '/asignar/' + id_asignar + '/' + id_rol + '/' + id_permiso
    response = requests.put(url, headers=headers, json=datos)
    json = response.json()
    return jsonify(json)

@app.route("/asignar/eliminar/<string:id_asignar>",methods = ["DELETE"])
def eliminarAsignacion(id_asignar):
    dataConfig = loadFileConfig()
    headers = {'content-type': 'application/json; charset= utf8'}
    url = dataConfig["url-ms-usuarios"] + '/asignar/' + id_asignar
    response = requests.delete(url, headers=headers)
    return jsonify({"mensaje": "la asignacion con id " + id_asignar + " eliminado"})
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

