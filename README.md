# CodeCraftHub API

CodeCraftHub es una API REST sencilla, creada con Python y Flask, para aprender
a administrar cursos mediante operaciones CRUD.

CRUD significa:

- **Create:** crear un curso con `POST`.
- **Read:** consultar cursos con `GET`.
- **Update:** actualizar un curso con `PUT`.
- **Delete:** eliminar un curso con `DELETE`.

La API guarda la información localmente en `courses.json`. No es necesario
instalar ni configurar una base de datos.

## Características

- Creación, consulta, actualización y eliminación de cursos.
- IDs numéricos generados automáticamente, comenzando en `1`.
- Fecha y hora de creación generadas automáticamente en UTC.
- Persistencia de datos en un archivo JSON.
- Creación automática de `courses.json` si no existe.
- Validación de campos obligatorios.
- Validación de fechas con formato `YYYY-MM-DD`.
- Validación de los estados permitidos.
- Respuestas y errores en formato JSON.
- Manejo de errores de lectura y escritura del archivo.
- Escritura segura para reducir el riesgo de archivos JSON incompletos.

## Requisitos

Antes de comenzar, instala:

- Python 3.9 o una versión más reciente.
- `pip`, el instalador de paquetes de Python.
- Una terminal.
- `curl` para probar la API desde la terminal.

Comprueba que Python está instalado:

```bash
python3 --version
```

## Instalación paso a paso

### 1. Abre el proyecto

Desde una terminal, entra en la carpeta del proyecto:

```bash
cd "/ruta/hacia/ibm cert"
```

Sustituye `/ruta/hacia/ibm cert` por la ubicación real del proyecto.

### 2. Crea un entorno virtual

Un entorno virtual mantiene las dependencias del proyecto separadas de las
dependencias del sistema:

```bash
python3 -m venv .venv
```

### 3. Activa el entorno virtual

En macOS o Linux:

```bash
source .venv/bin/activate
```

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Cuando esté activo, normalmente verás `(.venv)` al principio de la línea de la
terminal.

### 4. Instala Flask

```bash
python3 -m pip install Flask
```

En Windows también puedes usar:

```powershell
python -m pip install Flask
```

## Ejecutar la aplicación

Con el entorno virtual activo, ejecuta:

```bash
python3 app.py
```

En Windows:

```powershell
python app.py
```

La terminal mostrará una dirección similar a:

```text
http://127.0.0.1:5000
```

Mantén esa terminal abierta mientras utilizas la API. Para detener el servidor,
presiona `Ctrl+C`.

También puedes iniciar el proyecto con el comando de Flask:

```bash
flask --app app run --debug
```

## Modelo de un curso

Cada curso contiene:

- `id`: número generado automáticamente.
- `name`: nombre obligatorio del curso.
- `description`: descripción obligatoria.
- `target_date`: fecha objetivo obligatoria en formato `YYYY-MM-DD`.
- `status`: estado obligatorio.
- `created_at`: fecha y hora de creación generadas automáticamente.

Los únicos valores permitidos para `status` son:

- `Not Started`
- `In Progress`
- `Completed`

Ejemplo:

```json
{
  "id": 1,
  "name": "Python para principiantes",
  "description": "Introducción a Python y Flask",
  "target_date": "2026-12-15",
  "status": "Not Started",
  "created_at": "2026-10-21T21:35:00+00:00"
}
```

## Documentación de la API

Todos los endpoints comienzan con:

```text
http://127.0.0.1:5000/api/courses
```

Los ejemplos siguientes utilizan `curl`. La opción `-i` permite ver también el
código de estado HTTP de la respuesta.

### Crear un curso

- Método: `POST`
- Ruta: `/api/courses`
- Respuesta exitosa: `201 Created`

```bash
curl -i -X POST "http://127.0.0.1:5000/api/courses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python para principiantes",
    "description": "Introducción a Python y Flask",
    "target_date": "2026-12-15",
    "status": "Not Started"
  }'
```

Respuesta de ejemplo:

