-- Destinos
use gestemp_ecotech; 

-- Crear tabla destinos

create table if not exists destinos(
    id_destino int primary key AUTO_INCREMENT,
    nombre_destino varchar(100),
    descripcion text,
    actividades text,
    costo decimal(10,2),
    activo tinyint not null default 1
);

-- Crear destino
drop procedure if exists sp_destinos_crear;

delimiter $$

create procedure sp_destinos_crear(
    in d_nombre varchar(100),
    in d_desc text,
    in d_act text,
    in d_costo decimal(10,2)
)
begin

    declare d_id int;

    select id_destino into d_id from destinos where nombre_destino = d_nombre limit 1;

    if d_id is null then
        insert into destinos(nombre_destino,descripcion,actividades,costo,activo)
        values(d_nombre,d_desc,d_act,d_costo,1);
    else
        update destinos
        set descripcion = d_desc,
            actividades = d_act,
            costo = d_costo,
            activo = 1
        where id_destino = d_id;
    end if;

end$$

delimiter ;

-- Obtener id por nombre
drop procedure if exists sp_destino_verificar_nombre;

delimiter $$
create procedure sp_destino_verificar_nombre(
    in d_nombre varchar(100),
    out verificar int
)
begin
    declare d_id int;
    select id_destino into d_id from destinos where nombre_destino = d_nombre and activo = 1 limit 1;

    if d_id is not null then
        set verificar = d_id;
    else
        set verificar = -1;
    end if;
end$$
delimiter ;

-- Obtener datos por id
drop procedure if exists sp_destino_get_id;

delimiter $$

create procedure sp_destino_get_id(
    in d_id int,
    out verificar int
)
begin

    select  nombre_destino,
            descripcion,
            actividades,
            costo
    from destinos
    where id_destino = d_id and activo = 1;

end$$

delimiter ;

-- Modificar datos por id
drop procedure if exists sp_destino_modificar;

delimiter $$

create procedure sp_destino_modificar(
    in d_nombre varchar(100),
    in d_desc text,
    in d_act text,
    in d_costo decimal(10,2),
    in d_id int
)
begin

    update destinos
    set nombre_destino = d_nombre,
        descripcion = d_desc,
        actividades = d_act,
        costo = d_costo
    where id_destino = d_id;

end$$

delimiter ;

-- Listar Destinos
drop procedure if exists sp_destino_listar;

delimiter $$

create procedure sp_destino_listar()
begin

    select  nombre_destino,
            descripcion,
            actividades,
            costo
    from destinos
    where activo = 1;

end$$

delimiter ;


-- Eliminar Destino por ID
drop procedure if exists sp_destino_eliminar;

delimiter $$

create procedure sp_destino_eliminar(
    in d_id int
)
begin 

update destinos
set activo = 0
where id_destino = d_id and activo = 1;

end$$

delimiter ;