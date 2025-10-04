# Dashboard API - Corporación Todo por un Alma

API REST desarrollada con FastAPI para gestionar participantes, acudientes, sedes y mensualidades del dashboard de la Corporación Todo por un Alma.

## Características

- ✅ Gestión completa de Participantes
- ✅ Gestión completa de Acudientes
- ✅ Gestión completa de Sedes
- ✅ Gestión completa de Mensualidades
- ✅ Estadísticas del Dashboard
- ✅ Base de datos en memoria con datos de ejemplo
- ✅ Validaciones de integridad referencial
- ✅ Validaciones de datos inválidos
- ✅ Restricciones de integridad referencial
- ✅ CORS configurado para frontend React
- ✅ Formato de respuesta estandarizado (data/error)

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Navegar al directorio del proyecto:
```bash
cd fastapi_dashboard
```

2. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

Iniciar el servidor de desarrollo:

```bash
uvicorn main:app --host 0.0.0.0 --port 8081 --reload
```

La API estará disponible en: `http://localhost:8081`

## Documentación Interactiva

Una vez que el servidor esté ejecutándose, puedes acceder a:

- **Swagger UI (Interactiva)**: http://localhost:8081/docs
- **ReDoc**: http://localhost:8081/redoc

### Usando Swagger UI

Swagger UI te permite probar todos los endpoints de forma interactiva:

1. Abre http://localhost:8081/docs en tu navegador
2. Expande cualquier endpoint haciendo clic en él
3. Haz clic en "Try it out"
4. Completa los parámetros requeridos
5. Haz clic en "Execute"
6. Revisa la respuesta en la sección "Response body"

## Endpoints Principales

### Health Check
- `GET /api/health` - Verificar estado de la API

### Participantes
- `GET /api/participantes` - Listar todos los participantes
- `GET /api/participantes/{id}` - Obtener un participante
- `POST /api/participantes` - Crear un participante
- `PUT /api/participantes/{id}` - Actualizar un participante
- `DELETE /api/participantes/{id}` - Eliminar un participante

### Acudientes
- `GET /api/acudientes` - Listar todos los acudientes
- `GET /api/acudientes/{id}` - Obtener un acudiente
- `GET /api/acudientes/participante/{id_participante}` - Acudientes de un participante
- `POST /api/acudientes` - Crear un acudiente
- `PUT /api/acudientes/{id}` - Actualizar un acudiente
- `DELETE /api/acudientes/{id}` - Eliminar un acudiente

### Sedes
- `GET /api/sedes` - Listar todas las sedes
- `GET /api/sedes/{id}` - Obtener una sede
- `POST /api/sedes` - Crear una sede
- `PUT /api/sedes/{id}` - Actualizar una sede
- `DELETE /api/sedes/{id}` - Eliminar una sede

### Mensualidades
- `GET /api/mensualidades` - Listar todas las mensualidades
- `GET /api/mensualidades/{id}` - Obtener una mensualidad
- `GET /api/mensualidades/participante/{id_participante}` - Mensualidades de un participante
- `POST /api/mensualidades` - Crear una mensualidad
- `PUT /api/mensualidades/{id}` - Actualizar una mensualidad
- `DELETE /api/mensualidades/{id}` - Eliminar una mensualidad

### Dashboard
- `GET /api/dashboard/stats` - Obtener estadísticas generales

## Formato de Respuestas

Todas las respuestas siguen el formato estandarizado `{data, error}`:

**Éxito (200, 201):**
```json
{
  "data": { ... },
  "error": null
}
```

**Error (400, 404, 409, 500):**
```json
{
  "data": null,
  "error": {
    "message": "Descripción del error"
  }
}
```

## Ejemplos de Uso

### 1. Health Check

Verifica que el servidor esté funcionando:

```bash
curl http://localhost:8081/api/health
```

**Respuesta:**
```json
{
  "status": "ok",
  "message": "API is running"
}
```

### 2. Listar Participantes

Obtiene todos los participantes con información de su sede:

```bash
curl http://localhost:8081/api/participantes
```

