-- Paquetes
use gestemp_ecotech; 

-- Crear tabla paquetes

create table if not exists paquetes(
    id_paquete int primary key AUTO_INCREMENT,
    nombre_paquete varchar(100),
    fecha_inicio date,
    fecha_fin date,
    disponibilidad int,
    precio_total decimal(10,2),
    activo tinyint not null default 1
);

-- Crear tabla paquete_destino

create table if not exists paquete_destino(
    id_paquete_destino int primary key AUTO_INCREMENT,
    id_paquete int,
    id_destino int,
    foreign key(id_paquete) references paquetes(id_paquete),
    foreign key(id_destino) references destinos(id_destino)
);

-- Crear paquete
drop procedure if exists sp_paquetes_crear;

delimiter $$

create procedure sp_paquetes_crear(
    in p_nombre varchar(100),
    in p_fechai date,
    in p_fechaf date,
    in p_disp int
)
begin

    declare p_id int;

    select id_paquete into p_id from paquetes where nombre_paquete = p_nombre limit 1;

    if p_id is null then
        insert into paquetes(nombre_paquete,fecha_inicio,fecha_fin,disponibilidad,precio_total,activo)
        values(p_nombre,p_fechai,p_fechaf,p_disp,0,1);
    else
        update paquetes
        set fecha_inicio = p_fechai,
            fecha_fin = p_fechaf,
            disponibilidad = p_disp,
            precio_total = 0,
            activo = 1
        where id_paquete = p_id;
    end if;

end$$

delimiter ;

-- Listar Destinos
drop procedure if exists sp_paquete_listar;

delimiter $$

create procedure sp_paquete_listar()
begin

    select  nombre_paquete,
            fecha_inicio,
            fecha_fin,
            disponibilidad,
            precio_total
    from paquetes
    where activo = 1;

end$$

delimiter ;

-- Obtener id por nombre
drop procedure if exists sp_paquete_verificar_nombre;

delimiter $$
create procedure sp_paquete_verificar_nombre(
    in p_nombre varchar(100),
    out verificar int
)
begin
    declare p_id int;
    select id_paquete into p_id from paquetes where nombre_paquete = p_nombre and activo = 1 limit 1;

    if p_id is not null then
        set verificar = p_id;
    else
        set verificar = -1;
    end if;
end$$
delimiter ;

-- Obtener datos por id
drop procedure if exists sp_paquete_get_id;

delimiter $$

create procedure sp_paquete_get_id(
    in p_id int,
    out verificar int
)
begin

    select  nombre_paquete,
            fecha_inicio,
            fecha_fin,
            disponibilidad,
            precio_total
    from paquetes
    where id_paquete = p_id and activo = 1;

end$$

delimiter ;

-- Modificar datos por id
drop procedure if exists sp_paquete_modificar;

delimiter $$

create procedure sp_paquete_modificar(
    in p_nombre varchar(100),
    in p_fechai date,
    in p_fechaf date,
    in p_disp int,
    in p_id int
)
begin

    update paquetes
    set nombre_paquete = p_nombre,
        fecha_inicio = p_fechai,
        fecha_fin = p_fechaf,
        disponibilidad = p_disp
    where id_paquete = p_id;

end$$

delimiter ;

-- Eliminar Destino por ID
drop procedure if exists sp_paquete_eliminar;

delimiter $$

create procedure sp_paquete_eliminar(
    in p_id int
)
begin 

update paquetes
set activo = 0
where id_paquete = p_id and activo = 1;

end$$

delimiter ;

-- Anadir destino a paquete
drop procedure if exists sp_paquete_destino_anadir;

delimiter $$

create procedure sp_paquete_destino_anadir(
    in p_id int,
    in d_id int
)
begin 

    declare pd_id int;
    select id_paquete_destino into pd_id from paquete_destino where id_paquete = p_id and id_destino = d_id limit 1;

    if pd_id is null then
        insert into paquete_destino(id_paquete,id_destino)
        values  (p_id,d_id);
    end if;

end$$

delimiter ;

-- Mostrar Destino de Paquete
drop procedure if exists sp_paquete_destino_listar;

delimiter $$

create procedure sp_paquete_destino_listar(
    in p_id int
)
begin 

    select  d.nombre_destino,
            d.costo
    from paquete_destino pd
    inner join destinos d on pd.id_destino = d.id_destino
    where pd.id_paquete = p_id;

end$$

delimiter ;