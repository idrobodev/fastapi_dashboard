# Guía de Pruebas - Dashboard API

Esta guía describe cómo verificar que todos los endpoints de la API funcionen correctamente.

## Requisitos Previos

1. Asegúrate de que el servidor esté corriendo:
```bash
cd fastapi_dashboard
uvicorn main:app --host 0.0.0.0 --port 8081 --reload
```

2. Verifica que el servidor esté activo:
```bash
curl http://localhost:8081/api/health
```

## Método 1: Usar Swagger UI (Recomendado)

La forma más fácil de probar todos los endpoints es usando Swagger UI:

1. Abre tu navegador y ve a: **http://localhost:8081/docs**

2. Verás una interfaz interactiva con todos los endpoints organizados por categorías

3. Para probar cualquier endpoint:
   - Haz clic en el endpoint que quieres probar
   - Haz clic en "Try it out"
   - Completa los parámetros requeridos
   - Haz clic en "Execute"
   - Revisa la respuesta

### Pruebas Recomendadas en Swagger UI

#### A. Verificar Endpoints GET

1. **GET /api/participantes** - Debe retornar lista de participantes con información de sede
2. **GET /api/acudientes** - Debe retornar lista de acudientes
3. **GET /api/sedes** - Debe retornar lista de sedes
4. **GET /api/mensualidades** - Debe retornar lista de mensualidades con datos relacionados
5. **GET /api/dashboard/stats** - Debe retornar contadores

#### B. Probar Validaciones de Datos Inválidos

1. **POST /api/participantes** con fecha inválida:
```json
{
  "nombres": "Test",
  "apellidos": "Usuario",
  "tipo_documento": "CC",
  "numero_documento": "9999999999",
  "fecha_nacimiento": "2010-13-45",
  "genero": "MASCULINO",
  "fecha_ingreso": "2024-01-01",
  "estado": "ACTIVO",
  "id_sede": 1
}
```
**Resultado esperado**: Error 422 (Validation Error)

2. **POST /api/participantes** con tipo_documento inválido:
```json
{
  "nombres": "Test",
  "apellidos": "Usuario",
  "tipo_documento": "DNI",
  "numero_documento": "9999999999",
  "fecha_nacimiento": "2010-01-01",
  "genero": "MASCULINO",
  "fecha_ingreso": "2024-01-01",
  "estado": "ACTIVO",
  "id_sede": 1
}
```
**Resultado esperado**: Error 422 (Validation Error)

3. **POST /api/acudientes** con email inválido:
```json
{
  "nombres": "Test",
  "apellidos": "Acudiente",
  "tipo_documento": "CC",
  "numero_documento": "8888888888",
  "parentesco": "Padre",
  "telefono": "3008888888",
  "email": "correo-sin-arroba",
  "direccion": "Calle Test",
  "id_participante": 1
}
```
**Resultado esperado**: Error 422 (Validation Error)

4. **POST /api/mensualidades** con mes fuera de rango:
```json
{
  "participant_id": 1,
  "mes": 13,
  "año": 2024,
  "monto": 50000.0,
  "estado": "PENDIENTE",
  "metodo_pago": "TRANSFERENCIA"
}
```
**Resultado esperado**: Error 422 (Validation Error)

#### C. Probar Restricciones de Integridad Referencial

1. **POST /api/participantes** con sede inexistente:
```json
{
  "nombres": "Test",
  "apellidos": "Usuario",
  "tipo_documento": "CC",
  "numero_documento": "9999999999",
  "fecha_nacimiento": "2010-01-01",
  "genero": "MASCULINO",
  "fecha_ingreso": "2024-01-01",
  "estado": "ACTIVO",
  "id_sede": 999
}
```
**Resultado esperado**: Error 400 - "La sede con ID 999 no existe"

2. **POST /api/acudientes** con participante inexistente:
```json
{
  "nombres": "Test",
  "apellidos": "Acudiente",
  "tipo_documento": "CC",
  "numero_documento": "8888888888",
  "parentesco": "Padre",
  "telefono": "3008888888",
  "email": "test@example.com",
  "direccion": "Calle Test",
  "id_participante": 999
}
```
**Resultado esperado**: Error 400 - "El participante con ID 999 no existe"

3. **POST /api/mensualidades** con acudiente que no pertenece al participante:
```json
{
  "participant_id": 1,
  "id_acudiente": 3,
  "mes": 4,
  "año": 2024,
  "monto": 50000.0,
  "estado": "PENDIENTE",
  "metodo_pago": "TRANSFERENCIA"
}
```
**Resultado esperado**: Error 400 - "El acudiente con ID 3 no pertenece al participante con ID 1"

4. **POST /api/mensualidades** PAGADA sin fecha_pago:
```json
{
  "participant_id": 1,
  "mes": 5,
  "año": 2024,
  "monto": 50000.0,
  "estado": "PAGADA",
  "metodo_pago": "TRANSFERENCIA"
}
```
**Resultado esperado**: Error 400 - "La fecha de pago es requerida cuando el estado es PAGADA"

#### D. Probar Eliminación con Dependencias

1. **DELETE /api/participantes/1**
   - **Resultado esperado**: Error 409 - "No se puede eliminar el participante porque tiene X acudiente(s) y Y mensualidad(es) asociadas"

2. **DELETE /api/acudientes/1**
   - **Resultado esperado**: Error 409 - "No se puede eliminar el acudiente porque tiene X mensualidad(es) asociadas"

3. **DELETE /api/sedes/1**
   - **Resultado esperado**: Error 409 - "No se puede eliminar la sede porque tiene X participante(s) asociado(s)"

