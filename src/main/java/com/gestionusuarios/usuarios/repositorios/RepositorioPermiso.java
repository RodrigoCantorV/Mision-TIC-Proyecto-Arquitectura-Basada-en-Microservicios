package com.gestionusuarios.usuarios.repositorios;

import com.gestionusuarios.usuarios.modelos.Permiso;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

public interface RepositorioPermiso extends MongoRepository<Permiso,String> {
    @Query("{'url':'?0','metodo':'?1'}")
    public Permiso obtenerPermiso(String url,String metodo);
}
