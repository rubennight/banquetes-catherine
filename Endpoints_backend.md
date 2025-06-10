# Endpoints backend

# 📚 Proyecto Banquetes Catherine

## Bases de Datos II

**Docente:** Antonio de la Rosa

**Fecha:** 7 de Junio de 2025

---

## 🎯 Objetivo General

Desarrollar una API RESTful que permita gestionar los eventos de banquetes, usuarios, menús personalizados, empleados y la logística completa que involucra la planeación y ejecución de eventos sociales como bodas, bautizos, XV años y eventos casuales.

---

### 🍽️ Endpoint: `usuarios/infoCarta`

### Descripción

Obtener información para tarjeta de platillos

| Atributo | Valor |
| --- | --- |
| **URL** | `/usuarios/infoCarta` |
| **Método** | `GET` |

### 🔹 Entrada

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| N/E | N/E | N/E |

### 📥 Request

```json
N/E

```

### ✅ Salida (Caso Éxito)

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `numeric` | `idPlatillo` | Identificador del platillo |
| `string` | `descripcionPlatillo` | Descripción del platillo |
| `string` | `tipoPlatillo` | Tipo de platillo |
| `numeric` | `precio` | Precio por cada 100 personas |
| `string` | `imagen` | URL de la imagen del platillo |
| `array` | `ingredientes` | Arreglo de ingredientes |
| `object` | - | Objeto del arreglo de ingredientes |
| `string` | `descripcionIngrediente` | Descripción del ingrediente |
| `string` | `tipoIngrediente` | Tipo de ingrediente |
| `array` | `menu` | Arreglo de menús donde el platillo se encuentra |
| `object` | - | Objeto del arreglo de menús |
| `string` | `nombreMenu` | Nombre del menú |
| `string` | `descripcionMenu` | Descripción del menú |
| `numeric` | `precioMenu` | Precio del menú |

### 📤 Response (Ejemplo)

```json
{
  "idPlatillo": 1,
  "descripcionPlatillo": "Paella Valenciana",
  "tipoPlatillo": "Principal",
  "precio": 4500,
  "imagen": "<https://ejemplo.com/imagenes/paella.jpg>",
  "ingredientes": [
    {
      "descripcionIngrediente": "Arroz de grano corto",
      "tipoIngrediente": "Cereal"
    },
    {
      "descripcionIngrediente": "Mariscos frescos",
      "tipoIngrediente": "Proteína"
    },
    {
      "descripcionIngrediente": "Azafrán",
      "tipoIngrediente": "Especia"
    }
  ],
  "menus": [
    {
      "nombreMenu": "Menú Mediterráneo",
      "descripcionMenu": "Una selección de sabores tradicionales del Mediterráneo.",
      "precioMenu": 7500
    },
    {
      "nombreMenu": "Especial de Mariscos",
      "descripcionMenu": "Un menú centrado en los productos del mar más frescos.",
      "precioMenu": 8200
    }
  ]
}

```

### 📝 Observaciones

- Deberá regresar al menos **8 platillos**

---

### 🔐 Endpoint: `usuarios/login`

### Descripción

Iniciar sesión en el sistema

| Atributo | Valor |
| --- | --- |
| **URL** | `/usuarios/login` |
| **Método** | `POST` |

### 🔹 Entrada

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `string` | `usuario` | Nombre de usuario |
| `string` | `password` | Contraseña |

### 📥 Request

```json
{
  "usuario": "jperez",
  "password": "mipassword123"
}

```

### ✅ Salida (Caso Éxito)

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `numeric` | `idUsuario` | Identificador del usuario |
| `string` | `usuario` | Alias del usuario |
| `string` | `email` | Correo electrónico |
| `string` | `tipoUsuario` | CLIENTE o ADMINISTRADOR |
| `char` | `activo` | Indica si el usuario está activo (`S` o `N`) |

### 📤 Response (Ejemplo)

```json
{
  "id_usuario": 1,
  "usuario": "jperez",
  "email": "jperez@example.com",
  "tipo_usuario": "CLIENTE",
  "activo": "S"
}

```

### 📝 Observaciones

- N/A

---

### 👥 Endpoint: `empleados/porEvento`

### Descripción

Obtener lista de empleados asignados a un evento

| Atributo | Valor |
| --- | --- |
| **URL** | `/empleados/porEvento` |
| **Método** | `GET` |

