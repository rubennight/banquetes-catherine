
-- SECUENCIAS
CREATE SEQUENCE seq_usuarios START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_clientes START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_empleados START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_gerentes START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_platillos START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_ingredientes START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_platillo_ingrediente START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_eventos START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_evento_empleados START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_menus START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_evento_menu START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

-- TABLAS
CREATE TABLE usuarios (
    id_usuario NUMBER PRIMARY KEY,
    usuario VARCHAR2(50) CONSTRAINT nn_usuario NOT NULL,
    password VARCHAR2(100) CONSTRAINT nn_password NOT NULL,
    email VARCHAR2(100) CONSTRAINT nn_email NOT NULL,
    tipo_usuario VARCHAR2(20),
    fecha_creacion DATE DEFAULT SYSDATE,
    activo CHAR(1) DEFAULT 'S',
    CONSTRAINT uk_usuario UNIQUE (usuario),
    CONSTRAINT uk_email UNIQUE (email),
    CONSTRAINT ck_tipo_usuario CHECK (tipo_usuario IN ('CLIENTE', 'GERENTE_CUENTAS', 'GERENTE_EVENTOS', 'GERENTE_RH', 'ADMIN')),
    CONSTRAINT ck_activo CHECK (activo IN ('S', 'N'))
);

CREATE TABLE clientes (
    id_cliente NUMBER PRIMARY KEY,
    id_usuario NUMBER CONSTRAINT fk_cliente_usuario REFERENCES usuarios(id_usuario),
    nombre VARCHAR2(100) CONSTRAINT nn_cliente_nombre NOT NULL,
    apellido VARCHAR2(100) CONSTRAINT nn_cliente_apellido NOT NULL,
    telefono VARCHAR2(20),
    fecha_registro DATE DEFAULT SYSDATE,
    rfc VARCHAR2(13),
    direccion VARCHAR2(200),
    CONSTRAINT uk_cliente_usuario UNIQUE (id_usuario)
);

CREATE TABLE empleados (
    id_empleado NUMBER PRIMARY KEY,
    id_usuario NUMBER CONSTRAINT fk_empleado_usuario REFERENCES usuarios(id_usuario),
    tipo_contrato VARCHAR2(20),
    nombre VARCHAR2(100) CONSTRAINT nn_empleado_nombre NOT NULL,
    apellido VARCHAR2(100) CONSTRAINT nn_empleado_apellido NOT NULL,
    puesto VARCHAR2(50) CONSTRAINT nn_empleado_puesto NOT NULL,
    fecha_contratacion DATE DEFAULT SYSDATE,
    activo CHAR(1) DEFAULT 'S',
    sueldo NUMBER,
    CONSTRAINT ck_tipo_contrato CHECK (tipo_contrato IN ('TIEMPO_COMPLETO', 'MEDIO_TIEMPO')),
    CONSTRAINT ck_empleado_activo CHECK (activo IN ('S', 'N')),
    CONSTRAINT uk_empleado_usuario UNIQUE (id_usuario)
);

CREATE TABLE gerentes (
    id_gerente NUMBER PRIMARY KEY,
    id_empleado NUMBER CONSTRAINT fk_gerente_empleado REFERENCES empleados(id_empleado),
    tipo_gerente VARCHAR2(20),
    especialidad VARCHAR2(100),
    nivel_acceso NUMBER(1) DEFAULT 1,
    CONSTRAINT ck_tipo_gerente CHECK (tipo_gerente IN ('CUENTAS', 'EVENTOS', 'RH')),
    CONSTRAINT ck_nivel_acceso CHECK (nivel_acceso BETWEEN 1 AND 3),
    CONSTRAINT uk_gerente_empleado UNIQUE (id_empleado)
);

CREATE TABLE platillos (
    id_platillo NUMBER PRIMARY KEY,
    descripcion VARCHAR2(250),
    tipo_platillo VARCHAR2(250),
    precio_100_personas NUMBER,
    url_imagen VARCHAR2(250),
    CONSTRAINT ck_tipo_platillo CHECK (tipo_platillo IN ('ENTRADA', 'SOPA', 'PLATILLO_PRINCIPAL', 'POSTRE', 'BEBIDA'))
);

CREATE TABLE ingredientes (
    id_ingrediente NUMBER PRIMARY KEY,
    descripcion VARCHAR2(250),
    tipo_ingrediente VARCHAR2(50),
    CONSTRAINT ck_tipo_ingrediente CHECK (tipo_ingrediente IN ('LACTEOS', 'ESPECIAS', 'VERDURAS', 'FRUTAS', 'CARNES'))
);

