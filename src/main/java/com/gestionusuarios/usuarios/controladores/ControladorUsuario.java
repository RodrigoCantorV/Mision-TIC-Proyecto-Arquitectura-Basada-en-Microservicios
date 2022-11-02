package com.gestionusuarios.usuarios.controladores;

import com.gestionusuarios.usuarios.modelos.Usuario;
import com.gestionusuarios.usuarios.repositorios.RepositorioUsuario;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/usuario")
public class ControladorUsuario {

    @Autowired
    RepositorioUsuario miRepositorioUsuario;

    @GetMapping("/listar")
    public List<Usuario> consultarUsuarios(){
        return miRepositorioUsuario.findAll();
    }

    @PostMapping("/crear")
    public Usuario crearUsuario(@RequestBody Usuario usuario){
        return miRepositorioUsuario.save(usuario);
    }

    @PutMapping("/actualizar/{id}")
    public Usuario actualizarUsuario(@PathVariable String id,@RequestBody Usuario usuarioEntrada){
        Usuario usuarioConsulta = miRepositorioUsuario.findById(id).orElse(null);
        if(usuarioEntrada.getSeudonimo() != null){
            usuarioConsulta.setSeudonimo(usuarioEntrada.getSeudonimo());
        }
        if(usuarioEntrada.getCorreo() != null){
            usuarioConsulta.setCorreo(usuarioEntrada.getCorreo());
        }
       if(usuarioEntrada.getContrasena() !=  null){
           usuarioConsulta.setContrasena(usuarioEntrada.getContrasena());
       }
        return miRepositorioUsuario.save(usuarioConsulta);
    }

    @DeleteMapping("/eliminar")
    public String eliminarUsuario(@RequestParam(value = "idUsuario") String _idUsuario){
        miRepositorioUsuario.deleteById(_idUsuario);
        return "El usuario con id: " + _idUsuario + " fue eliminado correctamente";
    }
}
