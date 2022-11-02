package com.gestionusuarios.usuarios.controladores;

import com.gestionusuarios.usuarios.modelos.Rol;
import com.gestionusuarios.usuarios.modelos.Usuario;
import com.gestionusuarios.usuarios.repositorios.RepositorioRol;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/rol")
public class ControladorRol {

    @Autowired
    RepositorioRol miRepositorioRol;

    @GetMapping("/listar")
    public List<Rol> consultarRol(){
        return miRepositorioRol.findAll();
    }

    @PostMapping("/crear")
    public Rol crearRol(@RequestBody Rol rol){
        return miRepositorioRol.save(rol);
    }

    @PutMapping("/actualizar/{id}")
    public Rol actualizarRol(@PathVariable String id,@RequestBody Rol rolEntrada){
        Rol rolConsulta = miRepositorioRol.findById(id).orElse(null);
        if(rolEntrada.getNombre() != null){
            rolConsulta.setNombre(rolEntrada.getNombre());
        }
        if(rolEntrada.getDescripcion() != null){
            rolConsulta.setDescripcion(rolEntrada.getDescripcion());
        }
        return miRepositorioRol.save(rolConsulta);
    }

    @DeleteMapping("/eliminar")
    public String eliminarRol(@RequestParam(value = "idRol") String _idRol){
        miRepositorioRol.deleteById(_idRol);
        return "El Rol con id: " + _idRol + " fue eliminado correctamente";
    }
}
