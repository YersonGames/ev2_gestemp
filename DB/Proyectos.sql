-- PROYECTOS
use gestemp_ecotech; 
-- Crear tabla Proyectos
create table if not exists proyectos(
    id_proyecto int primary key AUTO_INCREMENT,
    nombre varchar(200) not null,
    descripcion varchar(300),
    activo tinyint(1) not null default 1,
    fecha_inicio date
);

-- Crear tabla ProyectoEmpleado
create table if not exists proyecto_empleado(
    id_proyecto_empleado int primary key AUTO_INCREMENT,
    id_proyecto int,
    id_empleado int,
    foreign key (id_proyecto) references proyectos(id_proyecto),
    foreign key (id_empleado) references empleado(id_empleado)
);

-- Funcion crear Proyecto
drop procedure if exists sp_proyectos_crear;

delimiter $$
create procedure sp_proyectos_crear(
    in p_nombre varchar(200),
    in p_descripcion varchar(300),
    in p_fecha_inicio date
)
begin
    declare p_id int;
    
    select id_proyecto into p_id from proyectos where nombre = p_nombre limit 1;

    if p_id is null then 
        insert into proyectos(nombre, descripcion, activo, fecha_inicio)
        values (p_nombre, p_descripcion, 1, p_fecha_inicio);
    else 
        update proyectos
        set descripcion = p_descripcion,
            fecha_inicio = p_fecha_inicio,
            activo = 1
        where id_proyecto = p_id;
    end if;

end$$
delimiter ;

-- Listar Proyecto
drop procedure if exists sp_proyectos_listar;

delimiter $$
create procedure sp_proyectos_listar()

begin
    select p.id_proyecto,
            p.nombre,
            p.descripcion,
            p.fecha_inicio
    from proyectos p
    where p.activo = 1
    order by p.id_proyecto asc;

end$$
delimiter ;

-- Buscar Proyectos
drop procedure if exists sp_proyectos_buscar;

delimiter $$
create procedure sp_proyectos_buscar(
    in p_nombre varchar(200),
    out verificar int)

begin 
    declare p_id int;

    select id_proyecto into p_id from proyectos where activo = 1 and nombre like concat(p_nombre,"%") limit 1;

    if p_id is not null then
        select  p.id_proyecto,
                p.nombre,
                p.descripcion,
                p.fecha_inicio  
        from proyectos p
        where p.activo = 1 and p.nombre like concat(p_nombre,"%");

        set verificar = p_id;
    else 
        set verificar = -1;
    end if;

end$$ 
delimiter ;

-- Eliminar Proyecto por nombre
drop procedure if exists sp_proyectos_eliminar_nombre;

delimiter $$

create procedure sp_proyectos_eliminar_nombre(
    in p_nombre varchar(200),
    out verificar int)

begin
    declare p_id int;

    select id_proyecto into p_id from proyectos where nombre = p_nombre and activo = 1 limit 1;

    if p_id is not null then 
        update proyectos
        set activo = 0
        where activo = 1 and nombre = p_nombre;

        select nombre
        from proyectos
        where id_proyecto = p_id; 

        delete from proyecto_empleado
        where id_proyecto = d_id;

        set verificar = p_id;
    else 
        set verificar = -1;
    end if;

end$$

delimiter ;


-- Verificar proyecto por nombre
drop procedure if exists sp_proyecto_verificar_nombre;

delimiter $$

create procedure sp_proyecto_verificar_nombre(
    in p_nombre varchar(100),
    out verificar int
)
begin
    declare p_id int;

    select id_proyecto into p_id from proyectos where nombre = p_nombre limit 1;

    if p_id is not null then
    set verificar = p_id;
    else
    set verificar = -1;
    end if;
end$$

delimiter ;

-- Obtener proyecto por id
drop procedure if exists sp_proyecto_obtener_id;

delimiter $$

create procedure sp_proyecto_obtener_id(
    in p_id int,
    out verificar int
)
begin

    select  nombre,
            descripcion,
            fecha_inicio
    from proyectos
    where id_proyecto = p_id;
end$$

delimiter ;

-- Funcion Modificar Proyecto

drop procedure if exists sp_proyecto_modificar;

delimiter $$
create procedure sp_proyecto_modificar(
    in d_nombre varchar(200),
    in d_descripcion varchar(300),
    in d_id_pro int
)
begin
        update proyectos
        set nombre = d_nombre,
            descripcion = d_descripcion,
            activo = 1
        where id_proyecto = d_id_pro;
end$$
delimiter ;

-- Asginar Empleado a Proyecto

drop procedure if exists sp_proyecto_asignar_empleado;

delimiter $$

create procedure sp_proyecto_asignar_empleado(
    in empleado_id int,
    in proyecto_id int,
    out verificar int
)
begin
    declare verificar_idpro int;
    select id_proyecto into verificar_idpro from proyecto_empleado where id_proyecto = proyecto_id and id_empleado = empleado_id limit 1;

    if verificar_idpro is null then
        insert proyecto_empleado(id_proyecto,id_empleado)
        values (proyecto_id,empleado_id);
        set verificar = LAST_INSERT_ID();
    else
        set verificar = -1;
    end if;
end$$

delimiter ;

-- Eliminar Empleado de Proyecto

drop procedure if exists sp_proyecto_eliminar_empleado;

delimiter $$

create procedure sp_proyecto_eliminar_empleado(
    in empleado_id int,
    in proyecto_id int,
    out verificar int
)
begin
    declare verificar_idpro int;
    select id_proyecto into verificar_idpro from proyecto_empleado where id_proyecto = proyecto_id and id_empleado = empleado_id limit 1;

    if verificar_idpro is not null then
        delete from proyecto_empleado
        where id_proyecto = proyecto_id and id_empleado = empleado_id;
        set verificar = verificar_idpro;
    else
        set verificar = -1;
    end if;
end$$

delimiter ;

-- Listar Empleados de un proyecto

drop procedure if exists sp_proyecto_listar_empleados;

delimiter $$
create procedure sp_proyecto_listar_empleados()
begin
    
    select  e.id_empleado,
            u.nombre,
            p.id_proyecto,
            p.nombre
    from proyecto_empleado pro
    inner join proyectos p on pro.id_proyecto = p.id_proyecto
    inner join empleado e on pro.id_empleado = e.id_empleado
    inner join usuario u on e.id_usuario = u.id_usuario
    where p.activo = 1 and u.activo = 1;


end$$
delimiter ;
