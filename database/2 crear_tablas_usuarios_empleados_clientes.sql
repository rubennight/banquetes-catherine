-- Secuencia para usuarios
CREATE SEQUENCE seq_usuarios 
START WITH 1 
INCREMENT BY 1 
NOCACHE NOCYCLE;

-- Secuencia para clientes
CREATE SEQUENCE seq_clientes 
START WITH 1 
INCREMENT BY 1 
NOCACHE NOCYCLE;

-- Secuencia para empleados
CREATE SEQUENCE seq_empleados 
START WITH 1 
INCREMENT BY 1 
NOCACHE NOCYCLE;

-- Secuencia para gerentes
CREATE SEQUENCE seq_gerentes 
START WITH 1 
INCREMENT BY 1 
NOCACHE NOCYCLE;

-- Tabla USUARIOS
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

-- Tabla CLIENTES
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

-- Tabla EMPLEADOS
CREATE TABLE empleados (
    id_empleado NUMBER PRIMARY KEY,
    id_usuario NUMBER CONSTRAINT fk_empleado_usuario REFERENCES usuarios(id_usuario),
    tipo_contrato VARCHAR2(20),
    nombre VARCHAR2(100) CONSTRAINT nn_empleado_nombre NOT NULL,
    apellido VARCHAR2(100) CONSTRAINT nn_empleado_apellido NOT NULL,
    puesto VARCHAR2(50) CONSTRAINT nn_empleado_puesto NOT NULL,
    fecha_contratacion DATE DEFAULT SYSDATE,
    activo CHAR(1) DEFAULT 'S',
    CONSTRAINT ck_tipo_contrato CHECK (tipo_contrato IN ('TIEMPO_COMPLETO', 'MEDIO_TIEMPO')),
    CONSTRAINT ck_empleado_activo CHECK (activo IN ('S', 'N')),
    CONSTRAINT uk_empleado_usuario UNIQUE (id_usuario)
);

-- Tabla GERENTES
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

-- Trigger para USUARIOS
CREATE OR REPLACE TRIGGER trg_usuarios
BEFORE INSERT ON usuarios
FOR EACH ROW
BEGIN
    IF :NEW.id_usuario IS NULL THEN
        SELECT seq_usuarios.NEXTVAL INTO :NEW.id_usuario FROM DUAL;
    END IF;
END;
/

-- Trigger para CLIENTES
CREATE OR REPLACE TRIGGER trg_clientes
BEFORE INSERT ON clientes
FOR EACH ROW
BEGIN
    IF :NEW.id_cliente IS NULL THEN
        SELECT seq_clientes.NEXTVAL INTO :NEW.id_cliente FROM DUAL;
    END IF;
END;
/

-- Trigger para EMPLEADOS
CREATE OR REPLACE TRIGGER trg_empleados
BEFORE INSERT ON empleados
FOR EACH ROW
BEGIN
    IF :NEW.id_empleado IS NULL THEN
        SELECT seq_empleados.NEXTVAL INTO :NEW.id_empleado FROM DUAL;
    END IF;
END;
/

-- Trigger para GERENTES
CREATE OR REPLACE TRIGGER trg_gerentes
BEFORE INSERT ON gerentes
FOR EACH ROW
BEGIN
    IF :NEW.id_gerente IS NULL THEN
        SELECT seq_gerentes.NEXTVAL INTO :NEW.id_gerente FROM DUAL;
    END IF;
END;
/