**Respuesta:**
```json
{
  "data": [
    {
      "id": 1,
      "nombres": "Juan Carlos",
      "apellidos": "Pérez Gómez",
      "tipo_documento": "CC",
      "numero_documento": "1234567890",
      "fecha_nacimiento": "2010-05-15",
      "genero": "MASCULINO",
      "fecha_ingreso": "2023-01-10",
      "estado": "ACTIVO",
      "id_sede": 1,
      "telefono": "3001234567",
      "sede": {
        "id": 1,
        "nombre": "Bello Principal",
        "direccion": "Calle 50 #45-30, Bello, Antioquia",
        "telefono": "6044567890",
        "capacidad_maxima": 50,
        "estado": "Activa",
        "tipo": "Principal"
      }
    }
  ],
  "error": null
}
```

### 3. Crear un Participante

Crea un nuevo participante:

```bash
curl -X POST http://localhost:8081/api/participantes \
  -H "Content-Type: application/json" \
  -d '{
    "nombres": "María",
    "apellidos": "González",
    "tipo_documento": "TI",
    "numero_documento": "1111111111",
    "fecha_nacimiento": "2012-03-15",
    "genero": "FEMENINO",
    "fecha_ingreso": "2024-01-15",
    "estado": "ACTIVO",
    "id_sede": 1,
    "telefono": "3001111111"
  }'
```

**Respuesta exitosa (201):**
```json
{
  "data": {
    "id": 11,
    "nombres": "María",
    "apellidos": "González",
    "tipo_documento": "TI",
    "numero_documento": "1111111111",
    "fecha_nacimiento": "2012-03-15",
    "genero": "FEMENINO",
    "fecha_ingreso": "2024-01-15",
    "estado": "ACTIVO",
    "id_sede": 1,
    "telefono": "3001111111",
    "sede": {
      "id": 1,
      "nombre": "Bello Principal",
      ...
    }
  },
  "error": null
}
```

### 4. Crear un Acudiente

Crea un acudiente asociado a un participante:

```bash
curl -X POST http://localhost:8081/api/acudientes \
  -H "Content-Type: application/json" \
  -d '{
    "nombres": "Pedro",
    "apellidos": "González",
    "tipo_documento": "CC",
    "numero_documento": "2222222222",
    "parentesco": "Padre",
    "telefono": "3002222222",
    "email": "pedro.gonzalez@example.com",
    "direccion": "Calle 10 #20-30",
    "id_participante": 11
  }'
```

### 5. Crear una Mensualidad

Crea una mensualidad para un participante:

```bash
curl -X POST http://localhost:8081/api/mensualidades \
  -H "Content-Type: application/json" \
  -d '{
    "participant_id": 11,
    "id_acudiente": 9,
    "mes": 3,
    "año": 2024,
    "monto": 50000.0,
    "estado": "PAGADA",
    "metodo_pago": "TRANSFERENCIA",
    "fecha_pago": "2024-03-05",
    "observaciones": "Pago puntual"
  }'
```

### 6. Obtener Estadísticas del Dashboard

```bash
curl http://localhost:8081/api/dashboard/stats
```

**Respuesta:**
```json
{
  "data": {
    "participantes": 11,
    "acudientes": 9,
    "mensualidades": 16
  },
  "error": null
}
```

## Validaciones Implementadas

### Validaciones de Datos Inválidos

La API valida automáticamente:

1. **Formatos de fecha**: Deben ser YYYY-MM-DD
   ```json
   {
     "fecha_nacimiento": "2010-13-45"  // ❌ Mes y día inválidos
   }
   ```

2. **Tipos de documento**: Solo acepta CC, TI, CE, PASAPORTE
   ```json
   {
     "tipo_documento": "DNI"  // ❌ Tipo no válido
   }
   ```

3. **Género**: Solo acepta MASCULINO o FEMENINO
   ```json
   {
     "genero": "Otro"  // ❌ Valor no válido
   }
   ```

4. **Estado de participante**: Solo acepta ACTIVO o INACTIVO
   ```json
   {
     "estado": "Suspendido"  // ❌ Estado no válido
   }
   ```

5. **Estado de mensualidad**: Solo acepta PAGADA o PENDIENTE
   ```json
   {
     "estado": "Vencida"  // ❌ Estado no válido
   }
   ```

6. **Método de pago**: Solo acepta TRANSFERENCIA o EFECTIVO
   ```json
   {
     "metodo_pago": "Tarjeta"  // ❌ Método no válido
   }
   ```

7. **Formato de email**: Debe ser un email válido
   ```json
   {
     "email": "correo-invalido"  // ❌ Sin @ ni dominio
   }
   ```

