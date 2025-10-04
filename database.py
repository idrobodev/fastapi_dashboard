"""
Base de datos en memoria para el sistema de dashboard.
Simula una base de datos usando diccionarios de Python.
"""

# ============================================================================
# Contadores para IDs autoincrementales
# ============================================================================

counters = {
    "participantes": 10,
    "acudientes": 8,
    "sedes": 3,
    "mensualidades": 15,
    "usuarios": 2
}

# ============================================================================
# Almacenamiento en memoria
# ============================================================================

participantes_db = {}
acudientes_db = {}
sedes_db = {}
mensualidades_db = {}
usuarios_db = {}

# ============================================================================
# Funciones de inicialización de datos
# ============================================================================

def init_sedes():
    """Inicializa datos de ejemplo para sedes"""
    global sedes_db
    sedes_db = {
        1: {
            "id": 1,
            "nombre": "Bello Principal",
            "direccion": "Calle 50 #45-30, Bello, Antioquia",
            "telefono": "6044567890",
            "capacidad_maxima": 50,
            "estado": "Activa",
            "tipo": "Principal"
        },
        2: {
            "id": 2,
            "nombre": "Bello Campestre",
            "direccion": "Carrera 60 #30-15, Bello, Antioquia",
            "telefono": "6044567891",
            "capacidad_maxima": 30,
            "estado": "Activa",
            "tipo": "Secundaria"
        },
        3: {
            "id": 3,
            "nombre": "Apartadó",
            "direccion": "Avenida Principal #20-10, Apartadó, Antioquia",
            "telefono": "6048281234",
            "capacidad_maxima": 40,
            "estado": "Activa",
            "tipo": "Principal"
        }
    }


def init_participantes():
    """Inicializa datos de ejemplo para participantes"""
    global participantes_db
    participantes_db = {
        1: {
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
            "telefono": "3001234567"
        },
        2: {
            "id": 2,
            "nombres": "María Fernanda",
            "apellidos": "López Martínez",
            "tipo_documento": "TI",
            "numero_documento": "1234567891",
            "fecha_nacimiento": "2012-08-20",
            "genero": "FEMENINO",
            "fecha_ingreso": "2023-02-15",
            "estado": "ACTIVO",
            "id_sede": 1,
            "telefono": "3001234568"
        },
        3: {
            "id": 3,
            "nombres": "Carlos Andrés",
            "apellidos": "Rodríguez Silva",
            "tipo_documento": "CC",
            "numero_documento": "1234567892",
            "fecha_nacimiento": "2011-03-10",
            "genero": "MASCULINO",
            "fecha_ingreso": "2023-03-20",
            "estado": "ACTIVO",
            "id_sede": 2,
            "telefono": "3001234569"
        },
        4: {
            "id": 4,
            "nombres": "Ana Sofía",
            "apellidos": "García Torres",
            "tipo_documento": "TI",
            "numero_documento": "1234567893",
            "fecha_nacimiento": "2013-11-25",
            "genero": "FEMENINO",
            "fecha_ingreso": "2023-04-05",
            "estado": "ACTIVO",
            "id_sede": 2,
            "telefono": "3001234570"
        },
        5: {
            "id": 5,
            "nombres": "Luis Miguel",
            "apellidos": "Hernández Ruiz",
            "tipo_documento": "CC",
            "numero_documento": "1234567894",
            "fecha_nacimiento": "2010-07-18",
            "genero": "MASCULINO",
            "fecha_ingreso": "2023-05-12",
            "estado": "ACTIVO",
            "id_sede": 3,
            "telefono": "3001234571"
        },
        6: {
            "id": 6,
            "nombres": "Laura Valentina",
            "apellidos": "Moreno Castro",
            "tipo_documento": "TI",
            "numero_documento": "1234567895",
            "fecha_nacimiento": "2012-09-30",
            "genero": "FEMENINO",
            "fecha_ingreso": "2023-06-18",
            "estado": "ACTIVO",
            "id_sede": 3,
            "telefono": "3001234572"
        },
        7: {
            "id": 7,
            "nombres": "Diego Alejandro",
            "apellidos": "Ramírez Vargas",
            "tipo_documento": "CC",
            "numero_documento": "1234567896",
            "fecha_nacimiento": "2011-12-05",
            "genero": "MASCULINO",
            "fecha_ingreso": "2023-07-22",
            "estado": "INACTIVO",
            "id_sede": 1,
            "telefono": "3001234573"
        },
        8: {
            "id": 8,
            "nombres": "Camila Andrea",
            "apellidos": "Sánchez Ortiz",
            "tipo_documento": "TI",
            "numero_documento": "1234567897",
            "fecha_nacimiento": "2013-04-14",
            "genero": "FEMENINO",
            "fecha_ingreso": "2023-08-10",
            "estado": "ACTIVO",
            "id_sede": 2,
            "telefono": "3001234574"
        },
        9: {
            "id": 9,
            "nombres": "Santiago",
            "apellidos": "Jiménez Parra",
            "tipo_documento": "CC",
            "numero_documento": "1234567898",
            "fecha_nacimiento": "2010-10-22",
            "genero": "MASCULINO",
            "fecha_ingreso": "2023-09-15",
            "estado": "ACTIVO",
            "id_sede": 3,
            "telefono": "3001234575"
        },
        10: {
            "id": 10,
            "nombres": "Isabella",
            "apellidos": "Cruz Mendoza",
            "tipo_documento": "TI",
            "numero_documento": "1234567899",
            "fecha_nacimiento": "2012-06-08",
            "genero": "FEMENINO",
            "fecha_ingreso": "2023-10-20",
            "estado": "ACTIVO",
            "id_sede": 1,
            "telefono": "3001234576"
        }
    }


