CREATE SEQUENCE seq_evento_cliente START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

CREATE TABLE evento_cliente (
    id_evento_cliente NUMBER PRIMARY KEY,
    id_evento NUMBER REFERENCES eventos(id_evento),
    id_cliente NUMBER REFERENCES clientes(id_cliente),
    fecha_registro DATE DEFAULT SYSDATE,
    CONSTRAINT uk_evento_cliente UNIQUE (id_evento)
);

CREATE OR REPLACE TRIGGER trg_evento_cliente
BEFORE INSERT ON evento_cliente
FOR EACH ROW
BEGIN
    IF :NEW.id_evento_cliente IS NULL THEN
        SELECT seq_evento_cliente.NEXTVAL INTO :NEW.id_evento_cliente FROM DUAL;
    END IF;
END;
/

--Esto se debe hacer para que permita insertar nuevos menus
DROP SEQUENCE seq_evento_menu;

CREATE SEQUENCE seq_evento_menu START WITH 6 INCREMENT BY 1 NOCACHE NOCYCLE;