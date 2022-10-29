from modelos.candidato import Candidato
from modelos.partido import Partido
from repositorios.repositorioCandidato import RepositorioCandidato
from repositorios.repositorioPartido import RepositorioPartido

class ControladorCandidato():
    def __init__(self):
        self.repositorioCandidato = RepositorioCandidato()
        self.repositorioPartido = RepositorioPartido()

    def listar_candidato(self):
        candidato = self.repositorioCandidato.findAll()
        return candidato

    def crear_candidato(self,datos):
        _candidato = Candidato(datos)
        return self.repositorioCandidato.save(_candidato)
    
    def mostrar_candidato(self,id):
        candidato = self.repositorioCandidato.findById(id)
        return candidato

    def eliminar_candidato(self,id):
        respuesta = self.repositorioCandidato.delete(id) 
        print("Candidato "+id+" eliminado")
        return respuesta

    def actualizar_candidato(self,id,datos):
        consulta = self.repositorioCandidato.findById(id)
        _candidato = Candidato(consulta)
        _candidato.cedula = datos["cedula"]
        _candidato.nombre= datos["nombre"]
        _candidato.apellido= datos["apellido"]
        print("Actualizando candidato con id ",id)
        return self.repositorioCandidato.save(_candidato)
    
    def asignar_partido(self,id_candidato, id_partido):
        candidatoActual = Candidato(self.repositorioCandidato.findById(id_candidato))
        partidoActual = Partido(self.repositorioPartido.findById(id_partido))
        candidatoActual.partido = partidoActual
        return self.repositorioCandidato.save(candidatoActual)
    