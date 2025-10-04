"""
Script de pruebas de integración para verificar todos los endpoints de la API.
Este script prueba validaciones, restricciones de integridad y formato de respuestas.
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8081"

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name: str):
    """Imprime el nombre de la prueba"""
    print(f"\n{Colors.BLUE}🧪 {name}{Colors.END}")

def print_success(message: str):
    """Imprime mensaje de éxito"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message: str):
    """Imprime mensaje de error"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message: str):
    """Imprime mensaje de advertencia"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def verify_response_format(response: requests.Response, expect_success: bool = True) -> bool:
    """Verifica que la respuesta tenga el formato correcto {data, error}"""
    try:
        data = response.json()
        if "data" not in data or "error" not in data:
            print_error(f"Formato de respuesta incorrecto. Esperado: {{data, error}}, Recibido: {list(data.keys())}")
            return False
        
        if expect_success:
            if data["error"] is not None:
                print_error(f"Se esperaba éxito pero hay error: {data['error']}")
                return False
            if data["data"] is None:
                print_error("Se esperaba data pero es None")
                return False
        else:
            if data["error"] is None:
                print_error("Se esperaba error pero es None")
                return False
        
        return True
    except json.JSONDecodeError:
        print_error("La respuesta no es JSON válido")
        return False

# ============================================================================
# Tests de Health Check
# ============================================================================

