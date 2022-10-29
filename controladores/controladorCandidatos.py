from modelos.candidato import Candidato
from repositorios.repositorioCandidato import RepositorioCandidato

class ControladorCandidato():
    def __init__(self):
        self.repositorioCandidato = RepositorioCandidato()

    def listar_candidato(self):
        candidato = self.repositorioCandidato.findAll()
        return candidato

    def crear_candidato(self,datos):
        _candidato = Candidato(datos)
        return self.repositorioCandidato.save(_candidato)

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
    
    def asignar_partido(self,id, id_partido):
        candidatoActual = Candidato(self.repositorioCandidato.findById(id))
        partidoActual = Partido(self.repositorioPartidoPolitico.findById(id_partido))
        candidatoActual.partido = partidoActual
        return self.repositorioCandidato.save(candidatoActual)
    