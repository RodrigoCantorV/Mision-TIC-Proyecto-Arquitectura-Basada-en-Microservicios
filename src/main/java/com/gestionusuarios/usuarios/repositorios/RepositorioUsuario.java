package com.gestionusuarios.usuarios.repositorios;

import com.gestionusuarios.usuarios.modelos.Usuario;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

public interface RepositorioUsuario extends MongoRepository<Usuario,String> {

    @Query("{'correo':'?0'}") //Consulta preparada
    public Usuario buscaPorCooreo(String correo);
}
