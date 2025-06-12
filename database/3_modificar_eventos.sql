-- Script para modificar la tabla eventos
-- 1. Crear tabla temporal con la estructura deseada
CREATE TABLE eventos_temp (
    id_evento NUMBER PRIMARY KEY,
    fecha_evento TIMESTAMP,
    tipo_evento VARCHAR2(20),
    descripcion VARCHAR2(250),
    total_precio NUMBER,
    CONSTRAINT ck_tipo_evento_temp CHECK (tipo_evento IN ('BODA', 'BAUTIZO', 'XVs', 'EVENTO_CASUAL'))
);

-- 2. Copiar datos existentes a la tabla temporal, combinando fecha_evento y hora_evento
INSERT INTO eventos_temp (id_evento, fecha_evento, tipo_evento, descripcion, total_precio)
SELECT 
    id_evento,
    CAST(fecha_evento + (CAST(hora_evento AS DATE) - TRUNC(CAST(hora_evento AS DATE))) AS TIMESTAMP),
    tipo_evento,
    descripcion,
    total_precio
FROM eventos;

-- 3. Eliminar la tabla original y sus constraints
DROP TABLE eventos CASCADE CONSTRAINTS;

-- 4. Renombrar la tabla temporal a eventos
ALTER TABLE eventos_temp RENAME TO eventos;

-- 5. Eliminar la secuencia existente y recrearla
DROP SEQUENCE seq_eventos;
CREATE SEQUENCE seq_eventos START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

CREATE OR REPLACE TRIGGER trg_eventos
BEFORE INSERT ON eventos
FOR EACH ROW
BEGIN
    IF :NEW.id_evento IS NULL THEN
        SELECT seq_eventos.NEXTVAL INTO :NEW.id_evento FROM DUAL;
    END IF;
END;
/

-- 6. Recrear las foreign keys que apuntan a eventos
ALTER TABLE evento_empleados ADD CONSTRAINT fk_evento_empleados_evento 
    FOREIGN KEY (id_evento) REFERENCES eventos(id_evento);

ALTER TABLE evento_menu ADD CONSTRAINT fk_evento_menu_evento 
    FOREIGN KEY (id_evento) REFERENCES eventos(id_evento);

ALTER TABLE evento_cliente ADD CONSTRAINT fk_evento_cliente_evento 
    FOREIGN KEY (id_evento) REFERENCES eventos(id_evento);

-- 7. Comentarios para documentar los cambios
COMMENT ON TABLE eventos IS 'Tabla de eventos modificada para usar TIMESTAMP y tipo_evento más corto';
COMMENT ON COLUMN eventos.fecha_evento IS 'Fecha y hora del evento en formato TIMESTAMP';
COMMENT ON COLUMN eventos.tipo_evento IS 'Tipo de evento: BODA, BAUTIZO, XVs, EVENTO_CASUAL'; 