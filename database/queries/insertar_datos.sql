
-- USUARIOS
INSERT INTO usuarios (usuario, password, email, tipo_usuario) VALUES
('cliente1', 'pass1', 'cliente1@example.com', 'CLIENTE'),
('cliente2', 'pass2', 'cliente2@example.com', 'CLIENTE'),
('gerente1', 'pass3', 'gerente1@example.com', 'GERENTE_EVENTOS'),
('empleado1', 'pass4', 'empleado1@example.com', 'CLIENTE'),
('admin', 'adminpass', 'admin@example.com', 'ADMIN');

-- CLIENTES
INSERT INTO clientes (id_usuario, nombre, apellido, telefono, rfc, direccion) VALUES
(1, 'Carlos', 'Ramírez', '5551234567', 'CARM880101XYZ', 'Calle Falsa 123'),
(2, 'Laura', 'Pérez', '5557654321', 'LAPE920202ABC', 'Av. Siempre Viva 742'),
(4, 'Ana', 'García', '5559988776', 'ANGR850505DEF', 'Insurgentes Sur 100'),
(5, 'Luis', 'Soto', '5551122334', 'LUSO780808GHI', 'Reforma 350'),
(3, 'Teresa', 'Lopez', '5553344556', 'TELO950909JKL', 'Av. Juárez 90');

-- EMPLEADOS
INSERT INTO empleados (id_usuario, tipo_contrato, nombre, apellido, puesto, sueldo) VALUES
(3, 'TIEMPO_COMPLETO', 'Mario', 'Ruiz', 'Chef', 20000),
(5, 'MEDIO_TIEMPO', 'Lucía', 'Mendoza', 'Mesera', 12000),
(2, 'TIEMPO_COMPLETO', 'Pedro', 'Sánchez', 'Cocinero', 15000),
(4, 'MEDIO_TIEMPO', 'Elena', 'Torres', 'Asistente', 10000),
(1, 'TIEMPO_COMPLETO', 'Raúl', 'Ortega', 'Logística', 17000);

-- GERENTES
INSERT INTO gerentes (id_empleado, tipo_gerente, especialidad, nivel_acceso) VALUES
(1, 'EVENTOS', 'Planeación', 2),
(2, 'CUENTAS', 'Finanzas', 1),
(3, 'RH', 'Recursos Humanos', 3),
(4, 'CUENTAS', 'Contabilidad', 2),
(5, 'EVENTOS', 'Protocolo', 1);

-- PLATILLOS
INSERT INTO platillos (descripcion, tipo_platillo, precio_100_personas, url_imagen) VALUES
('Ensalada César', 'ENTRADA', 1500, 'img/cesar.jpg'),
('Sopa Azteca', 'SOPA', 2000, 'img/sopa_azteca.jpg'),
('Pollo al mole', 'PLATILLO_PRINCIPAL', 4000, 'img/pollo_mole.jpg'),
('Flan napolitano', 'POSTRE', 1800, 'img/flan.jpg'),
('Agua de horchata', 'BEBIDA', 800, 'img/horchata.jpg');

-- INGREDIENTES
INSERT INTO ingredientes (descripcion, tipo_ingrediente) VALUES
('Leche evaporada', 'LACTEOS'),
('Canela', 'ESPECIAS'),
('Zanahoria', 'VERDURAS'),
('Manzana', 'FRUTAS'),
('Pechuga de pollo', 'CARNES');

-- PLATILLO_INGREDIENTE
INSERT INTO platillo_ingrediente (id_platillo, id_ingrediente, paso, cantidad, modo_preparacion) VALUES
(1, 3, 1, '2 tazas', 'Cortar en rodajas'),
(2, 1, 2, '1 taza', 'Agregar a la sopa caliente'),
(3, 5, 3, '1 kg', 'Cocinar en salsa'),
(4, 2, 4, '1 cucharadita', 'Espolvorear encima'),
(5, 4, 5, '3 piezas', 'Licuar y colar');

-- EVENTOS
INSERT INTO eventos (fecha_evento, hora_evento, tipo_evento, descripcion, total_precio) VALUES
(TO_DATE('2025-08-15', 'YYYY-MM-DD'), TO_DATE('15:00', 'HH24:MI'), 'BODA', 'Boda en jardín', 15000),
(TO_DATE('2025-09-10', 'YYYY-MM-DD'), TO_DATE('13:00', 'HH24:MI'), 'XVs', 'Fiesta de 15 años', 12000),
(TO_DATE('2025-10-05', 'YYYY-MM-DD'), TO_DATE('14:00', 'HH24:MI'), 'EVENTO_CASUAL', 'Comida de negocios', 8000),
(TO_DATE('2025-07-01', 'YYYY-MM-DD'), TO_DATE('12:00', 'HH24:MI'), 'BAUTIZO', 'Bautizo familiar', 10000),
(TO_DATE('2025-11-20', 'YYYY-MM-DD'), TO_DATE('18:00', 'HH24:MI'), 'BODA', 'Boda elegante', 20000);

-- EVENTO_EMPLEADOS
INSERT INTO evento_empleados (id_evento, id_empleado) VALUES
(1, 1),
(1, 2),
(2, 3),
(3, 4),
(4, 5);

-- MENUS
INSERT INTO menus (nombre, descripcion, id_platillo_entrada, id_platillo_sopa, id_platillo_plato_principal, id_platillo_postre, id_platillo_bebidas, id_platillo_infantil, precio) VALUES
('Menú Fiesta', 'Completo para eventos formales', 1, 2, 3, 4, 5, 3, 10000),
('Menú Ejecutivo', 'Ideal para reuniones de trabajo', 1, 2, 3, 4, 5, 3, 8500),
('Menú Infantil', 'Opciones suaves y dulces', 1, 2, 3, 4, 5, 3, 7000),
('Menú Vegetariano', 'Sin carnes', 1, 2, 3, 4, 5, 3, 9000),
('Menú Económico', 'Alternativa económica', 1, 2, 3, 4, 5, 3, 6000);

-- EVENTO_MENU
INSERT INTO evento_menu (id_evento, id_menu) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);
