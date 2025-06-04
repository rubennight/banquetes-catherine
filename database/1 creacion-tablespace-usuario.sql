-- 1. Crear tablespace (opcional pero recomendado)
CREATE TABLESPACE ts_banquetes
DATAFILE 'ts_banquetes.dbf' SIZE 100M AUTOEXTEND ON;

-- 1.2 Verifica el contenedor actual
SHOW CON_NAME;

-- 1.3 Cambia al contenedor pluggable (XEPDB1 es el predeterminado en XE)
ALTER SESSION SET CONTAINER = XEPDB1;

-- 1.4 Desactiva temporalmente la validación de nombres
ALTER SESSION SET "_ORACLE_SCRIPT"=true;

-- 2. Crear usuario (esto crea automáticamente tu esquema)
CREATE USER banquetes_admin IDENTIFIED BY "banquetes2025"
DEFAULT TABLESPACE ts_banquetes_catherine
TEMPORARY TABLESPACE temp
QUOTA UNLIMITED ON ts_banquetes_catherine;

-- 3. Dar privilegios básicos
GRANT CONNECT, RESOURCE TO banquetes_admin;

-- 4. Desde SQL*Plus (después de desconectarte)
CONNECT banquetes_admin/banquetes2025@localhost/XEPDB1

-- Conexion: jdbc:oracle:thin:@localhost:1521/XEPDB1
-- Iniciar conexion: sqlplus banquetes_admin/"banquetes2025"@localhost/XEPDB1