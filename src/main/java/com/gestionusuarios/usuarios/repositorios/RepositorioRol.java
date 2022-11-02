package com.gestionusuarios.usuarios.repositorios;

import com.gestionusuarios.usuarios.modelos.Rol;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface RepositorioRol extends MongoRepository<Rol,String> {
}