#### E. Verificar Formato de Respuestas

Todos los endpoints deben retornar el formato `{data, error}`:

**Respuesta exitosa:**
```json
{
  "data": { ... },
  "error": null
}
```

**Respuesta con error:**
```json
{
  "data": null,
  "error": {
    "message": "Descripción del error"
  }
}
```

## Método 2: Usar el Script de Pruebas Automatizado

El proyecto incluye un script Python que ejecuta todas las pruebas automáticamente:

```bash
# Asegúrate de que el servidor esté corriendo
uvicorn main:app --port 8081 --reload

# En otra terminal, ejecuta el script de pruebas
python test_integration.py
```

El script verificará:
- ✅ Health check
- ✅ Todos los endpoints GET
- ✅ Creación de recursos válidos
- ✅ Validaciones de datos inválidos
- ✅ Restricciones de integridad referencial
- ✅ Restricciones de unicidad
- ✅ Eliminación con dependencias
- ✅ Formato de respuestas

## Método 3: Usar cURL

También puedes probar los endpoints usando cURL desde la terminal:

### Ejemplos de cURL

```bash
# Health check
curl http://localhost:8081/api/health

# Listar participantes
curl http://localhost:8081/api/participantes

# Obtener un participante específico
curl http://localhost:8081/api/participantes/1

# Crear un participante
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
    "id_sede": 1,
    "telefono": "3009999999"
  }'

# Actualizar un participante
curl -X PUT http://localhost:8081/api/participantes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "telefono": "3001111111"
  }'

# Eliminar un participante (sin dependencias)
curl -X DELETE http://localhost:8081/api/participantes/11

# Obtener estadísticas
curl http://localhost:8081/api/dashboard/stats
```

## Checklist de Verificación

Usa este checklist para asegurarte de que todo funciona correctamente:

### Endpoints Básicos
- [ ] GET /api/health retorna status "ok"
- [ ] GET /api/participantes retorna lista con información de sede
- [ ] GET /api/acudientes retorna lista de acudientes
- [ ] GET /api/sedes retorna lista de sedes
- [ ] GET /api/mensualidades retorna lista con datos relacionados
- [ ] GET /api/dashboard/stats retorna contadores correctos

### Validaciones de Datos Inválidos
- [ ] Fecha inválida (formato incorrecto) retorna error 422
- [ ] Tipo de documento inválido retorna error 422
- [ ] Género inválido retorna error 422
- [ ] Email inválido retorna error 422
- [ ] Mes fuera de rango (< 1 o > 12) retorna error 422
- [ ] Año fuera de rango retorna error 422
- [ ] Monto negativo o cero retorna error 422

### Restricciones de Integridad Referencial
- [ ] Crear participante con sede inexistente retorna error 400
- [ ] Crear acudiente con participante inexistente retorna error 400
- [ ] Crear mensualidad con participante inexistente retorna error 400
- [ ] Crear mensualidad con acudiente inexistente retorna error 400
- [ ] Crear mensualidad con acudiente que no pertenece al participante retorna error 400
- [ ] Crear mensualidad PAGADA sin fecha_pago retorna error 400

### Restricciones de Unicidad
- [ ] Crear participante con documento duplicado retorna error 409
- [ ] Crear acudiente con documento duplicado retorna error 409
- [ ] Crear sede con nombre duplicado retorna error 409
- [ ] Crear mensualidad duplicada (mismo participante, mes, año) retorna error 409

### Eliminación con Dependencias
- [ ] Eliminar participante con acudientes retorna error 409
- [ ] Eliminar participante con mensualidades retorna error 409
- [ ] Eliminar acudiente con mensualidades retorna error 409
- [ ] Eliminar sede con participantes retorna error 409

### Formato de Respuestas
- [ ] Todas las respuestas exitosas tienen formato {data: ..., error: null}
- [ ] Todas las respuestas con error tienen formato {data: null, error: {...}}

## Resultados Esperados

Si todas las pruebas pasan correctamente, deberías ver:

- ✅ Todos los endpoints GET retornan datos correctamente
- ✅ Las validaciones de Pydantic funcionan (errores 422)
- ✅ Las validaciones de negocio funcionan (errores 400)
- ✅ Las restricciones de unicidad funcionan (errores 409)
- ✅ Las restricciones de eliminación funcionan (errores 409)
- ✅ Todas las respuestas tienen el formato correcto {data, error}
- ✅ Los datos relacionados se incluyen correctamente (sede en participantes, etc.)

## Notas Importantes

1. **Base de datos en memoria**: Los datos se reinician cada vez que reinicias el servidor
2. **IDs autoincrementales**: Los IDs comienzan en 11 para participantes, 9 para acudientes, etc.
3. **CORS**: Configurado para http://localhost:3001
4. **Puerto**: La API corre en el puerto 8081 (no 8080)

## Solución de Problemas

### El servidor no responde
```bash
# Verifica que el servidor esté corriendo
ps aux | grep uvicorn

# Si no está corriendo, inícialo
uvicorn main:app --port 8081 --reload
```

### Error de conexión en el script de pruebas
```bash
# Verifica que el puerto sea el correcto (8081)
curl http://localhost:8081/api/health

# Si el puerto es diferente, edita BASE_URL en test_integration.py
```

### Los datos no son los esperados
```bash
# Reinicia el servidor para resetear los datos de ejemplo
# Ctrl+C para detener
# Luego vuelve a iniciar
uvicorn main:app --port 8081 --reload
```