def init_acudientes():
    """Inicializa datos de ejemplo para acudientes"""
    global acudientes_db
    acudientes_db = {
        1: {
            "id_acudiente": 1,
            "nombres": "Roberto",
            "apellidos": "Pérez González",
            "tipo_documento": "CC",
            "numero_documento": "9876543210",
            "parentesco": "Padre",
            "telefono": "3101234567",
            "email": "roberto.perez@example.com",
            "direccion": "Calle 45 #30-20, Bello",
            "id_participante": 1
        },
        2: {
            "id_acudiente": 2,
            "nombres": "Patricia",
            "apellidos": "López Ramírez",
            "tipo_documento": "CC",
            "numero_documento": "9876543211",
            "parentesco": "Madre",
            "telefono": "3101234568",
            "email": "patricia.lopez@example.com",
            "direccion": "Carrera 50 #25-15, Bello",
            "id_participante": 2
        },
        3: {
            "id_acudiente": 3,
            "nombres": "Jorge",
            "apellidos": "Rodríguez Pérez",
            "tipo_documento": "CC",
            "numero_documento": "9876543212",
            "parentesco": "Padre",
            "telefono": "3101234569",
            "email": "jorge.rodriguez@example.com",
            "direccion": "Avenida 60 #40-30, Bello",
            "id_participante": 3
        },
        4: {
            "id_acudiente": 4,
            "nombres": "Sandra",
            "apellidos": "García Morales",
            "tipo_documento": "CC",
            "numero_documento": "9876543213",
            "parentesco": "Madre",
            "telefono": "3101234570",
            "email": "sandra.garcia@example.com",
            "direccion": "Calle 55 #35-25, Bello",
            "id_participante": 4
        },
        5: {
            "id_acudiente": 5,
            "nombres": "Fernando",
            "apellidos": "Hernández López",
            "tipo_documento": "CC",
            "numero_documento": "9876543214",
            "parentesco": "Padre",
            "telefono": "3101234571",
            "email": "fernando.hernandez@example.com",
            "direccion": "Carrera 70 #20-10, Apartadó",
            "id_participante": 5
        },
        6: {
            "id_acudiente": 6,
            "nombres": "Gloria",
            "apellidos": "Moreno Díaz",
            "tipo_documento": "CC",
            "numero_documento": "9876543215",
            "parentesco": "Madre",
            "telefono": "3101234572",
            "email": "gloria.moreno@example.com",
            "direccion": "Avenida Principal #15-20, Apartadó",
            "id_participante": 6
        },
        7: {
            "id_acudiente": 7,
            "nombres": "Andrés",
            "apellidos": "Ramírez Castro",
            "tipo_documento": "CC",
            "numero_documento": "9876543216",
            "parentesco": "Tío",
            "telefono": "3101234573",
            "email": "andres.ramirez@example.com",
            "direccion": "Calle 48 #32-18, Bello",
            "id_participante": 7
        },
        8: {
            "id_acudiente": 8,
            "nombres": "Claudia",
            "apellidos": "Sánchez Vargas",
            "tipo_documento": "CC",
            "numero_documento": "9876543217",
            "parentesco": "Madre",
            "telefono": "3101234574",
            "email": "claudia.sanchez@example.com",
            "direccion": "Carrera 65 #28-12, Bello",
            "id_participante": 8
        }
    }


def init_usuarios():
    """Inicializa datos de ejemplo para usuarios"""
    global usuarios_db
    usuarios_db = {
        1: {
            "id_usuario": 1,
            "email": "admin@example.com",
            "rol": "ADMINISTRADOR"
        },
        2: {
            "id_usuario": 2,
            "email": "consulta@example.com",
            "rol": "CONSULTA"
        }
    }