### 🔹 Entrada

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `numeric` | `idEvento` | ID del evento |

### 📥 Request

```json
	idEvento
```

### ✅ Salida (Caso Éxito)

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `numeric` | `idEvento` | ID del evento |
| `array` | `empleados` | Lista de empleados |
| `object` | - | Información del empleado |
| `numeric` | `idEmpleado` | ID del empleado |
| `string` | `nombre` | Nombre del empleado |
| `string` | `apellido` | Apellido del empleado |
| `string` | `puesto` | Puesto del empleado |

### 📤 Response (Ejemplo)

```json
{
  "idEvento": 12345,
  "empleados": [
    {
      "idEmpleado": 1,
      "nombre": "Juan",
      "apellido": "Pérez",
      "puesto": "Ingeniero"
    },
    {
      "idEmpleado": 2,
      "nombre": "María",
      "apellido": "Gómez",
      "puesto": "Analista"
    },
    {
		"idEmpleado": 3,
		"nombre": "Luis",
		"apellido": "Rodríguez",
		"puesto": "Diseñador"
		}
	]
}
```

### 📝 Observaciones

- Si el evento no existe:

```json
{"error":"Evento no existe","codigo": 404}

```

---

### 🧑‍💼 Endpoint: `eventos/asignarEmpleados`

### Descripción

Asignar uno o varios empleados a un evento.

| Atributo | Valor |
| --- | --- |
| **URL** | `/eventos/asignarEmpleados` |
| **Método** | `POST` |

### 🔹 Entrada

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `numeric` | `idEvento` | ID del evento |
| `array` | `empleados` | Lista de IDs de empleados |
| `object` | - | Información de empleados |
| `numeric` | idEmpleado | ID del empleado |

### 📥 Request

```json
{
  "id_evento": 5,
  "empleados": [3, 7]
}

```

### ✅ Salida (Caso Éxito)

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `string` | `mensaje` | “Los empleados se han asignado correctamente” |

### 📤 Response (Ejemplo)

```json
{ "mensaje": "2 empleados asignados correctamente" }

```

### 📝 Observaciones

- Se tendrá que validar si el empleado no tiene un evento asignado el mismo día. Si un empleado no esta disponible y el resto si lo está, se agregan solo aquellos con disponibilidad

---

### 🗓️ Endpoint: `eventos/registrar`

Observaciones:
HACE FALTA UNA TABLA QUE LIGUE LOS EVENTOS
CON EL CLIENTE

### Descripción

Registrar un nuevo evento.

| Atributo | Valor |
| --- | --- |
| **URL** | `/eventos/registrar` |
| **Método** | `POST` |

### 🔹 Entrada

El precio debe calcularse dentro del backend

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `datetime` | `fechaEvento` | Fecha del evento en formato `"dd-mm-yyyy HH:MM:SS"` |
| `string` | `tipoEvento` | Valores permitidos: `BODA`, `BAUTIZO`, `XVs`, `EVENTO_CASUAL` |
| `string` | `descripcion` | Descripcion del evento, incluyendo el lugar del mismo |
| `numeric` | `idUsuario` | Identificador del usuario que nos ligará a un cliente. |
| `object` |  | Objeto que puede contener un menú existente (`idMenu`) o personalizado |
| `numeric` | `idMenu` | En caso de no personalizar su menú, este campo
vendrá con el id del menú elegido y el resto de los
campos serán null, de lo contrario este campo será null
y el resto de los campos estarán poblados. Si es un menú personalizado se tendrá que validar; si no existe un menú con los mismos platillos seleccionados, este menú personalizado se agrega a la base de datos, de lo contrario se asigna el menú existente. |
| `string` | `descripcion` | Descripción del menú personalizado |
| `string` | `nombre` | Nombre del menú |
| `numeric` | `idPlatilloEntrada` | Id del platillo que será la entrada del menú, este espacio
no puede ser null |
| `numeric` | `idPlatilloSopa` | Id del platillo que será la entrada del menú, este espacio
puede ser null |
| `numeric` | `idPlatilloPlatoPrincipal` | Id del platillo principal del menú, este campo no peude
ser null |
| `numeric` | `idPlatilloPostre` | Id del platillo que ser´pa postre, este campo no puede
ser null |
| `numeric` | `idPlatilloBebidas` | Id del platillo que representa las bebidas, no puede ser
null |
| `numeric` | `idPlatilloInfantil` | Id del platillo infantil, el campó puede ser null |

