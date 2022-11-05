package com.gestionusuarios.usuarios.repositorios;

import com.gestionusuarios.usuarios.modelos.Asignar;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface RepositorioAsignar extends MongoRepository<Asignar,String> {
}