8. **Rangos numéricos**:
   - Mes: 1-12
   - Año: 2020-2030
   - IDs: > 0
   - Monto: > 0

### Restricciones de Integridad Referencial

#### 1. No se puede crear un participante con una sede inexistente

```bash
curl -X POST http://localhost:8081/api/participantes \
  -H "Content-Type: application/json" \
  -d '{
    "nombres": "Test",
    "apellidos": "Usuario",
    "tipo_documento": "CC",
    "numero_documento": "9999999999",
    "fecha_nacimiento": "2010-01-01",
    "genero": "MASCULINO",
    "fecha_ingreso": "2024-01-01",
    "estado": "ACTIVO",
    "id_sede": 999
  }'
```

**Respuesta (400):**
```json
{
  "detail": "La sede con ID 999 no existe"
}
```

#### 2. No se puede crear un acudiente con un participante inexistente

```bash
curl -X POST http://localhost:8081/api/acudientes \
  -H "Content-Type: application/json" \
  -d '{
    "nombres": "Test",
    "apellidos": "Acudiente",
    "tipo_documento": "CC",
    "numero_documento": "8888888888",
    "parentesco": "Padre",
    "telefono": "3008888888",
    "email": "test@example.com",
    "direccion": "Calle Test",
    "id_participante": 999
  }'
```

**Respuesta (400):**
```json
{
  "detail": "El participante con ID 999 no existe"
}
```

#### 3. No se puede crear una mensualidad con acudiente que no pertenece al participante

```bash
curl -X POST http://localhost:8081/api/mensualidades \
  -H "Content-Type: application/json" \
  -d '{
    "participant_id": 1,
    "id_acudiente": 3,
    "mes": 4,
    "año": 2024,
    "monto": 50000.0,
    "estado": "PENDIENTE",
    "metodo_pago": "TRANSFERENCIA"
  }'
```

**Respuesta (400):**
```json
{
  "detail": "El acudiente con ID 3 no pertenece al participante con ID 1"
}
```

#### 4. No se puede crear una mensualidad PAGADA sin fecha de pago

```bash
curl -X POST http://localhost:8081/api/mensualidades \
  -H "Content-Type: application/json" \
  -d '{
    "participant_id": 1,
    "mes": 5,
    "año": 2024,
    "monto": 50000.0,
    "estado": "PAGADA",
    "metodo_pago": "TRANSFERENCIA"
  }'
```

**Respuesta (400):**
```json
{
  "detail": "La fecha de pago es requerida cuando el estado es PAGADA"
}
```

### Restricciones de Unicidad

#### 1. No se puede crear un participante con documento duplicado

```bash
curl -X POST http://localhost:8081/api/participantes \
  -H "Content-Type: application/json" \
  -d '{
    "nombres": "Test",
    "apellidos": "Usuario",
    "tipo_documento": "CC",
    "numero_documento": "1234567890",
    ...
  }'
```

**Respuesta (409):**
```json
{
  "detail": "Ya existe un participante con el documento 1234567890"
}
```

#### 2. No se puede crear una sede con nombre duplicado

```bash
curl -X POST http://localhost:8081/api/sedes \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Bello Principal",
    "direccion": "Otra dirección",
    "estado": "Activa"
  }'
```

**Respuesta (409):**
```json
{
  "detail": "Ya existe una sede con el nombre 'Bello Principal'"
}
```

#### 3. No se puede crear una mensualidad duplicada (mismo participante, mes y año)

```bash
curl -X POST http://localhost:8081/api/mensualidades \
  -H "Content-Type: application/json" \
  -d '{
    "participant_id": 1,
    "mes": 1,
    "año": 2024,
    "monto": 50000.0,
    "estado": "PENDIENTE",
    "metodo_pago": "TRANSFERENCIA"
  }'
```

**Respuesta (409):**
```json
{
  "detail": "Ya existe una mensualidad para el participante 1 en 1/2024"
}
```

### Restricciones de Eliminación con Dependencias

#### 1. No se puede eliminar un participante con acudientes o mensualidades

```bash
curl -X DELETE http://localhost:8081/api/participantes/1
```

**Respuesta (409):**
```json
{
  "detail": "No se puede eliminar el participante porque tiene 1 acudiente(s) y 2 mensualidad(es) asociadas"
}
```