def test_health_check():
    """Prueba el endpoint de health check"""
    print_test("Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print_success("Health check OK")
                return True
            else:
                print_error(f"Health check falló: {data}")
                return False
        else:
            print_error(f"Health check falló con código {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error al conectar con la API: {e}")
        return False

# ============================================================================
# Tests de Sedes
# ============================================================================

def test_get_sedes():
    """Prueba obtener todas las sedes"""
    print_test("GET /api/sedes - Listar todas las sedes")
    
    response = requests.get(f"{BASE_URL}/api/sedes")
    if response.status_code == 200 and verify_response_format(response):
        data = response.json()["data"]
        print_success(f"Se obtuvieron {len(data)} sedes")
        return True
    return False

def test_create_sede_valid():
    """Prueba crear una sede válida"""
    print_test("POST /api/sedes - Crear sede válida")
    
    nueva_sede = {
        "nombre": "Sede Test Temporal",
        "direccion": "Calle Test 123",
        "telefono": "6041234567",
        "capacidad_maxima": 25,
        "estado": "Activa",
        "tipo": "Temporal"
    }
    
    response = requests.post(f"{BASE_URL}/api/sedes", json=nueva_sede)
    if response.status_code == 201 and verify_response_format(response):
        data = response.json()["data"]
        print_success(f"Sede creada con ID: {data['id']}")
        return data["id"]
    return None

def test_create_sede_duplicate_name():
    """Prueba crear una sede con nombre duplicado (debe fallar)"""
    print_test("POST /api/sedes - Crear sede con nombre duplicado (debe fallar)")
    
    sede_duplicada = {
        "nombre": "Bello Principal",  # Ya existe
        "direccion": "Otra dirección",
        "estado": "Activa"
    }
    
    response = requests.post(f"{BASE_URL}/api/sedes", json=sede_duplicada)
    if response.status_code == 409:
        print_success("Validación de nombre duplicado funciona correctamente")
        return True
    else:
        print_error(f"Se esperaba código 409, se obtuvo {response.status_code}")
        return False

def test_delete_sede_with_participantes():
    """Prueba eliminar una sede con participantes (debe fallar)"""
    print_test("DELETE /api/sedes/1 - Eliminar sede con participantes (debe fallar)")
    
    response = requests.delete(f"{BASE_URL}/api/sedes/1")
    if response.status_code == 409:
        print_success("Restricción de integridad funciona: no se puede eliminar sede con participantes")
        return True
    else:
        print_error(f"Se esperaba código 409, se obtuvo {response.status_code}")
        return False

# ============================================================================
# Tests de Participantes
# ============================================================================

def test_get_participantes():
    """Prueba obtener todos los participantes"""
    print_test("GET /api/participantes - Listar todos los participantes")
    
    response = requests.get(f"{BASE_URL}/api/participantes")
    if response.status_code == 200 and verify_response_format(response):
        data = response.json()["data"]
        print_success(f"Se obtuvieron {len(data)} participantes")
        # Verificar que incluye información de sede
        if len(data) > 0 and "sede" in data[0]:
            print_success("Los participantes incluyen información de sede")
        return True
    return False

def test_create_participante_valid():
    """Prueba crear un participante válido"""
    print_test("POST /api/participantes - Crear participante válido")
    
    nuevo_participante = {
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
    }
    
    response = requests.post(f"{BASE_URL}/api/participantes", json=nuevo_participante)
    if response.status_code == 201 and verify_response_format(response):
        data = response.json()["data"]
        print_success(f"Participante creado con ID: {data['id']}")
        return data["id"]
    return None

def test_create_participante_invalid_sede():
    """Prueba crear participante con sede inexistente (debe fallar)"""
    print_test("POST /api/participantes - Crear con sede inexistente (debe fallar)")
    
    participante_invalido = {
        "nombres": "Test",
        "apellidos": "Usuario",
        "tipo_documento": "CC",
        "numero_documento": "8888888888",
        "fecha_nacimiento": "2010-01-01",
        "genero": "MASCULINO",
        "fecha_ingreso": "2024-01-01",
        "estado": "ACTIVO",
        "id_sede": 999  # Sede inexistente
    }
    
    response = requests.post(f"{BASE_URL}/api/participantes", json=participante_invalido)
    if response.status_code == 400:
        print_success("Validación de sede existente funciona correctamente")
        return True
    else:
        print_error(f"Se esperaba código 400, se obtuvo {response.status_code}")
        return False

def test_create_participante_duplicate_document():
    """Prueba crear participante con documento duplicado (debe fallar)"""
    print_test("POST /api/participantes - Crear con documento duplicado (debe fallar)")
    
    participante_duplicado = {
        "nombres": "Test",
        "apellidos": "Usuario",
        "tipo_documento": "CC",
        "numero_documento": "1234567890",  # Ya existe
        "fecha_nacimiento": "2010-01-01",
        "genero": "MASCULINO",
        "fecha_ingreso": "2024-01-01",
        "estado": "ACTIVO",
        "id_sede": 1
    }
    
    response = requests.post(f"{BASE_URL}/api/participantes", json=participante_duplicado)
    if response.status_code == 409:
        print_success("Validación de documento único funciona correctamente")
        return True
    else:
        print_error(f"Se esperaba código 409, se obtuvo {response.status_code}")
        return False

def test_delete_participante_with_dependencies():
    """Prueba eliminar participante con dependencias (debe fallar)"""
    print_test("DELETE /api/participantes/1 - Eliminar con dependencias (debe fallar)")
    
    response = requests.delete(f"{BASE_URL}/api/participantes/1")
    if response.status_code == 409:
        print_success("Restricción de integridad funciona: no se puede eliminar participante con dependencias")
        return True
    else:
        print_error(f"Se esperaba código 409, se obtuvo {response.status_code}")
        return False

# ============================================================================
# Tests de Acudientes
# ============================================================================

def test_get_acudientes():
    """Prueba obtener todos los acudientes"""
    print_test("GET /api/acudientes - Listar todos los acudientes")
    
    response = requests.get(f"{BASE_URL}/api/acudientes")
    if response.status_code == 200 and verify_response_format(response):
        data = response.json()["data"]
        print_success(f"Se obtuvieron {len(data)} acudientes")
        return True
    return False

def test_get_acudientes_by_participante():
    """Prueba obtener acudientes de un participante"""
    print_test("GET /api/acudientes/participante/1 - Acudientes de un participante")
    
    response = requests.get(f"{BASE_URL}/api/acudientes/participante/1")
    if response.status_code == 200 and verify_response_format(response):
        data = response.json()["data"]
        print_success(f"Se obtuvieron {len(data)} acudientes del participante 1")
        return True
    return False

def test_create_acudiente_valid():
    """Prueba crear un acudiente válido"""
    print_test("POST /api/acudientes - Crear acudiente válido")
    
    nuevo_acudiente = {
        "nombres": "Test",
        "apellidos": "Acudiente",
        "tipo_documento": "CC",
        "numero_documento": "7777777777",
        "parentesco": "Padre",
        "telefono": "3007777777",
        "email": "test.acudiente@example.com",
        "direccion": "Calle Test 456",
        "id_participante": 1
    }
    
    response = requests.post(f"{BASE_URL}/api/acudientes", json=nuevo_acudiente)
    if response.status_code == 201 and verify_response_format(response):
        data = response.json()["data"]
        print_success(f"Acudiente creado con ID: {data['id_acudiente']}")
        return data["id_acudiente"]
    return None

def test_create_acudiente_invalid_participante():
    """Prueba crear acudiente con participante inexistente (debe fallar)"""
    print_test("POST /api/acudientes - Crear con participante inexistente (debe fallar)")
    
    acudiente_invalido = {
        "nombres": "Test",
        "apellidos": "Acudiente",
        "tipo_documento": "CC",
        "numero_documento": "6666666666",
        "parentesco": "Padre",
        "telefono": "3006666666",
        "email": "test2@example.com",
        "direccion": "Calle Test",
        "id_participante": 999  # Participante inexistente
    }
    
    response = requests.post(f"{BASE_URL}/api/acudientes", json=acudiente_invalido)
    if response.status_code == 400:
        print_success("Validación de participante existente funciona correctamente")
        return True
    else:
        print_error(f"Se esperaba código 400, se obtuvo {response.status_code}")
        return False

def test_delete_acudiente_with_mensualidades():
    """Prueba eliminar acudiente con mensualidades (debe fallar)"""
    print_test("DELETE /api/acudientes/1 - Eliminar con mensualidades (debe fallar)")
    
    response = requests.delete(f"{BASE_URL}/api/acudientes/1")
    if response.status_code == 409:
        print_success("Restricción de integridad funciona: no se puede eliminar acudiente con mensualidades")
        return True
    else:
        print_error(f"Se esperaba código 409, se obtuvo {response.status_code}")
        return False

# ============================================================================
# Tests de Mensualidades
# ============================================================================

def test_get_mensualidades():
    """Prueba obtener todas las mensualidades"""
    print_test("GET /api/mensualidades - Listar todas las mensualidades")
    
    response = requests.get(f"{BASE_URL}/api/mensualidades")
    if response.status_code == 200 and verify_response_format(response):
        data = response.json()["data"]
        print_success(f"Se obtuvieron {len(data)} mensualidades")
        # Verificar que incluye datos relacionados
        if len(data) > 0:
            if "participant_name" in data[0] and "sede_name" in data[0]:
                print_success("Las mensualidades incluyen datos relacionados (participante, sede)")
        return True
    return False

def test_get_mensualidades_by_participante():
    """Prueba obtener mensualidades de un participante"""
    print_test("GET /api/mensualidades/participante/1 - Mensualidades de un participante")
    
    response = requests.get(f"{BASE_URL}/api/mensualidades/participante/1")
    if response.status_code == 200 and verify_response_format(response):
        data = response.json()["data"]
        print_success(f"Se obtuvieron {len(data)} mensualidades del participante 1")
        return True
    return False

def test_create_mensualidad_valid():
    """Prueba crear una mensualidad válida"""
    print_test("POST /api/mensualidades - Crear mensualidad válida")
    
    nueva_mensualidad = {
        "participant_id": 1,
        "id_acudiente": 1,
        "mes": 3,
        "año": 2024,
        "monto": 50000.0,
        "estado": "PAGADA",
        "metodo_pago": "TRANSFERENCIA",
        "fecha_pago": "2024-03-05",
        "observaciones": "Pago de prueba"
    }
    
    response = requests.post(f"{BASE_URL}/api/mensualidades", json=nueva_mensualidad)
    if response.status_code == 201 and verify_response_format(response):
        data = response.json()["data"]
        print_success(f"Mensualidad creada con ID: {data['id']}")
        return data["id"]
    return None

def test_create_mensualidad_duplicate():
    """Prueba crear mensualidad duplicada (mismo participante, mes, año) - debe fallar"""
    print_test("POST /api/mensualidades - Crear duplicada (debe fallar)")
    
    mensualidad_duplicada = {
        "participant_id": 1,
        "id_acudiente": 1,
        "mes": 1,  # Ya existe para participante 1 en enero 2024
        "año": 2024,
        "monto": 50000.0,
        "estado": "PENDIENTE",
        "metodo_pago": "TRANSFERENCIA"
    }
    
    response = requests.post(f"{BASE_URL}/api/mensualidades", json=mensualidad_duplicada)
    if response.status_code == 409:
        print_success("Validación de mensualidad única funciona correctamente")
        return True
    else:
        print_error(f"Se esperaba código 409, se obtuvo {response.status_code}")
        return False

def test_create_mensualidad_acudiente_wrong_participante():
    """Prueba crear mensualidad con acudiente que no pertenece al participante (debe fallar)"""
    print_test("POST /api/mensualidades - Acudiente no pertenece al participante (debe fallar)")
    
    mensualidad_invalida = {
        "participant_id": 1,
        "id_acudiente": 3,  # Este acudiente pertenece al participante 3, no al 1
        "mes": 4,
        "año": 2024,
        "monto": 50000.0,
        "estado": "PENDIENTE",
        "metodo_pago": "TRANSFERENCIA"
    }
    
    response = requests.post(f"{BASE_URL}/api/mensualidades", json=mensualidad_invalida)
    if response.status_code == 400:
        print_success("Validación de relación acudiente-participante funciona correctamente")
        return True
    else:
        print_error(f"Se esperaba código 400, se obtuvo {response.status_code}")
        return False

def test_create_mensualidad_pagada_sin_fecha():
    """Prueba crear mensualidad PAGADA sin fecha de pago (debe fallar)"""
    print_test("POST /api/mensualidades - PAGADA sin fecha_pago (debe fallar)")
    
    mensualidad_invalida = {
        "participant_id": 2,
        "mes": 5,
        "año": 2024,
        "monto": 50000.0,
        "estado": "PAGADA",
        "metodo_pago": "TRANSFERENCIA"
        # Falta fecha_pago
    }
    
    response = requests.post(f"{BASE_URL}/api/mensualidades", json=mensualidad_invalida)
    if response.status_code == 400:
        print_success("Validación de fecha_pago requerida funciona correctamente")
        return True
    else:
        print_error(f"Se esperaba código 400, se obtuvo {response.status_code}")
        return False

# ============================================================================
# Tests de Dashboard
# ============================================================================

def test_dashboard_stats():
    """Prueba obtener estadísticas del dashboard"""
    print_test("GET /api/dashboard/stats - Estadísticas del dashboard")
    
    response = requests.get(f"{BASE_URL}/api/dashboard/stats")
    if response.status_code == 200 and verify_response_format(response):
        data = response.json()["data"]
        if "participantes" in data and "mensualidades" in data and "acudientes" in data:
            print_success(f"Estadísticas: {data['participantes']} participantes, {data['acudientes']} acudientes, {data['mensualidades']} mensualidades")
            return True
    return False

# ============================================================================
# Tests de Recursos No Encontrados
# ============================================================================

def test_get_participante_not_found():
    """Prueba obtener participante inexistente (debe retornar 404)"""
    print_test("GET /api/participantes/999 - Recurso no encontrado (debe retornar 404)")
    
    response = requests.get(f"{BASE_URL}/api/participantes/999")
    if response.status_code == 404:
        print_success("Manejo de recurso no encontrado funciona correctamente")
        return True
    else:
        print_error(f"Se esperaba código 404, se obtuvo {response.status_code}")
        return False

# ============================================================================
# Función Principal
# ============================================================================

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print(f"\n{Colors.BLUE}{'='*70}")
    print("🚀 INICIANDO PRUEBAS DE INTEGRACIÓN")
    print(f"{'='*70}{Colors.END}\n")
    
    results = {
        "passed": 0,
        "failed": 0,
        "total": 0
    }
    
    tests = [
        # Health Check
        ("Health Check", test_health_check),
        
        # Sedes
        ("Listar Sedes", test_get_sedes),
        ("Crear Sede Válida", test_create_sede_valid),
        ("Crear Sede Duplicada", test_create_sede_duplicate_name),
        ("Eliminar Sede con Participantes", test_delete_sede_with_participantes),
        
        # Participantes
        ("Listar Participantes", test_get_participantes),
        ("Crear Participante Válido", test_create_participante_valid),
        ("Crear Participante con Sede Inexistente", test_create_participante_invalid_sede),
        ("Crear Participante con Documento Duplicado", test_create_participante_duplicate_document),
        ("Eliminar Participante con Dependencias", test_delete_participante_with_dependencies),
        
        # Acudientes
        ("Listar Acudientes", test_get_acudientes),
        ("Listar Acudientes por Participante", test_get_acudientes_by_participante),
        ("Crear Acudiente Válido", test_create_acudiente_valid),
        ("Crear Acudiente con Participante Inexistente", test_create_acudiente_invalid_participante),
        ("Eliminar Acudiente con Mensualidades", test_delete_acudiente_with_mensualidades),
        
        # Mensualidades
        ("Listar Mensualidades", test_get_mensualidades),
        ("Listar Mensualidades por Participante", test_get_mensualidades_by_participante),
        ("Crear Mensualidad Válida", test_create_mensualidad_valid),
        ("Crear Mensualidad Duplicada", test_create_mensualidad_duplicate),
        ("Crear Mensualidad con Acudiente Incorrecto", test_create_mensualidad_acudiente_wrong_participante),
        ("Crear Mensualidad PAGADA sin Fecha", test_create_mensualidad_pagada_sin_fecha),
        
        # Dashboard
        ("Estadísticas del Dashboard", test_dashboard_stats),
        
        # Recursos No Encontrados
        ("Recurso No Encontrado (404)", test_get_participante_not_found),
    ]
    
    for test_name, test_func in tests:
        results["total"] += 1
        try:
            result = test_func()
            if result or result is True:
                results["passed"] += 1
            else:
                results["failed"] += 1
        except Exception as e:
            print_error(f"Excepción en prueba: {e}")
            results["failed"] += 1
    
    # Resumen
    print(f"\n{Colors.BLUE}{'='*70}")
    print("📊 RESUMEN DE PRUEBAS")
    print(f"{'='*70}{Colors.END}\n")
    
    print(f"Total de pruebas: {results['total']}")
    print(f"{Colors.GREEN}✅ Exitosas: {results['passed']}{Colors.END}")
    print(f"{Colors.RED}❌ Fallidas: {results['failed']}{Colors.END}")
    
    success_rate = (results['passed'] / results['total']) * 100 if results['total'] > 0 else 0
    print(f"\nTasa de éxito: {success_rate:.1f}%")
    
    if results['failed'] == 0:
        print(f"\n{Colors.GREEN}🎉 ¡TODAS LAS PRUEBAS PASARON!{Colors.END}\n")
    else:
        print(f"\n{Colors.YELLOW}⚠️  Algunas pruebas fallaron. Revisa los detalles arriba.{Colors.END}\n")

if __name__ == "__main__":
    run_all_tests()
