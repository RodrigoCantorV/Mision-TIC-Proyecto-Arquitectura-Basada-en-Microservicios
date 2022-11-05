package com.gestionusuarios.usuarios.controladores;
import com.gestionusuarios.usuarios.modelos.Permiso;
import com.gestionusuarios.usuarios.repositorios.RepositorioPermiso;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.theme.CookieThemeResolver;

import java.awt.*;
import java.util.List;
@RestController
@RequestMapping("permisos")
public class ControladorPermiso {
    @Autowired
    private RepositorioPermiso repoPermiso;

    @GetMapping("/listar")
    public List<Permiso> listarPermisos(){
        return repoPermiso.findAll();
    }

    @PostMapping("/crear")
    public Permiso crearPermiso(@RequestBody Permiso permiso){
        return repoPermiso.save(permiso);
    }

    @PutMapping("/actualizar/{id}")
    public String actualizarPermiso(@PathVariable String id, @RequestBody Permiso permisoEntrada){
        Permiso permisoConsulta = repoPermiso.findById(id).orElse(null);
        permisoConsulta.setUrl(permisoEntrada.getUrl());
        permisoConsulta.setMetodo(permisoEntrada.getMetodo());
        repoPermiso.save(permisoConsulta);
        return "el permiso se ha actualizado";
    }

    @DeleteMapping("/eliminar/{id}")
    public String eliminarPermiso(@PathVariable String id){
        repoPermiso.deleteById(id);
        return "se ha eliminado el permiso";
    }
}