#### 2. No se puede eliminar un acudiente con mensualidades

```bash
curl -X DELETE http://localhost:8081/api/acudientes/1
```

**Respuesta (409):**
```json
{
  "detail": "No se puede eliminar el acudiente porque tiene 2 mensualidad(es) asociadas"
}
```

#### 3. No se puede eliminar una sede con participantes

```bash
curl -X DELETE http://localhost:8081/api/sedes/1
```

**Respuesta (409):**
```json
{
  "detail": "No se puede eliminar la sede porque tiene 4 participante(s) asociado(s)"
}
```

## Pruebas Automatizadas

El proyecto incluye un script de pruebas de integración que verifica todos los endpoints:

```bash
# Asegúrate de que el servidor esté corriendo primero
uvicorn main:app --port 8081 --reload

# En otra terminal, ejecuta las pruebas
python test_integration.py
```

El script prueba:
- ✅ Todos los endpoints GET, POST, PUT, DELETE
- ✅ Validaciones de datos inválidos
- ✅ Restricciones de integridad referencial
- ✅ Restricciones de unicidad
- ✅ Eliminación con dependencias
- ✅ Formato de respuestas (data/error)

## Estructura del Proyecto

```
fastapi_dashboard/
├── main.py              # Aplicación principal y endpoints
├── models.py            # Modelos Pydantic
├── database.py          # Base de datos en memoria
├── services.py          # Lógica de negocio y validaciones
├── requirements.txt     # Dependencias
└── README.md           # Este archivo
```

## Datos de Ejemplo

El sistema incluye datos de ejemplo precargados:
- 3 Sedes (Bello Principal, Bello Campestre, Apartadó)
- 10 Participantes
- 8 Acudientes
- 15 Mensualidades

Los datos se reinician cada vez que se reinicia el servidor.

## Integración con Frontend

Esta API está configurada para trabajar con el frontend React que corre en `http://localhost:3001`. El CORS está habilitado para ese origen.

## Notas Importantes

- Esta API NO maneja autenticación ni autorización (eso es responsabilidad del servicio `fastapi_auth`)
- Los datos se almacenan en memoria y se pierden al reiniciar el servidor
- El puerto por defecto es 8081 (diferente al puerto 8080 de fastapi_auth)

## Desarrollo

Para desarrollo con recarga automática:

```bash
uvicorn main:app --reload --port 8081
```

## Verificación de la Implementación

Para verificar que todos los endpoints funcionan correctamente, consulta la [Guía de Pruebas](TESTING_GUIDE.md).

### Resumen de Verificación

La API ha sido probada y verifica:

✅ **Todos los endpoints funcionan correctamente**
- Health check
- CRUD completo para Participantes, Acudientes, Sedes y Mensualidades
- Endpoints de consulta por relaciones
- Estadísticas del dashboard

✅ **Validaciones de datos inválidos**
- Formatos de fecha (YYYY-MM-DD)
- Tipos de documento (CC, TI, CE, PASAPORTE)
- Género (MASCULINO, FEMENINO)
- Estados (ACTIVO/INACTIVO, PAGADA/PENDIENTE)
- Métodos de pago (TRANSFERENCIA, EFECTIVO)
- Formato de email
- Rangos numéricos (mes 1-12, año 2020-2030, IDs > 0, monto > 0)

✅ **Restricciones de integridad referencial**
- No se puede crear participante con sede inexistente
- No se puede crear acudiente con participante inexistente
- No se puede crear mensualidad con participante inexistente
- No se puede crear mensualidad con acudiente inexistente
- No se puede crear mensualidad con acudiente que no pertenece al participante
- Mensualidad PAGADA requiere fecha_pago

✅ **Restricciones de unicidad**
- Documento único para participantes
- Documento único para acudientes
- Nombre único para sedes
- Mensualidad única por participante/mes/año

✅ **Eliminación con dependencias**
- No se puede eliminar participante con acudientes o mensualidades
- No se puede eliminar acudiente con mensualidades
- No se puede eliminar sede con participantes

✅ **Formato de respuestas estandarizado**
- Todas las respuestas usan formato {data, error}
- Respuestas exitosas: {data: {...}, error: null}
- Respuestas con error: {data: null, error: {message: "..."}}

## Soporte

Para preguntas o problemas, contacta al equipo de desarrollo.
