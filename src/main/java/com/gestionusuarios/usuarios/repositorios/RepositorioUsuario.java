package com.gestionusuarios.usuarios.repositorios;

import com.gestionusuarios.usuarios.modelos.Usuario;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface RepositorioUsuario extends MongoRepository<Usuario,String> {
}
