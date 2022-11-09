package com.gestionusuarios.usuarios.controladores;

import com.gestionusuarios.usuarios.modelos.Rol;
import com.gestionusuarios.usuarios.modelos.Usuario;
import com.gestionusuarios.usuarios.repositorios.RepositorioRol;
import com.gestionusuarios.usuarios.repositorios.RepositorioUsuario;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.List;

@RestController
@RequestMapping("/usuario")
public class ControladorUsuario {

    @Autowired
    RepositorioUsuario miRepositorioUsuario;
    @Autowired
    RepositorioRol miRepositorioRol;

    @GetMapping("/listar")
    public List<Usuario> consultarUsuarios(){
        return miRepositorioUsuario.findAll();
    }

    @PostMapping("/crear")
    public Usuario crearUsuario(@RequestBody Usuario usuario){
        usuario.setContrasena(convertirSHA256(usuario.getContrasena()));
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

    @PutMapping("/{idUsuario}/rol/{idRol}")
    public Usuario asignarRol(@PathVariable String idUsuario,@PathVariable String idRol){
    Usuario consultaUsuario = miRepositorioUsuario.findById(idUsuario).orElse(null);
    Rol consultaRol = miRepositorioRol.findById(idRol).orElse(null);
    consultaUsuario.setRol(consultaRol);
    return miRepositorioUsuario.save(consultaUsuario);

    }

    @PostMapping("/login")
    public Usuario inicioSesion(@RequestBody Usuario usuarioEntrada){
            Usuario usuarioConsulta = miRepositorioUsuario.buscaPorCooreo(usuarioEntrada.getCorreo());
            if(usuarioConsulta != null && usuarioConsulta.getContrasena().equals(convertirSHA256(usuarioEntrada.getContrasena()))){
                usuarioConsulta.setContrasena("");
                return usuarioConsulta;
            }else{
                return null;
            }
    }

    public String convertirSHA256(String password){
        MessageDigest md  = null;
        try{
            md = MessageDigest.getInstance("SHA-256");
        }catch (NoSuchAlgorithmException e){
            e.printStackTrace();
            return null;
        }
        byte[] hash = md.digest(password.getBytes());
        StringBuffer sb = new StringBuffer();
        for(byte b: hash){
            sb.append(String.format("%02x",b));
        }
        return  sb.toString();
    }
}