### 📥 Request

```json
{
  "fechaEvento": "07-06-2025 18:30:00",
  "tipoEvento": "BODA",
  "descripcion": "Boda en Hacienda El Paraíso, Guadalajara, Jalisco",
  "idUsuario": 1234,
  "menu": {
    "idMenu": null,
    "descripcion": "Menú gourmet personalizado con platillos regionales",
    "nombre": "Menú Boda Jalisco",
    "idPlatilloEntrada": 101,
    "idPlatilloSopa": 202,
    "idPlatilloPlatoPrincipal": 303,
    "idPlatilloPostre": 404,
    "idPlatilloBebidas": 505,
    "idPlatilloInfantil": 606
  }
}
{
		"fechaEvento": "15-12-2025 20:00:00",
		"tipoEvento": "XV",
		"descripcion": "Fiesta de XV años en Salón Real del Sol, CDMX",
		"idUsuario": 5678,
		"menu": {
		"idMenu": 12,
		"descripcion": null,
		"nombre": null,
		"idPlatilloEntrada": null,
		"idPlatilloSopa": null,
		"idPlatilloPlatoPrincipal": null,
		"idPlatilloPostre": null,
		"idPlatilloBebidas": null,
		"idPlatilloInfantil": null
	}
}
```

### ✅ Salida (Caso Éxito)

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `numeric` | `idEvento` | Regresará el id del event |
| `numeric` | `precio` | Precio total del evento |

### 📤 Response (Ejemplo)

```json
{
  "idEvento": 9876,
  "precio": 85000
}

```

### 📝 Observaciones

- Si el menú ya existe (mismos platillos), se reutiliza.
- Si no, se crea uno nuevo.
- El precio se calcula automáticamente basándose en los platillos del menú.

### 📤 Error (Ejemplo)

```json
{"error": "Mensaje Personalziado", "codigo": 400}
```

---

### 📋 Endpoint: `eventos/listar`

### Descripción

Listar todos los eventos registrados.

| Atributo | Valor |
| --- | --- |
| **URL** | `/eventos/listar` |
| **Método** | `GET` |

### 🔹 Entrada

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| N/E | N/E | N/E |

### 📥 Request

```json
N/E

```

### ✅ Salida (Caso Éxito)

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `array` | `eventos` | Lista de eventos |
| `object` | - | Información del evento |
| `int` | `idEvento` | ID del evento |
| `datetime` | `fechaEvento` | Fecha del evento |
| `string` | `tipoEvento` | Tipo de evento |
| `string` | `descripcion` | Descripción del evento |
| `numeric` | `totalPrecio` | Precio total del evento |
| `object` | `menu` | Información del menú asociado |
| `string` | `nombreMenu` | Nombre del menú |
| `string` | `descripcionMenu` | Descripción del menú |
| `numeric` | `precioMenu` | Precio del menú |
| `array` | `empleados` | Lista de empleados asignados |
| `object` | - | Objecto del arreglo de
empleados |
| `numeric` | `idEmpleado` | ID del empleado |
| `string` | `nombre` | Nombre del empleado |
| `string` | `apellido` | Apellido del empleado |
| `string` | `puesto` | Puesto del empleado |

### 📤 Response (Ejemplo)

```json
{
  "eventos": [
    {
      "idEvento": 1001,
      "fechaEvento": "10-08-2025 17:00:00",
      "tipoEvento": "BODA",
      "descripcion": "Boda en Jardín La Casona, Querétaro",
      "totalPrecio": 95000,
      "menu": {
        "nombreMenu": "Menú Clásico Mexicano",
        "descripcionMenu": "Entrada de quesadillas gourmet, crema de elote, mole poblano con pollo y pastel de tres leches.",
        "precioMenu": 45000
      },
      "empleados": [
        {
          "idEmpleado": 1,
          "nombre": "Luis",
          "apellido": "Ramírez",
          "puesto": "Chef principal"
        },
        {
          "idEmpleado": 2,
          "nombre": "Ana",
          "apellido": "Gómez",
          "puesto": "Mesera"
        }
      ]
    }
  ]
}

```

### 📝 Observaciones

- Devuelve todos los eventos registrados.
- Incluye información del menú y empleados asignados.

### 📤 Error (Ejemplo)

```json
{"error": "Mensaje Personalziado", "codigo": 400}
```

---

### 🔍 Endpoint: `eventos/buscarPorFecha`

