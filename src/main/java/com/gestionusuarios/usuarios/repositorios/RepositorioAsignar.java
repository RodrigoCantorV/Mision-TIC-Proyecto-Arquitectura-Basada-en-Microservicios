package com.gestionusuarios.usuarios.repositorios;

import com.gestionusuarios.usuarios.modelos.Asignar;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

public interface RepositorioAsignar extends MongoRepository<Asignar,String> {

    @Query("{'rol.$id':ObjectId('?0'),'permiso.$id':ObjectId('?1')}") //Forma 1
    //@Query("{rol: DBRef('rol', ObjectId('?0')),permiso:DBRef('permiso', ObjectId('?1'))}")
    public Asignar obtenerRolPermiso(String idRol, String idPermiso);

}
