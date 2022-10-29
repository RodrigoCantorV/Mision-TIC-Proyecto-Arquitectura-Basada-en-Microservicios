from repositorios.repositorioPartido import RepositorioPartido
from modelos.partido import Partido

class ControladorPartidoPolitico():
    def __init__(self):
        self.repositorioPartido = RepositorioPartido()
        
    def listar_partido(self):
        partido = self.repositorioPartido.findAll()
        return partido
    
    def crear_partido(self,datos):
        _partido = Partido(datos)
        return self.repositorioPartido.save(_partido)
    
    def mostrar_partido(self,id):
        partido = self.repositorioPartido.findById(id)
        return partido
    
    def eliminar_partido(self,id):
        respuesta = self.repositorioPartido.delete(id)
        print("partido "+id+" eliminado")
        return respuesta
    
    def actualizar_partido(self,id,datos):
        consulta = self.repositorioPartido.findById(id)
        _partido = Partido(consulta)
        _partido.nombre = datos["nombre"]
        _partido.lema = datos["lema"]
        print("Actualizando partido con id ",id)
        return self.repositorioPartido.save(_partido)
    