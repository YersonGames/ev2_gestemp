create database if not exists gestemp_ecotech;
use gestemp_ecotech; 

-- Crear tabla Usuario
create table if not exists usuario(
    id_usuario int primary key AUTO_INCREMENT,
    nombre varchar(200) not null,
    direccion varchar(100) not null,
    telefono varchar(20) not null,
    email varchar(100),
    run varchar(20) not null,
    contrasenahash varchar(255),
    permiso int not null,
    activo tinyint(1) not null default 1
);


-- Crear tabla Empleado
create table if not exists empleado(
    id_empleado int primary key AUTO_INCREMENT,
    id_usuario int,
    fecha_inicio date,
    salario decimal(12,2),
    foreign key(id_usuario) references usuario(id_usuario)
);

-- Funcion registrar Usuario/Empleado
drop procedure if exists sp_empleado_registrar;

delimiter $$
create procedure sp_empleado_registrar(
    in u_nombre varchar(200),
    in u_direccion varchar(100),
    in u_telefono varchar(20),
    in u_email varchar(100),
    in u_run varchar(20),
    in u_contrasenahash varchar(255),
    in u_permiso int,
    in u_fecha_inicio date,
    in u_salario decimal(12,2)
)
begin
    declare u_id int;
    declare u_tid int;

    select id_usuario into u_id from usuario where run = u_run limit 1;

    if u_id is null then
        insert into usuario(nombre, direccion, telefono, email,run,contrasenahash,permiso,activo)
        values (u_nombre, u_direccion, u_telefono,u_email,u_run,u_contrasenahash,u_permiso,1);

        set u_tid = LAST_INSERT_ID();
        insert into empleado(id_usuario,fecha_inicio,salario)
        values (u_tid,u_fecha_inicio,u_salario);
    else
        update usuario
        set nombre = u_nombre,
            direccion  = u_direccion,
            telefono = u_telefono,
            email = u_email,
            run = u_run,
            contrasenahash = u_contrasenahash,
            permiso = u_permiso,
            activo = 1
        where id_usuario = u_id;

        update empleado
        set fecha_inicio = u_fecha_inicio,
            salario = u_salario
        where id_usuario = u_id;
    end if;
end$$
delimiter ;

-- Listar empleados
drop procedure if exists sp_empleado_listar;

delimiter $$
create procedure sp_empleado_listar()

begin
    select  e.id_empleado,
            u.nombre,
            u.direccion,
            u.telefono,
            u.email,
            u.run,
            u.permiso,
            e.fecha_inicio,
            e.salario
    from empleado e
    inner join usuario u on e.id_usuario = u.id_usuario
    where u.activo = 1;

end$$
delimiter ;

-- Buscar empleado
drop procedure if exists sp_empleado_buscar;

delimiter $$
create procedure sp_empleado_buscar(
    in u_nombre varchar(200),
    out verificar int)

begin
    declare u_id int;

    select id_usuario into u_id from usuario where activo = 1 and nombre like concat("%",u_nombre,"%") limit 1;
    
    if u_id is not null then
        select  e.id_empleado,
                u.nombre,
                u.direccion,
                u.telefono,
                u.email,
                u.run,
                u.permiso,
                e.fecha_inicio,
                e.salario
        from empleado e
        inner join usuario u on e.id_usuario = u.id_usuario
        where u.activo = 1 and u.nombre like concat("%",u_nombre,"%");

        set verificar = u_id;
    else
        set verificar = -1;
    end if;


end$$
delimiter ;

-- Verificar si empleado existe por run, devolver id usuario

drop procedure if exists sp_empleado_verificar_run;

delimiter $$
create procedure sp_empleado_verificar_run(
    in u_run varchar(20),
    out verificar int)
begin
    declare u_id int;

    select id_usuario into u_id from usuario where run = u_run and activo = 1 limit 1;

    if u_id is not null then
        select  u.nombre,
                u.direccion,
                u.telefono,
                u.email,
                u.run,
                u.permiso,
                e.fecha_inicio,
                e.salario,
                u.contrasenahash
        from empleado e
        inner join usuario u on e.id_usuario = u.id_usuario
        where u.activo = 1 and u.run = u_run;
        set verificar = u_id;
    else
        set verificar = -1;
    end if;


end$$

delimiter ;

-- Verificar si empleado existe por run, devolver id empleado

drop procedure if exists sp_empleado_verificar_run_idempleado;

delimiter $$
create procedure sp_empleado_verificar_run_idempleado(
    in u_run varchar(20),
    out verificar int)
begin
    declare u_id int;
    declare e_id int;

    select id_usuario into u_id from usuario where run = u_run and activo = 1 limit 1;

    if u_id is not null then
        select id_empleado into e_id from empleado where id_usuario = u_id limit 1;
        set verificar = e_id;
    else
        set verificar = -1;
    end if;


end$$

delimiter ;

-- Eliminar Empleado por Run
drop procedure if exists sp_empleado_eliminar_run;

delimiter $$

create procedure sp_empleado_eliminar_run(
    in u_run varchar(20),
    out verificar int
)
begin
    declare u_id int;

    select id_usuario into u_id from usuario where run = u_run and activo = 1 limit 1;

    if u_id is not null then
        update usuario
        set activo = 0
        where activo = 1 and run = u_run;

        select nombre
        from usuario
        where id_usuario = u_id;

        set verificar = u_id;
    else
        set verificar = -1;
    end if;


