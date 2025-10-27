-- DEPARTAMENTO
use gestemp_ecotech; 
-- Crear tabla Departamentos
create table if not exists departamentos(
    id_departamento int primary key AUTO_INCREMENT,
    nombre varchar(200) not null,
    descripcion varchar(300),
    activo tinyint(1) not null default 1,
    id_gerente int,
    foreign key (id_gerente) references empleado(id_empleado)
);

-- Crear tabla Departamento Empleado
create table if not exists departamento_empleado(
    id_departamento_empleado int primary key AUTO_INCREMENT,
    id_departamento int,
    id_empleado int,
    foreign key (id_departamento) references departamentos(id_departamento),
    foreign key (id_empleado) references empleado(id_empleado)
);

-- Funcion crear Departamento
drop procedure if exists sp_departamento_crear;

delimiter $$
create procedure sp_departamento_crear(
    in d_nombre varchar(200),
    in d_descripcion varchar(300)
)
begin
    declare d_id int;

    select id_departamento into d_id from departamentos where nombre = d_nombre limit 1;

    if d_id is null then
        insert into departamentos(nombre, descripcion, activo)
        values (d_nombre, d_descripcion,1);
    else
        update departamentos
        set nombre = d_nombre,
            descripcion = d_descripcion,
            activo = 1,
            id_gerente = null
        where id_departamento = d_id;

    end if;
end$$
delimiter ;


-- Verificar si Departamento existe por nombre

drop procedure if exists sp_departamento_verificar_nombre;

delimiter $$
create procedure sp_departamento_verificar_nombre(
    in d_nombre varchar(200),
    out verificar int)
begin
    declare d_id int;

    select id_departamento into d_id from departamentos where nombre = d_nombre and activo = 1 limit 1;

    if d_id is not null then
        select  d.nombre,
                d.descripcion,
                d.activo,
                d.id_gerente
        from departamentos d
        where d.activo = 1 and d.id_departamento = d_id;
        set verificar = d_id;
    else
        set verificar = -1;
    end if;
end$$
delimiter ;

-- Obtener datos Departamentos por id

drop procedure if exists sp_departamento_obtener_id;

delimiter $$
create procedure sp_departamento_obtener_id(
    in d_id_dep int,
    out verificar int)
begin
    declare d_id int;

    select id_departamento into d_id from departamentos where id_departamento = d_id_dep and activo = 1 limit 1;

    if d_id is not null then
        select  nombre,
                descripcion,
                activo,
                id_gerente
        from departamentos
        where activo = 1 and id_departamento = d_id_dep;
        set verificar = d_id;
    else
        set verificar = -1;
    end if;
end$$
delimiter ;

-- Funcion Modificar Departamento

drop procedure if exists sp_departamento_modificar;

delimiter $$
create procedure sp_departamento_modificar(
    in d_nombre varchar(200),
    in d_descripcion varchar(300),
    in d_id_dep int
)
begin
        update departamentos
        set nombre = d_nombre,
            descripcion = d_descripcion,
            activo = 1
        where id_departamento = d_id_dep;
end$$
delimiter ;



-- Eliminar Departamento por nombre
drop procedure if exists sp_departamento_eliminar_nombre;

delimiter $$

create procedure sp_departamento_eliminar_nombre(
    in d_nombre varchar(200),
    out verificar int
)
begin
    declare d_id int;

    select id_departamento into d_id from departamentos where nombre = d_nombre and activo = 1 limit 1;

    if d_id is not null then
        update departamentos
        set activo = 0
        where activo = 1 and nombre = d_nombre;

        select nombre
        from departamentos
        where id_departamento = d_id;

        delete from departamento_empleado
        where id_departamento = d_id;

        set verificar = d_id;
    else
        set verificar = -1;
    end if;

end$$

delimiter ;


-- Listar Departamentos
drop procedure if exists sp_departamento_listar;

delimiter $$
create procedure sp_departamento_listar()

begin
    select  d.id_departamento,
            d.nombre,
            d.descripcion,
            d.id_gerente,
            u.nombre
    from departamentos d
    left join empleado e on d.id_gerente = e.id_empleado
    left join usuario u on e.id_usuario = u.id_usuario
    where d.activo = 1;

