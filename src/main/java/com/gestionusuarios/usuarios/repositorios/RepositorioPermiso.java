package com.gestionusuarios.usuarios.repositorios;

import com.gestionusuarios.usuarios.modelos.Permiso;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface RepositorioPermiso extends MongoRepository<Permiso,String> {
}
