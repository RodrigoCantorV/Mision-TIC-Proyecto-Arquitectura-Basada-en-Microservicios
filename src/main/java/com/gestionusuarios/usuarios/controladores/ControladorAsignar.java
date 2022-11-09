package com.gestionusuarios.usuarios.controladores;

import com.gestionusuarios.usuarios.modelos.Asignar;
import com.gestionusuarios.usuarios.modelos.Permiso;
import com.gestionusuarios.usuarios.modelos.Rol;
import com.gestionusuarios.usuarios.repositorios.RepositorioAsignar;
import com.gestionusuarios.usuarios.repositorios.RepositorioPermiso;
import com.gestionusuarios.usuarios.repositorios.RepositorioRol;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/asignar")
public class ControladorAsignar {

    @Autowired
    RepositorioAsignar miRepoAsignar;
    @Autowired
    RepositorioRol miRepoRol;
    @Autowired
    RepositorioPermiso miRepoPermiso;

    @GetMapping("")
    public List<Asignar> listarAsignacion(){
        return miRepoAsignar.findAll();
    }

    @PostMapping("/{idRol}/{idPermiso}")
    public Asignar crearAsignación(@PathVariable String idRol, @PathVariable String idPermiso){
        Rol rolConsulta = miRepoRol.findById(idRol).orElse(null);
        Permiso permisoConsulta = miRepoPermiso.findById(idPermiso).orElse(null);
        return miRepoAsignar.save(new Asignar(rolConsulta,permisoConsulta));
    }

    @PutMapping("{idAsignar}/{idRol}/{idPermiso}")
    public String actualizarAsignacion(@PathVariable String idAsignar,
                                     @PathVariable String idRol,
                                     @PathVariable String idPermiso){
        Asignar asignarConsulta = miRepoAsignar.findById(idAsignar).orElse(null);
        Rol rolConsulta = miRepoRol.findById(idRol).orElse(null);
        Permiso permisoConsulta = miRepoPermiso.findById(idPermiso).orElse(null);
        asignarConsulta.setPermiso(permisoConsulta);
        asignarConsulta.setRol(rolConsulta);
        miRepoAsignar.save(asignarConsulta);
        return "Se han actualizado los permisos de la app";
    }

    @DeleteMapping("/{idAsignar}")
    public String eliminarAsignacion(@PathVariable String idAsignar){
        miRepoAsignar.deleteById(idAsignar);
        return "Se han eliminado los permisos asignados";
    }
}