end$$
delimiter ;


-- Buscar Departamento
drop procedure if exists sp_departamento_buscar;

delimiter $$
create procedure sp_departamento_buscar(
    in d_nombre varchar(200),
    out verificar int)

begin
    declare d_id int;

    select id_departamento into d_id from departamentos where activo = 1 and nombre like concat(d_nombre,"%") limit 1;
    
    if d_id is not null then
        select  d.id_departamento,
            d.nombre,
            d.descripcion,
            d.id_gerente,
            u.nombre
        from departamentos d
        left join empleado e on d.id_gerente = e.id_empleado
        left join usuario u on e.id_usuario = u.id_usuario
        where d.activo = 1 and d.nombre like concat(d_nombre,"%");

        set verificar = d_id;
    else
        set verificar = -1;
    end if;

end$$
delimiter ;

-- Verificar si departamento tiene un gerente

drop procedure if exists sp_departamento_verificar_gerente;

delimiter $$
create procedure sp_departamento_verificar_gerente(
    in d_id int,
    out verificar int)
begin
    declare d_gerente int;

    select id_gerente into d_gerente from departamentos where id_departamento = d_id and activo = 1 limit 1;

    if d_gerente is null then
        set verificar = 1;
    else
        set verificar = -1;
    end if;

end$$
delimiter ;


-- Asignar Gerente a Departamento

drop procedure if exists sp_departamento_asignar_gerente;

delimiter $$
create procedure sp_departamento_asignar_gerente(
    in e_id int,
    in d_id int,
    out verificar int
)
begin
    update departamentos
    set id_gerente = e_id
    where id_departamento = d_id;

end$$
delimiter ;

-- Eliminar Gerente de Departamento

drop procedure if exists sp_departamento_eliminar_gerente;

delimiter $$
create procedure sp_departamento_eliminar_gerente(
    in d_id int,
    out verificar int
)
begin
    update departamentos
    set id_gerente = null
    where id_departamento = d_id;

end$$
delimiter ;

-- Verificar si Empleado ya está asignado a un Departamento
drop procedure if exists sp_departamento_verificar_empleado_asignado;

delimiter $$
create procedure sp_departamento_verificar_empleado_asignado(
    in d_id_empleado int,
    out verificar int
)
begin
    declare d_asignado int;

    select id_departamento_empleado into d_asignado from departamento_empleado where id_empleado = d_id_empleado;

    if d_asignado is not null then
        set verificar = 1;
    else
        set verificar = -1;
    end if;

end$$
delimiter ;

-- Asignar Empleados a Departamento

drop procedure if exists sp_departamento_asignar_empleado;

delimiter $$
create procedure sp_departamento_asignar_empleado(
    in d_id_departamento int,
    in d_id_empleado int,
    out verificar int
)
begin
    insert into departamento_empleado(id_departamento, id_empleado)
    values (d_id_departamento, d_id_empleado);

end$$   
delimiter ;

-- Eliminar Empleado de Departamento

drop procedure if exists sp_departamento_eliminar_empleado;

delimiter $$
create procedure sp_departamento_eliminar_empleado(
    in d_id_empleado int,
    out verificar int
)
begin
    declare verificar_iddep int;
    select id_empleado into verificar_iddep from departamento_empleado where id_empleado = d_id_empleado limit 1;

    if verificar_iddep is not null then
        delete from departamento_empleado
        where id_empleado = d_id_empleado;
        set verificar = verificar_iddep;
    else
        set verificar = -1;
    end if;
end$$
delimiter ;

-- Listar Empleados de un Departamento

drop procedure if exists sp_departamento_listar_empleados;

delimiter $$
create procedure sp_departamento_listar_empleados()
begin
    select de.id_departamento_empleado,
            d.id_departamento,
            d.nombre,
            e.id_empleado,
            u.nombre
    from departamento_empleado de
    inner join departamentos d on de.id_departamento = d.id_departamento
    inner join empleado e on de.id_empleado = e.id_empleado
    inner join usuario u on e.id_usuario = u.id_usuario
    where d.activo = 1 and u.activo = 1;

end$$
delimiter ;