end$$

delimiter ;

-- Funcion Modificar Usuario/Empleado
drop procedure if exists sp_empleado_modificar_run;

delimiter $$
create procedure sp_empleado_modificar_run(
    in u_nombre varchar(200),
    in u_direccion varchar(100),
    in u_telefono varchar(20),
    in u_email varchar(100),
    in u_run varchar(20),
    in u_contrasenahash varchar(255),
    in u_permiso int,
    in u_fecha_inicio date,
    in u_salario decimal(12,2)
)
begin
    declare u_id int;

    select id_usuario into u_id from usuario where run = u_run limit 1;

    
        update usuario
        set nombre = u_nombre,
            direccion  = u_direccion,
            telefono = u_telefono,
            email = u_email,
            run = u_run,
            contrasenahash = u_contrasenahash,
            permiso = u_permiso,
            activo = 1
        where id_usuario = u_id;

        update empleado
        set fecha_inicio = u_fecha_inicio,
            salario = u_salario
        where id_usuario = u_id;

end$$
delimiter ;


-- DEPARTAMENTO

-- Crear tabla Departamentos
create table if not exists departamentos(
    id_departamento int primary key AUTO_INCREMENT,
    nombre varchar(200) not null,
    descripcion varchar(300),
    activo tinyint(1) not null default 1,
    id_gerente int,
    foreign key (id_gerente) references empleado(id_empleado)
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

        delete from departamento_empleado
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
            d.id_gerente
    from departamentos d
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

    select id_departamento into d_id from departamentos where activo = 1 and nombre like concat("%",d_nombre,"%") limit 1;
    
    if d_id is not null then
        select  d.id_departamento,
                d.nombre,
                d.descripcion,
                d.id_gerente
        from departamentos d
        where d.activo = 1 and d.nombre like concat("%",d_nombre,"%");

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
    in u_id int,
    in d_id int,
    out verificar int
)
begin
    update departamentos
    set id_gerente = u_id
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

-- Crear tabla Departamento Empleado
create table if not exists departamento_empleado(
    id_departamento_empleado int primary key AUTO_INCREMENT,
    id_departamento int,
    id_empleado int,
    foreign key (id_departamento) references departamentos(id_departamento),
    foreign key (id_empleado) references empleado(id_empleado)
);

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
    delete from departamento_empleado
    where id_empleado = d_id_empleado;

    set verificar = 1;
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
    where d.activo = 1;

end$$
delimiter ;


-- PROYECTOS

-- Crear tabla Proyectos
create table if not exists proyectos(
    id_proyecto int primary key AUTO_INCREMENT,
    nombre varchar(200) not null,
    descripcion varchar(300),
    activo tinyint(1) not null default 1,
    fecha_inicio date
);

-- Funcion crear Proyecto
drop procedure if exists sp_proyecto_crear;

delimiter $$
create procedure sp_proyecto_crear(
    in p_nombre varchar(200),
    in p_descripcion varchar(300),
    in p_fecha_inicio date
)
begin
    declare p_id int;
    
    select id_proyecto into p_id from proyecto where nombre = p_nombre limit 1;

    if p_id is null then 
        insert into proyecto(nombre, descripcion, activo, fecha_inicio)
        values (p_nombre, p_descripcion, 1, p_fecha_inicio);
    else 
        update proyecto
        set descripcion = p_descripcion,
            fecha_inicio = p_fecha_inicio,
            activo = 1
        where id_proyecto = p_id;
    end if;

end$$
delimiter ;

-- Listar Proyecto
drop procedure if exists sp_proyecto_listar;

delimiter $$
create procedure sp_proyecto_listar()

begin
    select p.id_proyecto,
            p.nombre,
            p.descripcion,
            p.fecha_inicio
    from proyecto p
    where p.activo = 1;

end$$
delimiter ;

-- Buscar Proyecto
drop procedure if exists sp_proyecto_buscar;

delimiter $$
create procedure sp_proyecto_buscar(
    in p_nombre varchar(200),
    out verificar int)

begin 
    declare p_id int;

    select id_proyecto into p_id from proyecto where activo = 1 and nombre like concat("%",p_nombre,"%") limit 1;

    if p_id is not null then
        select  p.id_proyecto,
                p.nombre,
                p.descripcion,
                p,fecha_inicio  
        from proyecto p
        where p.activo = 1 and p.nombre like concat("%",p_nombre,"%");

        set verificar = p_id;
    else 
        set verificar = -1;
    end if;

end$$ 
delimiter ;

-- Eliminar Proyecto por nombre
drop procedure if exists sp_proyecto_eliminar_nombre;

delimiter $$

create procedure sp_proyecto_eliminar_nombre(
    in p_nombre varchar(200),
    out verificar int)

begin
    declare p_id int;

    select id_proyecto into p_id from proyecto where nombre = p_nombre and activo = 1 limit 1;

    if p_id is not null then 
        update proyecto
        set activo = 0
        where activo = 1 and nombre = p_nombre;

        select nombre
        from proyecto
        where id_proyecto = p_id; 

        set verificar = p_id;
    else 
        set verificar = -1;
    end if;

end$$

delimiter ;
