-- Conéctate como banquetes_admin
CONNECT banquetes_admin/banquetes2025@localhost/XEPDB1

-- Iniciar transacción
SET TRANSACTION NAME 'LIMPIEZA_BD';

-- Primero tablas que referencian a otras
DELETE FROM gerentes;
DELETE FROM clientes;
DELETE FROM empleados;
DELETE FROM usuarios;

-- Si tienes más tablas con relaciones, agrégales aquí
-- DELETE FROM nombre_tabla;

-- Reiniciar secuencias a 1
ALTER SEQUENCE seq_usuarios RESTART START WITH 1;
ALTER SEQUENCE seq_clientes RESTART START WITH 1;
ALTER SEQUENCE seq_empleados RESTART START WITH 1;
ALTER SEQUENCE seq_gerentes RESTART START WITH 1;

-- Si tienes otras secuencias, agrégales aquí
-- ALTER SEQUENCE seq_nombre RESTART START WITH 1;

-- Se mandan cmabios.
COMMIT;