```json
{
  "id": 1,
  "name": "Python para principiantes",
  "description": "Introducción a Python y Flask",
  "target_date": "2026-12-15",
  "status": "Not Started",
  "created_at": "2026-10-21T21:35:00+00:00"
}
```

No envíes `id` ni `created_at`; la aplicación los genera automáticamente.

### Obtener todos los cursos

- Método: `GET`
- Ruta: `/api/courses`
- Respuesta exitosa: `200 OK`

```bash
curl -i "http://127.0.0.1:5000/api/courses"
```

La respuesta es una lista JSON:

```json
[
  {
    "id": 1,
    "name": "Python para principiantes",
    "description": "Introducción a Python y Flask",
    "target_date": "2026-12-15",
    "status": "Not Started",
    "created_at": "2026-10-21T21:35:00+00:00"
  }
]
```

Si todavía no hay cursos, la respuesta es:

```json
[]
```

### Obtener un curso específico

- Método: `GET`
- Ruta: `/api/courses/<id>`
- Respuesta exitosa: `200 OK`

Para consultar el curso con ID `1`:

```bash
curl -i "http://127.0.0.1:5000/api/courses/1"
```

Si el curso no existe, la API responde con `404 Not Found`:

```json
{
  "error": "Course not found."
}
```

### Actualizar un curso

- Método: `PUT`
- Ruta: `/api/courses/<id>`
- Respuesta exitosa: `200 OK`

Esta API utiliza `PUT`, por lo que debes enviar todos los campos editables,
incluso si solo deseas cambiar uno.

```bash
curl -i -X PUT "http://127.0.0.1:5000/api/courses/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python y Flask",
    "description": "Creación de aplicaciones REST con Flask",
    "target_date": "2027-01-20",
    "status": "In Progress"
  }'
```

La respuesta contiene el curso actualizado. Los campos `id` y `created_at` no
cambian.

### Eliminar un curso

- Método: `DELETE`
- Ruta: `/api/courses/<id>`
- Respuesta exitosa: `200 OK`

```bash
curl -i -X DELETE "http://127.0.0.1:5000/api/courses/1"
```

Respuesta:

```json
{
  "message": "Course deleted successfully."
}
```

## Códigos de estado principales

- `200 OK`: la consulta, actualización o eliminación fue exitosa.
- `201 Created`: el curso fue creado correctamente.
- `400 Bad Request`: faltan campos o algún dato no es válido.
- `404 Not Found`: el ID solicitado no corresponde a ningún curso.
- `500 Internal Server Error`: ocurrió un problema al leer o escribir el
  archivo JSON.

## Pruebas

Primero inicia la aplicación en una terminal:

```bash
python3 app.py
```

Después abre una segunda terminal y define la URL:

```bash
export BASE_URL="http://127.0.0.1:5000"
```

En Windows PowerShell:

```powershell
$BASE_URL = "http://127.0.0.1:5000"
```

### Flujo de prueba CRUD

Ejecuta los comandos en este orden:

1. Crea un curso:

```bash
curl -i -X POST "$BASE_URL/api/courses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fundamentos de REST",
    "description": "Aprender métodos y respuestas HTTP",
    "target_date": "2026-12-20",
    "status": "Not Started"
  }'
```

2. Copia el `id` devuelto y úsalo en las siguientes solicitudes. Si es `1`,
   consulta el curso así:

```bash
curl -i "$BASE_URL/api/courses/1"
```

3. Actualiza el curso:

```bash
curl -i -X PUT "$BASE_URL/api/courses/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fundamentos de REST",
    "description": "Aprender métodos, rutas y respuestas HTTP",
    "target_date": "2026-12-20",
    "status": "In Progress"
  }'
```

4. Consulta todos los cursos:

```bash
curl -i "$BASE_URL/api/courses"
```

5. Elimina el curso:

```bash
curl -i -X DELETE "$BASE_URL/api/courses/1"
```

6. Comprueba que fue eliminado:

```bash
curl -i "$BASE_URL/api/courses/1"
```

La última solicitud debe responder con `404 Not Found`.

