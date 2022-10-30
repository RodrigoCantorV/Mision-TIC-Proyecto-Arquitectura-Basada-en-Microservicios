from modelos.candidato import Candidato
from modelos.mesa import Mesa
from modelos.resultado import Resultado
from repositorios.repositorioMesa import RepositorioMesa
from repositorios.repositorioCandidato import RepositorioCandidato
from repositorios.repositorioResultado import RepositorioResultado

class ControladorResultados():
    def __init__(self):
        self.repositorioResultado = RepositorioResultado()
        self.repositorioMesa = RepositorioMesa()
        self.repositorioCandidato = RepositorioCandidato()
        

    def listar_resultado(self):
        return self.repositorioResultado.findAll()

    """ 
    Asignar a cada resultado el candidato junto con la mesa
    """
    def crear_resultado(self,infoResultado,id_candidato,id_mesa):
        nuevoResultado = Resultado(infoResultado)
        elCandidato = Candidato(self.repositorioCandidato.findById(id_candidato))
        laMesa = Mesa(self.repositorioMesa.findById(id_mesa))
        nuevoResultado.candidato = elCandidato
        nuevoResultado.mesa = laMesa
        return self.repositorioResultado.save(nuevoResultado)

    def mostrar_resultado(self,id):
        elResultado = Resultado(self.repositorioResultado.findById(id))
        return elResultado.__dict__
    """
    Modificar de resultado (candidato mesa)
    """
    def actualizar_resultado(self,id,infoResultado,id_candidato,id_mesa):
        elResultado = Resultado(self.repositorioResultado.findById(id))
        elResultado = Resultado(infoResultado)
        elCandidato = Candidato(self.repositorioCandidato.findById(id_candidato))
        laMesa = Mesa(self.repositorioMesa.findById(id_mesa))
        elResultado.candidato = elCandidato
        elResultado.mesa = laMesa
        return self.repositorioResultado.save(elResultado)

    def eliminar_resultado(self,id):
        return self.repositorioResultado.delete(id)

    def getConsulta1(self):
        consulta = self.repositorioResultado.query({"total_votos":10})
        return consulta
    
    """
    Obtiene el numero maximo de votos que alcanzo a obtener un candidato
    """
    def getConsulta2(self):    
        consulta = self.repositorioResultado.queryAggregation(
            [{
            "$group": {
                    "_id": "$candidato",
                    "max": {
                        "$max": "$total_votos"
                    },
                    "doc": {
                        "$first": "$$ROOT"
                    }
                }
            }]
        )
        return consulta

    """
    maximo de votos obtenidos en cada mesa
    """ 
    def getConsulta3(self):    
        consulta = self.repositorioResultado.queryAggregation(
            [{
            "$group": {
                    "_id": "$mesa",
                    "max": {
                        "$max": "$total_votos"
                    },
                    "doc": {
                        "$first": "$$ROOT"
                    }
                }
            }]
        )
        return consulta

    """
    Cantidad total de votos por mesa (Participacion ciudadana)
    """
    def getConsulta4(self):    
        consulta = self.repositorioResultado.queryAggregation(
            [{
            "$group": {
                    "_id": "$mesa",
                    "max": {
                        "$sum": "$total_votos"
                    },
                    "doc": {
                        "$first": "$$ROOT"
                    }
                }
            }]
        )
        return consulta

    """
    suma de votos obtenidos por candidato    
    """
    def getConsulta5(self):    
        consulta = self.repositorioResultado.queryAggregation(
            [{
            "$group": {
                    "_id": "$candidato",
                    "max": {
                        "$sum": "$total_votos"
                    },
                    "doc": {
                        "$first": "$$ROOT"
                    }
                }
            }]
        )
        return consulta
        
        
    def getConsulta6(self):    
        query1 = {
          "$match": {"materia.$id":"635dc3655cd8060be4de8533"}
        }
        query2 = {
          "$group": {
            "_id": "$partido",
            "total_votos": {
                "$sum": "$total_votos"
            }
          }
        }
        pipeline = [query1,query2]
        consulta = self.repositorioResultado.queryAggregation(pipeline)
        return consulta
        