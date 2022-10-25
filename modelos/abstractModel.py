from abc import ABCMeta

class AbstractModel(metaclass = ABCMeta):
    def __init__(self,datos):
        for llave,valor in datos.items():
            setattr(self,llave,valor)
            print("Se ha creado un objeto con: ", llave, " ", valor)

