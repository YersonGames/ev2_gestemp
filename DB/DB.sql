create database if not exists gestemp_ecotech;
use gestemp_ecotech; 

-- Crear tabla Usuario
create table if not exists usuario(
    id_usuario int primary key AUTO_INCREMENT,
    nombre text,
    direccion text,
    telefono text,
    email text,
    run varchar(20),
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

    select id_usuario into u_id from usuario where activo = 1 and nombre like concat(u_nombre,"%") limit 1;
    
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
        where u.activo = 1 and u.nombre like concat(u_nombre,"%");

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

-- devolver datos por id empleados

drop procedure if exists sp_empleado_get_id;

delimiter $$
create procedure sp_empleado_get_id(
    in u_id varchar(20),
    out verificar int)
begin

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
        where u.activo = 1 and u.id_usuario = u_id;


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

-- Verificar si empleado existe por run, devolver id empleado empleado a gerente

drop procedure if exists sp_empleado_verificar_run_idempleado_gerente;

delimiter $$
create procedure sp_empleado_verificar_run_idempleado_gerente(
    in u_run varchar(20),
    out verificar int)
begin
    declare u_id int;
    declare e_id int;
    declare e_idg int;

    select id_usuario into u_id from usuario where run = u_run and activo = 1 limit 1;

    if u_id is not null then
        select id_empleado into e_id from empleado where id_usuario = u_id limit 1;
        select id_empleado into e_idg from departamento_empleado where id_empleado = e_id limit 1;
        set verificar = e_id;

        if e_idg is not null then
            set verificar = -2;
        end if;

    else
        set verificar = -1;
    end if;


end$$

delimiter ;

-- Verificar si empleado existe por run, devolver id empleado gerente a empleado

drop procedure if exists sp_empleado_verificar_run_idempleado_gerenteempleado;

delimiter $$
create procedure sp_empleado_verificar_run_idempleado_gerenteempleado(
    in u_run varchar(20),
    out verificar int)
begin
    declare u_id int;
    declare e_id int;
    declare e_idg int;

    select id_usuario into u_id from usuario where run = u_run and activo = 1 limit 1;

    if u_id is not null then
        select id_empleado into e_id from empleado where id_usuario = u_id limit 1;
        select id_gerente into e_idg from departamentos where id_gerente = e_id limit 1;
        set verificar = e_id;

        if e_idg is not null then
            set verificar = -2;
        end if;

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
    declare e_id int;

    select id_usuario into u_id from usuario where run = u_run and activo = 1 limit 1;

    if u_id is not null then
        select id_empleado into e_id from empleado where id_usuario = u_id limit 1;

        update usuario
        set activo = 0
        where activo = 1 and run = u_run;

        select nombre
        from usuario
        where id_usuario = u_id;

        delete from proyecto_empleado
        where id_empleado = e_id;

        delete from departamento_empleado
        where id_empleado = e_id;

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


-- Funcion Modificar Usuario/Empleado por id
drop procedure if exists sp_empleado_modificar_id;

delimiter $$
create procedure sp_empleado_modificar_id(
    in u_nombre varchar(200),
    in u_direccion varchar(100),
    in u_telefono varchar(20),
    in u_email varchar(100),
    in u_run varchar(20),
    in u_contrasenahash varchar(255),
    in u_permiso int,
    in u_fecha_inicio date,
    in u_salario decimal(12,2),
    in u_id int
)
begin

    
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