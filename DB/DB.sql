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

-- Crear Tabla Horas Empleado
create table if not exists empleado_registro(
    id_empleado_hora int primary key AUTO_INCREMENT,
    id_empleado int,
    horas float,
    fecha_registro date,
    foreign key(id_empleado) references empleado(id_empleado)
);

-- Admin
delete from usuario where id_usuario = 1;
insert into usuario(id_usuario,nombre,direccion,telefono,email,run,contrasenahash,permiso,activo)
values (1,"QWRtaW4=","","","","MjIuMTk4LjgyMy0w","5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",3,1);

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
    declare u_adid int;

    select id_usuario into u_id from usuario where run = u_run limit 1;
    select id_usuario into u_adid from usuario where run = u_run and permiso = 3 limit 1;

    if u_id is null then
        if u_adid is null then
            insert into usuario(nombre, direccion, telefono, email,run,contrasenahash,permiso,activo)
            values (u_nombre, u_direccion, u_telefono,u_email,u_run,u_contrasenahash,u_permiso,1);

            set u_tid = LAST_INSERT_ID();
            insert into empleado(id_usuario,fecha_inicio,salario)
            values (u_tid,u_fecha_inicio,u_salario);
        end if;
    else
        if u_adid is null then
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
    where u.activo = 1
    order by e.id_empleado asc;

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
    declare e_id int;

    select id_usuario into u_id from usuario where run = u_run and activo = 1 and permiso != 3 limit 1;

    if u_id is not null then
    select id_empleado into e_id from empleado where id_usuario = u_id limit 1;

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
        set verificar = e_id;
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

    select id_usuario into u_id from usuario where run = u_run and activo = 1 and permiso != 3 limit 1;

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

    select id_usuario into u_id from usuario where run = u_run and activo = 1 and permiso != 3 limit 1;

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

        delete from empleado_registro
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

-- Verificar e inciar sesion usuario
drop procedure if exists sp_usuario_login;

delimiter $$

create procedure sp_usuario_login(
    in u_run text,
    in u_contrasenahash text,
    out verificar_id int,
    out verificar_permiso int,
    out verificar_nombre text
)
begin

    declare u_id int;
    declare u_per int;
    declare u_nom text;

    select id_usuario into u_id from usuario where run = u_run limit 1;
    select permiso into u_per from usuario where contrasenahash = u_contrasenahash limit 1;
    select nombre into u_nom from usuario where run = u_run limit 1;


    if u_id is not null then

        if u_per is not null then

            set verificar_id = u_id;
            set verificar_permiso = u_per;
            set verificar_nombre = u_nom;
        else
            set verificar_id = -1;
            set verificar_permiso = -1;
            set verificar_nombre = "Error";
        end if;

    else
            set verificar_id = -1;
            set verificar_permiso = -1;
            set verificar_nombre = "Error";

    end if;

end$$

delimiter ;

-- Funcion Registrar horas empleados
drop procedure if exists sp_empleado_registrar_horas;

delimiter $$

create procedure sp_empleado_registrar_horas(
    in u_id int,
    in e_horas float,
    in eh_fecha date,
    out verificar int
)
begin

    declare e_id int;
    declare eh_id int;

    select id_empleado into e_id from empleado where id_usuario = u_id limit 1;
    select id_empleado into eh_id from empleado_registro where id_empleado = e_id and year(fecha_registro) = year(eh_fecha) and month(fecha_registro) = month(eh_fecha) limit 1;

    if eh_id is null then
        insert empleado_registro(id_empleado,horas,fecha_registro)
        values (e_id,e_horas,eh_fecha);
        set verificar = eh_id;
    else
        update empleado_registro
        set horas = horas+e_horas
        where id_empleado = e_id;
        set verificar = e_id;
    end if;


end $$

delimiter ;

-- Devolver Registro de horas por anio-mes
drop procedure if exists sp_empleado_obtener_registro;

delimiter $$

create procedure sp_empleado_obtener_registro(
    in u_id int,
    in eh_fecha date,
    out verificar int
)
begin

    declare eh_id int;
    declare e_id int;
    
    select id_empleado into e_id from empleado where id_usuario = u_id limit 1;
    select id_empleado_hora into eh_id from empleado_registro where id_empleado = e_id and year(fecha_registro) = year(eh_fecha) and month(fecha_registro) = month(eh_fecha) limit 1;

    if eh_id is not null then
        select horas
        from empleado_registro
        where id_empleado_hora = eh_id;
        set verificar = eh_id;
    else
        set verificar = -1;
    end if;

end$$

delimiter ;


-- Listar datos Registro, empleados
drop procedure if exists sp_empleado_listar_registro;

delimiter $$

create procedure sp_empleado_listar_registro()
begin

    select  e.id_empleado,
            u.nombre,
            er.horas,
            er.fecha_registro
    from empleado e
    left join usuario u on e.id_usuario = u.id_usuario
    left join empleado_registro er on e.id_empleado = er.id_empleado
    order by e.id_empleado asc;

end$$

delimiter ;