### Descripción

Buscar eventos por una fecha específica.

| Atributo | Valor |
| --- | --- |
| **URL** | `/eventos/buscarPorFecha` |
| **Método** | `GET` |

### 🔹 Entrada

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `date` | `fecha` | Fecha a buscar en formato `YYYY-MM-DD` |

### 📥 Request

```
/eventos/buscarPorFecha?fecha=2025-08-10

```

### ✅ Salida (Caso Éxito)

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `array` | `eventos` | Arreglo de objetos evento |
| `object` | - | Información del evento |
| `int` | `idEvento` | ID del evento |
| `datetime` | `fechaEvento` | Fecha del evento |
| `string` | `tipoEvento` | Tipo de evento |
| `string` | `descripcion` | Descripción del evento |
| `numeric` | `totalPrecio` | Precio total del evento |
| `object` | `menu` | Información del menú |
| `string` | `nombreMenu` | Nombre del menú |
| `string` | `descripcionMenu` | Descripción del menú |
| `numeric` | `precioMenu` | Precio del menú |
| `array` | `empleados` | Lista de empleados asignados |
| `object` | - | Objecto del arreglo de
empleados |
| `numeric` | `idEmpleado` | ID del empleado |
| `string` | `nombre` | Nombre del empleado |
| `string` | `apellido` | Apellido del empleado |
| `string` | `puesto` | Puesto del empleado |

### 📤 Response (Ejemplo)

```json
{
  "eventos": [
    {
      "idEvento": 1001,
      "fechaEvento": "10-08-2025 17:00:00",
      "tipoEvento": "BODA",
      "descripcion": "Boda en Jardín La Casona, Querétaro",
      "totalPrecio": 95000,
      "menu": {
        "nombreMenu": "Menú Clásico Mexicano",
        "descripcionMenu": "Entrada de quesadillas gourmet, crema de elote, mole poblano con pollo y pastel de tres leches.",
        "precioMenu": 45000
      },
      "empleados": [
        {
          "idEmpleado": 1,
          "nombre": "Luis",
          "apellido": "Ramírez",
          "puesto": "Chef principal"
        },
        {
          "idEmpleado": 2,
          "nombre": "Ana",
          "apellido": "Gómez",
          "puesto": "Mesera"
        }
      ]
    }
  ]
}

```

### 📝 Observaciones

- Devuelve todos los eventos programados en la fecha especificada.
- Incluye información completa del menú y empleados asignados.

### 📤 Error (Ejemplo)

```json
{"error": "Mensaje Personalziado", "codigo": 400}
```

---

### 🍽️ Endpoint: `menus/obtenerPorId`

### Descripción

Obtener información detallada de un menú por su ID.

| Atributo | Valor |
| --- | --- |
| **URL** | `/menus/obtenerPorId` |
| **Método** | `GET` |

### 🔹 Entrada

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `numeric` | `idMenu` | ID del menú |

### 📥 Request

```
/menus/obtenerPorId?idMenu=25

```

### ✅ Salida (Caso Éxito)

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `numeric` | `idMenu` | ID del menú |
| `string` | `nombreMenu` | Nombre del menú |
| `string` | `descripcionMenu` | Descripción del menú |
| `numeric` | `precioMenu` | Precio del menú |
| `array` | `platillos` | Listado de platillos del menú |
| `object` | - | Información del platillo |
| `numeric` | `idPlatillo` | ID del platillo |
| `string` | `descripcionPlatillo` | Descripción del platillo |
| `string` | `tipoPlatillo` | Tipo de platillo |
| `numeric` | `precio` | Precio por cada 100 personas |
| `string` | `imagen` | URL de la imagen del platillo |
| `array` | `ingredientes` | Arreglo de ingredientes |
| `object` | - | Objeto del arreglo de
ingredientes |
| `string` | `descripcionIngrediente` | Descripción del ingrediente |
| `string` | `tipoIngrediente` | Tipo de ingrediente |

### 📤 Response (Ejemplo)