CREATE TABLE platillo_ingrediente (
    id_platillo_ingrediente NUMBER PRIMARY KEY,
    id_platillo NUMBER REFERENCES platillos(id_platillo),
    id_ingrediente NUMBER REFERENCES ingredientes(id_ingrediente),
    paso NUMBER,
    cantidad VARCHAR2(250),
    modo_preparacion VARCHAR2(250),
    CONSTRAINT uk_platillo_ingrediente UNIQUE (id_platillo)
);

CREATE TABLE eventos (
    id_evento NUMBER PRIMARY KEY,
    fecha_evento DATE,
    hora_evento DATE,
    tipo_evento VARCHAR2(250),
    descripcion VARCHAR2(250),
    total_precio NUMBER,
    CONSTRAINT ck_tipo_evento CHECK (tipo_evento IN ('BODA', 'BAUTIZO', 'XVs', 'EVENTO_CASUAL'))
);

CREATE TABLE evento_empleados (
    id_evento_empleado NUMBER PRIMARY KEY,
    id_evento NUMBER REFERENCES eventos(id_evento),
    id_empleado NUMBER REFERENCES empleados(id_empleado)
);

CREATE TABLE menus (
    id_menu NUMBER PRIMARY KEY,
    nombre VARCHAR2(250),
    descripcion VARCHAR2(250),
    id_platillo_entrada NUMBER REFERENCES platillos(id_platillo),
    id_platillo_sopa NUMBER REFERENCES platillos(id_platillo),
    id_platillo_plato_principal NUMBER REFERENCES platillos(id_platillo),
    id_platillo_postre NUMBER REFERENCES platillos(id_platillo),
    id_platillo_bebidas NUMBER REFERENCES platillos(id_platillo),
    id_platillo_infantil NUMBER REFERENCES platillos(id_platillo),
    precio NUMBER
);

CREATE TABLE evento_menu (
    id_evento_menu NUMBER PRIMARY KEY,
    id_evento NUMBER REFERENCES eventos(id_evento),
    id_menu NUMBER REFERENCES menus(id_menu)
);

-- TRIGGERS
CREATE OR REPLACE TRIGGER trg_usuarios
BEFORE INSERT ON usuarios
FOR EACH ROW
BEGIN
    IF :NEW.id_usuario IS NULL THEN
        SELECT seq_usuarios.NEXTVAL INTO :NEW.id_usuario FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_clientes
BEFORE INSERT ON clientes
FOR EACH ROW
BEGIN
    IF :NEW.id_cliente IS NULL THEN
        SELECT seq_clientes.NEXTVAL INTO :NEW.id_cliente FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_empleados
BEFORE INSERT ON empleados
FOR EACH ROW
BEGIN
    IF :NEW.id_empleado IS NULL THEN
        SELECT seq_empleados.NEXTVAL INTO :NEW.id_empleado FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_gerentes
BEFORE INSERT ON gerentes
FOR EACH ROW
BEGIN
    IF :NEW.id_gerente IS NULL THEN
        SELECT seq_gerentes.NEXTVAL INTO :NEW.id_gerente FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_platillos
BEFORE INSERT ON platillos
FOR EACH ROW
BEGIN
    IF :NEW.id_platillo IS NULL THEN
        SELECT seq_platillos.NEXTVAL INTO :NEW.id_platillo FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_ingredientes
BEFORE INSERT ON ingredientes
FOR EACH ROW
BEGIN
    IF :NEW.id_ingrediente IS NULL THEN
        SELECT seq_ingredientes.NEXTVAL INTO :NEW.id_ingrediente FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_platillo_ingrediente
BEFORE INSERT ON platillo_ingrediente
FOR EACH ROW
BEGIN
    IF :NEW.id_platillo_ingrediente IS NULL THEN
        SELECT seq_platillo_ingrediente.NEXTVAL INTO :NEW.id_platillo_ingrediente FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_eventos
BEFORE INSERT ON eventos
FOR EACH ROW
BEGIN
    IF :NEW.id_evento IS NULL THEN
        SELECT seq_eventos.NEXTVAL INTO :NEW.id_evento FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_evento_empleados
BEFORE INSERT ON evento_empleados
FOR EACH ROW
BEGIN
    IF :NEW.id_evento_empleado IS NULL THEN
        SELECT seq_evento_empleados.NEXTVAL INTO :NEW.id_evento_empleado FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_menus
BEFORE INSERT ON menus
FOR EACH ROW
BEGIN
    IF :NEW.id_menu IS NULL THEN
        SELECT seq_menus.NEXTVAL INTO :NEW.id_menu FROM DUAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_evento_menu
BEFORE INSERT ON evento_menu
FOR EACH ROW
BEGIN
    IF :NEW.id_evento_menu IS NULL THEN
        SELECT seq_evento_menu.NEXTVAL INTO :NEW.id_evento_menu FROM DUAL;
    END IF;
END;