def init_mensualidades():
    """Inicializa datos de ejemplo para mensualidades"""
    global mensualidades_db
    mensualidades_db = {
        1: {
            "id": 1,
            "participant_id": 1,
            "id_acudiente": 1,
            "mes": 1,
            "año": 2024,
            "monto": 50000.0,
            "estado": "PAGADA",
            "metodo_pago": "TRANSFERENCIA",
            "fecha_pago": "2024-01-05",
            "observaciones": "Pago puntual"
        },
        2: {
            "id": 2,
            "participant_id": 1,
            "id_acudiente": 1,
            "mes": 2,
            "año": 2024,
            "monto": 50000.0,
            "estado": "PAGADA",
            "metodo_pago": "EFECTIVO",
            "fecha_pago": "2024-02-03",
            "observaciones": None
        },
        3: {
            "id": 3,
            "participant_id": 2,
            "id_acudiente": 2,
            "mes": 1,
            "año": 2024,
            "monto": 50000.0,
            "estado": "PAGADA",
            "metodo_pago": "TRANSFERENCIA",
            "fecha_pago": "2024-01-08",
            "observaciones": None
        },
        4: {
            "id": 4,
            "participant_id": 2,
            "id_acudiente": 2,
            "mes": 2,
            "año": 2024,
            "monto": 50000.0,
            "estado": "PENDIENTE",
            "metodo_pago": "TRANSFERENCIA",
            "fecha_pago": None,
            "observaciones": "Pendiente de pago"
        },
        5: {
            "id": 5,
            "participant_id": 3,
            "id_acudiente": 3,
            "mes": 1,
            "año": 2024,
            "monto": 45000.0,
            "estado": "PAGADA",
            "metodo_pago": "EFECTIVO",
            "fecha_pago": "2024-01-10",
            "observaciones": None
        },
        6: {
            "id": 6,
            "participant_id": 4,
            "id_acudiente": 4,
            "mes": 1,
            "año": 2024,
            "monto": 50000.0,
            "estado": "PAGADA",
            "metodo_pago": "TRANSFERENCIA",
            "fecha_pago": "2024-01-12",
            "observaciones": None
        },
        7: {
            "id": 7,
            "participant_id": 5,
            "id_acudiente": 5,
            "mes": 1,
            "año": 2024,
            "monto": 55000.0,
            "estado": "PAGADA",
            "metodo_pago": "TRANSFERENCIA",
            "fecha_pago": "2024-01-15",
            "observaciones": None
        },
        8: {
            "id": 8,
            "participant_id": 5,
            "id_acudiente": 5,
            "mes": 2,
            "año": 2024,
            "monto": 55000.0,
            "estado": "PENDIENTE",
            "metodo_pago": "TRANSFERENCIA",
            "fecha_pago": None,
            "observaciones": None
        },
        9: {
            "id": 9,
            "participant_id": 6,
            "id_acudiente": 6,
            "mes": 1,
            "año": 2024,
            "monto": 50000.0,
            "estado": "PAGADA",
            "metodo_pago": "EFECTIVO",
            "fecha_pago": "2024-01-18",
            "observaciones": None
        },
        10: {
            "id": 10,
            "participant_id": 8,
            "id_acudiente": 8,
            "mes": 1,
            "año": 2024,
            "monto": 50000.0,
            "estado": "PAGADA",
            "metodo_pago": "TRANSFERENCIA",
            "fecha_pago": "2024-01-20",
            "observaciones": None
        },
        11: {
            "id": 11,
            "participant_id": 9,
            "id_acudiente": None,
            "mes": 1,
            "año": 2024,
            "monto": 50000.0,
            "estado": "PAGADA",
            "metodo_pago": "EFECTIVO",
            "fecha_pago": "2024-01-22",
            "observaciones": "Pago directo"
        },
        12: {
            "id": 12,
            "participant_id": 10,
            "id_acudiente": None,
            "mes": 1,
            "año": 2024,
            "monto": 50000.0,
            "estado": "PENDIENTE",
            "metodo_pago": "TRANSFERENCIA",
            "fecha_pago": None,
            "observaciones": None
        },
        13: {
            "id": 13,
            "participant_id": 3,
            "id_acudiente": 3,
            "mes": 2,
            "año": 2024,
            "monto": 45000.0,
            "estado": "PENDIENTE",
            "metodo_pago": "EFECTIVO",
            "fecha_pago": None,
            "observaciones": None
        },
        14: {
            "id": 14,
            "participant_id": 4,
            "id_acudiente": 4,
            "mes": 2,
            "año": 2024,
            "monto": 50000.0,
            "estado": "PENDIENTE",
            "metodo_pago": "TRANSFERENCIA",
            "fecha_pago": None,
            "observaciones": None
        },
        15: {
            "id": 15,
            "participant_id": 6,
            "id_acudiente": 6,
            "mes": 2,
            "año": 2024,
            "monto": 50000.0,
            "estado": "PAGADA",
            "metodo_pago": "EFECTIVO",
            "fecha_pago": "2024-02-18",
            "observaciones": None
        }
    }


def initialize_database():
    """Inicializa toda la base de datos con datos de ejemplo"""
    init_sedes()
    init_participantes()
    init_acudientes()
    init_usuarios()
    init_mensualidades()
    print("✅ Base de datos inicializada con datos de ejemplo")
    print(f"   - {len(sedes_db)} sedes")
    print(f"   - {len(participantes_db)} participantes")
    print(f"   - {len(acudientes_db)} acudientes")
    print(f"   - {len(usuarios_db)} usuarios")
    print(f"   - {len(mensualidades_db)} mensualidades")


# Inicializar la base de datos al importar el módulo
initialize_database()