```json
{
  "idMenu": 25,
  "nombreMenu": "Menú Gourmet Fiesta",
  "descripcionMenu": "Menú de cuatro tiempos para eventos elegantes con opciones internacionales.",
  "precioMenu": 58000,
  "platillos": [
    {
      "idPlatillo": 101,
      "descripcionPlatillo": "Carpaccio de res con parmesano",
      "tipoPlatillo": "Entrada",
      "precio": 8000,
      "imagen": "<https://ejemplo.com/imagenes/carpaccio.jpg>",
      "ingredientes": [
        { "descripcionIngrediente": "Láminas de res", "tipoIngrediente": "Carne" },
        { "descripcionIngrediente": "Queso parmesano", "tipoIngrediente": "Lácteo" },
        { "descripcionIngrediente": "Aceite de oliva", "tipoIngrediente": "Grasa" }
      ]
    }
  ]
}

```

### 📝 Observaciones

- Devuelve toda la información asociada al menú incluyendo platillos e ingredientes.

---

### 🧾 Endpoint: `menus/agregar`

### Descripción

Agregar un menú personalizado al sistema.

| Atributo | Valor |
| --- | --- |
| **URL** | `/menus/agregar` |
| **Método** | `POST` |

### 🔹 Entrada

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `string` | `nombre` | Nombre del menú |
| `string` | `descripcion` | Descripción del menú personalizado |
| `numeric` | `idPlatilloEntrada` | Id del platillo que será la entrada del menú,
este espacio no puede ser null |
| `numeric` | `idPlatilloSopa` | Id del platillo que será la entrada del menú,
este espacio puede ser null |
| `numeric` | `idPlatilloPlatoPrincipal` | Id del platillo principal del menú, este campo
no peude ser null |
| `numeric` | `idPlatilloPostre` | Id del platillo que es para postre, este campo no puede ser null |
| `numeric` | `idPlatilloBebidas` | Id del platillo que representa las bebidas, no
puede ser nul |
| `numeric` | `idPlatilloInfantil` | Id del platillo infantil, el campó puede ser null |

### 📥 Request

```json
{
  "nombre": "Menú Boda Gourmet Mexicana",
  "descripcion": "Menú personalizado para boda con enfoque en cocina mexicana contemporánea.",
  "idPlatilloEntrada": 101,
  "idPlatilloSopa": null,
  "idPlatilloPlatoPrincipal": 303,
  "idPlatilloPostre": 404,
  "idPlatilloBebidas": 505,
  "idPlatilloInfantil": null
}

```

### ✅ Salida (Caso Éxito)

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `Object` |  | Informacion del menú creado |
| `numeric` | `idMenu` | ID del menú agregado |
| `string` | `nombre` | Nombre del menú |

### 📤 Response (Ejemplo)

```json
{
  "idMenu": 37,
  "nombre": "Menú Boda Gourmet Mexicana"
}

```

### 📝 Observaciones

- Si ya existe un menú con los mismos platillos, se reutiliza y no se crea uno nuevo.
- El campo `idPlatilloSopa` y `idPlatilloInfantil` son opcionales.

---

### 👥 Endpoint: `empleados/porDisponibilidad`

### Descripción

Obtener lista de empleados disponibles para una fecha específica (basado en un evento).

| Atributo | Valor |
| --- | --- |
| **URL** | `/empleados/porDisponibilidad` |
| **Método** | `GET` |

### 🔹 Entrada

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `numeric` | `idEvento` | ID del evento |

### 📥 Request

```
/empleados/porDisponibilidad?idEvento=12345

```

### ✅ Salida (Caso Éxito)

| Tipo de Dato | Campo | Observaciones |
| --- | --- | --- |
| `array` | `empleados` | Lista de empleados |
| `object` | - | Información del empleado |
| `numeric` | `idEmpleado` | ID del empleado |
| `string` | `nombre` | Nombre del empleado |
| `string` | `apellido` | Apellido del empleado |
| `string` | `puesto` | Puesto del empleado |

### 📤 Response (Ejemplo)

```json
[
  {
    "idEmpleado": 1,
    "nombre": "Juan",
    "apellido": "Pérez",
    "puesto": "Ingeniero"
  },
  {
    "idEmpleado": 2,
    "nombre": "María",
    "apellido": "Gómez",
    "puesto": "Analista"
  },
  {
    "idEmpleado": 3,
    "nombre": "Luis",
    "apellido": "Rodríguez",
    "puesto": "Diseñador"
  }
]

```

### 📝 Observaciones

- Se evalúa la fecha del evento asociado al `idEvento`.
- Solo se devuelven los empleados que no tienen otro evento asignado en esa fecha.

> ❌ Error: Si el evento no existe:
> 

```json
{"error":"Evento no existe","codigo": 404}

```

---