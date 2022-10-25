from repositorios.repositorioMesa import RepositorioMesa
from modelos.mesa import Mesa

class ControladorMesa():
    def __init__(self):
        self.repositorioMesa = RepositorioMesa()
    
    def index(self):
        return self.repositorioMesa.findAll()
    
    def create(self,infoMesa):
        nuevaMesa = Mesa(infoMesa)
        return self.repositorioMesa.save(nuevaMesa)

    def show(self,id):
        laMesa = Mesa(self.repositorioMesa.findById(id))
        return laMesa.__dict__

    def update(self,id,infoMesa):
        mesaActual = Mesa(self.repositorioMesa.findById(id))
        mesaActual = Mesa(infoMesa)
        return self.repositorioMesa.save(mesaActual)

    def delete(self,id):
        return self.repositorioMesa.delete(id)