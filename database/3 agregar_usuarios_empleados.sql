-- Usuarios para los 5 gerentes
INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('gcuentas1', 'G3r3nt3C!', 'gcuentas1@banquetes.com', 'GERENTE_CUENTAS');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('geventos1', 'G3r3nt3E!', 'geventos1@banquetes.com', 'GERENTE_EVENTOS');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('grh1', 'G3r3nt3RH!', 'grh1@banquetes.com', 'GERENTE_RH');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('gcuentas2', 'G3r3nt3C2!', 'gcuentas2@banquetes.com', 'GERENTE_CUENTAS');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('geventos2', 'G3r3nt3E2!', 'geventos2@banquetes.com', 'GERENTE_EVENTOS');

-- Usuarios para los 30 empleados
INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('chef1', 'Ch3fEj3c!', 'chef1@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('superv1', 'Sup3rv1s0r!', 'supervisor1@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('chef2', 'Ch3fC0c1n4!', 'chef2@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('pastelera', 'P4st3l3r14!', 'pastelera@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('mesero1', 'M3s3r01!', 'mesero1@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('mesera1', 'M3s3r41!', 'mesera1@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('barman1', 'B4rm4n1!', 'barman1@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('hostess1', 'H0st3ss1!', 'hostess1@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('coord1', 'C00rd3vnt!', 'coordeventos@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('disenio1', 'D1s3ñ0M3n!', 'diseniomenu@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('ayudante1', '4yud4nt3!', 'ayudante1@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('recepc1', 'R3c3pc1!', 'recepcion@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('compras1', 'C0mpr4s1!', 'compras@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('coordper', 'C00rdp3rs!', 'coordpersonal@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('valet1', 'V4l3tp4rk!', 'valet@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('anfitrion', '4nf1tr01!', 'anfitriona@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('sommelier', 'S0mm3l13r!', 'sommelier@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('bodas1', 'B0d4sC00rd!', 'bodas@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('seguridad', 'S3gur1d4d!', 'seguridad@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('lavanderia', 'L4v4nd3r1!', 'lavanderia@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('audiovideo', '4ud10v1d30!', 'audiovideo@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('decoracion', 'D3c0r4c10n!', 'decoracion@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('mantenim', 'M4nt3n1m!', 'mantenimiento@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('limpieza1', 'L1mp13z4!', 'limpieza@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('contador1', 'C0nt4d0r!', 'contabilidad@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('asistger', '4s1stg3r!', 'asistgerencia@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('ayudgen', '4yudg3n3r!', 'ayudgeneral@banquetes.com', 'ADMIN');

INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('florista1', 'Fl0r1st41!', 'florista@banquetes.com', 'ADMIN');

COMMIT;

-- Empleados que son gerentes (5)
INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(1, 'TIEMPO_COMPLETO', 'Roberto', 'Mendoza', 'Gerente de Cuentas Senior');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(2, 'TIEMPO_COMPLETO', 'Sofía', 'López', 'Gerente de Eventos Premium');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(3, 'TIEMPO_COMPLETO', 'Carlos', 'Ruiz', 'Gerente de Recursos Humanos');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(4, 'TIEMPO_COMPLETO', 'Ana', 'García', 'Gerente de Cuentas Corporativas');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(5, 'TIEMPO_COMPLETO', 'Miguel', 'Torres', 'Gerente de Eventos Especiales');

-- Empleados regulares (25)
INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(6, 'TIEMPO_COMPLETO', 'Fernando', 'Martínez', 'Chef Ejecutivo');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(7, 'TIEMPO_COMPLETO', 'Patricia', 'Gómez', 'Supervisora de Banquetes');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(8, 'TIEMPO_COMPLETO', 'Alejandro', 'Vázquez', 'Chef de Cocina');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(9, 'TIEMPO_COMPLETO', 'Mariana', 'Hernández', 'Jefa de Pastelería');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(10, 'MEDIO_TIEMPO', 'Juan', 'Pérez', 'Mesero');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(11, 'MEDIO_TIEMPO', 'Laura', 'Díaz', 'Mesera');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(12, 'MEDIO_TIEMPO', 'Ricardo', 'Sánchez', 'Barman');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(13, 'MEDIO_TIEMPO', 'Gabriela', 'Castro', 'Hostess');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(14, 'TIEMPO_COMPLETO', 'Oscar', 'Ramírez', 'Coordinador de Eventos');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(15, 'TIEMPO_COMPLETO', 'Lucía', 'Fernández', 'Diseñadora de Menús');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(16, 'MEDIO_TIEMPO', 'Jorge', 'Jiménez', 'Ayudante de Cocina');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(17, 'MEDIO_TIEMPO', 'Daniela', 'Morales', 'Recepcionista');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(18, 'TIEMPO_COMPLETO', 'Arturo', 'Silva', 'Jefe de Compras');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(19, 'TIEMPO_COMPLETO', 'Adriana', 'Luna', 'Coordinadora de Personal');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(20, 'MEDIO_TIEMPO', 'Raúl', 'Ortega', 'Valet Parking');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(21, 'MEDIO_TIEMPO', 'Isabel', 'Cortés', 'Anfitriona');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(22, 'TIEMPO_COMPLETO', 'Francisco', 'Núñez', 'Sommelier');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(23, 'TIEMPO_COMPLETO', 'Verónica', 'Ríos', 'Coordinadora de Bodas');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(24, 'MEDIO_TIEMPO', 'Héctor', 'Vega', 'Seguridad');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(25, 'MEDIO_TIEMPO', 'Carmen', 'Pineda', 'Lavandería');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(26, 'TIEMPO_COMPLETO', 'Eduardo', 'Miranda', 'Técnico de Audio y Video');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(27, 'TIEMPO_COMPLETO', 'Diana', 'Rosas', 'Diseñadora de Decoración');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(28, 'MEDIO_TIEMPO', 'Sergio', 'Campos', 'Mantenimiento');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(29, 'MEDIO_TIEMPO', 'Teresa', 'Mejía', 'Limpieza');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(30, 'TIEMPO_COMPLETO', 'Manuel', 'Rojas', 'Contador');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(31, 'TIEMPO_COMPLETO', 'Paulina', 'Guerrero', 'Asistente de Gerencia');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(32, 'MEDIO_TIEMPO', 'Javier', 'Santos', 'Ayudante General');

INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto) VALUES
(33, 'MEDIO_TIEMPO', 'Liliana', 'Cervantes', 'Florista');

COMMIT;

-- Asignar los 5 gerentes
INSERT INTO gerentes (id_empleado, tipo_gerente, especialidad, nivel_acceso) VALUES
(1, 'CUENTAS', 'Clientes Corporativos', 3);

INSERT INTO gerentes (id_empleado, tipo_gerente, especialidad, nivel_acceso) VALUES
(2, 'EVENTOS', 'Eventos Premium', 3);

INSERT INTO gerentes (id_empleado, tipo_gerente, especialidad, nivel_acceso) VALUES
(3, 'RH', 'Reclutamiento y Capacitación', 2);

INSERT INTO gerentes (id_empleado, tipo_gerente, especialidad, nivel_acceso) VALUES
(4, 'CUENTAS', 'Cuentas Clave', 2);

INSERT INTO gerentes (id_empleado, tipo_gerente, especialidad, nivel_acceso) VALUES
(5, 'EVENTOS', 'Bodas y Eventos Especiales', 2);

COMMIT;