### Probar campos faltantes

```bash
curl -i -X POST "$BASE_URL/api/courses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Curso incompleto"
  }'
```

Respuesta esperada: `400 Bad Request`.

```json
{
  "error": "Missing required fields: description, target_date, status."
}
```

### Probar un estado inválido

```bash
curl -i -X POST "$BASE_URL/api/courses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Curso de prueba",
    "description": "Validación del estado",
    "target_date": "2026-12-20",
    "status": "Pending"
  }'
```

Respuesta esperada: `400 Bad Request`.

### Probar una fecha inválida

```bash
curl -i -X POST "$BASE_URL/api/courses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Curso de prueba",
    "description": "Validación de la fecha",
    "target_date": "20-12-2026",
    "status": "Not Started"
  }'
```

Respuesta esperada: `400 Bad Request`.

### Probar un curso inexistente

```bash
curl -i "$BASE_URL/api/courses/9999"
```

Respuesta esperada: `404 Not Found`.

```json
{
  "error": "Course not found."
}
```

> En Windows PowerShell, `curl` puede ser un alias de otro comando. Si los
> ejemplos no funcionan, reemplaza `curl` por `curl.exe`.

## Estructura del proyecto

```text
CodeCraftHub/
├── app.py          # Aplicación Flask, rutas, validaciones y acceso a datos
├── courses.json    # Archivo donde se almacenan los cursos
└── README.md       # Documentación del proyecto
```

### `app.py`

Contiene:

- La creación de la aplicación Flask.
- Los endpoints de la API.
- Las reglas de validación.
- Las funciones para leer y escribir cursos.
- El manejo de errores.

### `courses.json`

Almacena una lista JSON con todos los cursos. La aplicación crea este archivo
automáticamente con una lista vacía:

```json
[]
```

Para evitar datos dañados, no edites el archivo manualmente mientras el
servidor está ejecutándose.

### `README.md`

Explica cómo instalar, ejecutar, probar y comprender el proyecto.

## Solución de problemas

### `ModuleNotFoundError: No module named 'flask'`

Activa el entorno virtual e instala Flask:

```bash
source .venv/bin/activate
python3 -m pip install Flask
```

### `python3: command not found`

Prueba con:

```bash
python --version
python app.py
```

Si tampoco funciona, instala Python desde
[python.org](https://www.python.org/downloads/).

### El puerto 5000 está ocupado

Inicia Flask en otro puerto:

```bash
flask --app app run --debug --port 5001
```

Después utiliza `http://127.0.0.1:5001` en los comandos `curl`.

### La API responde con `404 Not Found`

Comprueba que:

- El servidor sigue ejecutándose.
- La URL comienza con `/api/courses`.
- Incluiste un ID válido en las operaciones sobre un solo curso.
- Estás utilizando el puerto correcto.

### La API responde con `400 Bad Request`

Comprueba que:

- Enviaste los cuatro campos obligatorios.
- La fecha usa el formato `YYYY-MM-DD`.
- El estado es exactamente `Not Started`, `In Progress` o `Completed`.
- Incluiste el encabezado `Content-Type: application/json`.
- El contenido enviado es JSON válido y usa comillas dobles.

### La API responde con un error de archivo

Comprueba que:

- El proyecto tiene permisos para crear y modificar `courses.json`.
- `courses.json` contiene una lista JSON válida.
- Otro programa no tiene bloqueado el archivo.

Un archivo válido y vacío debe contener:

```json
[]
```

### Los cambios desaparecen

La información se guarda en `courses.json`. Verifica que ejecutas siempre el
mismo archivo `app.py` y que no estás eliminando o reemplazando
`courses.json`.

## Próximos pasos para aprender

Después de comprender este proyecto, puedes intentar:

- Crear una interfaz web que consuma la API.
- Agregar búsquedas y filtros.
- Implementar actualizaciones parciales con `PATCH`.
- Escribir pruebas automáticas con `pytest`.
- Sustituir el archivo JSON por SQLite.
- Añadir autenticación de usuarios.

