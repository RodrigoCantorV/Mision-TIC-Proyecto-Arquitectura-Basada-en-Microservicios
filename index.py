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
from controladores.controladorMesas import ControladorMesa
miControladorMesa = ControladorMesa()
from controladores.controladorPartidoPolitico import ControladorPartidoPolitico
miControladorPartido = ControladorPartidoPolitico()
from controladores.controladorCandidatos import ControladorCandidato 
miControladorCandidato = ControladorCandidato()
from controladores.controladorResultados import ControladorResultados
miControladorResultado = ControladorResultados()
###################################################################################
@app.route("/",methods=['GET'])
def test():
    json = {}
    json["message"]="Server running ..."
    return jsonify(json)
###################################################################################
#PATHS DE PARTIDOS POLITICOS
@app.route("/partidos",methods=['GET'])
def getPartido():
    json = miControladorPartido.listar_partido()
    return jsonify(json)

@app.route("/partidos",methods=['POST'])
def crearPartido():
    datos = request.get_json()
    json = miControladorPartido.crear_partido(datos)
    return jsonify(json)

@app.route("/partidos/<string:id>",methods=['GET'])
def listarPartido(id):
    json=miControladorPartido.mostrar_partido(id)
    return jsonify(json)

@app.route("/partidos/<string:id>",methods=['PUT'])
def modificarPartido(id):
    datos = request.get_json()
    json=miControladorPartido.actualizar_partido(id, datos)
    return jsonify(json)

@app.route("/partidos/<string:id>",methods=['DELETE'])
def eliminarPartido(id):
    json=miControladorPartido.eliminar_partido(id)
    return jsonify(json)

###################################################################################
#PATHS DE CANDIDATOS
@app.route("/candidatos",methods=['GET'])
def getCandidato():
    json = miControladorCandidato.listar_candidato()
    return jsonify(json)

@app.route("/candidatos",methods=['POST'])
def crearCandidato():
    datos = request.get_json()
    json = miControladorCandidato.crear_candidato(datos)
    return jsonify(json)

@app.route("/candidatos/<string:id>",methods=['GET'])
def listarCandidato(id):
    json=miControladorCandidato.mostrar_candidato(id)
    return jsonify(json)

@app.route("/candidatos/<string:id>",methods=['PUT'])
def modificarCandidato(id):
    datos = request.get_json()
    json=miControladorCandidato.actualizar_candidato(id, datos)
    return jsonify(json)

@app.route("/candidatos/<string:id>",methods=['DELETE'])
def eliminarCandidato(id):
    json=miControladorCandidato.eliminar_candidato(id)
    return jsonify(json)

@app.route("/candidatos/<string:id_candidato>/partido/<string:id_partido>",methods=['PUT'])
def asignarPartido(id_candidato,id_partido):
    json=miControladorCandidato.asignar_partido(id_candidato, id_partido)
    return jsonify(json)

###################################################################################
#PATHS DE MESAS
@app.route("/mesas",methods=['GET'])
def getMesas():
    json = miControladorMesa.index()
    return jsonify(json)

@app.route("/mesas",methods=['POST'])
def crearMesa():
    data = request.get_json()
    json = miControladorMesa.create(data)
    return jsonify(json)

@app.route("/mesas/<string:id>",methods=['GET'])
def getMesa(id):
    json=miControladorMesa.show(id)
    return jsonify(json)

@app.route("/mesas/<string:id>",methods=['PUT'])
def modificarMesa(id):
    data = request.get_json()
    json=miControladorMesa.update(id,data)
    return jsonify(json)

@app.route("/mesas/<string:id>",methods=['DELETE'])
def eliminarMesa(id):
    json=miControladorMesa.delete(id)
    return jsonify(json)
###################################################################################
#PATHS DE RESULTADOS
@app.route("/resultados",methods=['GET'])
def getResultados():
    json = miControladorResultado.listar_resultado()
    return jsonify(json)

@app.route("/resultado/candidato/<string:id_candidato>/mesa/<string:id_mesa>",methods=['POST'])
def crearResultado(id_candidato,id_mesa):
    data = request.get_json()
    json = miControladorResultado.crear_resultado(data,id_candidato,id_mesa)
    return jsonify(json)

@app.route("/resultado/<string:id>",methods=['GET'])
def getResultado(id):
    json=miControladorResultado.mostrar_resultado(id)
    return jsonify(json)

@app.route("/resultado/<string:id_resultado>/candidato/<string:id_candidato>/mesa/<string:id_mesa>",methods=['PUT'])
def modificarResultado(id_resultado,id_candidato,id_mesa):
    data = request.get_json()
    json=miControladorResultado.actualizar_resultado(id_resultado,data,id_candidato,id_mesa)
    return jsonify(json)

@app.route("/resultado/<string:id>",methods=['DELETE'])
def eliminarResultado(id):
    json=miControladorResultado.eliminar_resultado(id)
    return jsonify(json)

@app.route("/resultado/consulta",methods=['GET'])
def getConsultaf():
    json=miControladorResultado.getConsulta5()
    return jsonify(json)

###################################################################################
def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" + str(dataConfig["port"]))
    serve(app,host=dataConfig["url-backend"],port=dataConfig["port"])

###################################################################################
