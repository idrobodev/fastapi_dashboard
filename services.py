"""
Servicios y validaciones de lógica de negocio.
Contiene funciones para validar datos y verificar integridad referencial.
"""

from typing import Optional, Dict, Any
from datetime import datetime
import re
from database import (
    participantes_db, 
    acudientes_db, 
    sedes_db, 
    mensualidades_db
)

# ============================================================================
# Validaciones de Formato
# ============================================================================

def validate_email_format(email: str) -> bool:
    """
    Valida que el email tenga un formato válido.
    
    Args:
        email: Email a validar
        
    Returns:
        True si el formato es válido, False en caso contrario
    """
    if not email or '@' not in email:
        return False
    
    # Patrón básico de email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_fecha_format(fecha: str) -> bool:
    """
    Valida que la fecha tenga formato YYYY-MM-DD y sea una fecha válida.
    
    Args:
        fecha: Fecha en formato string
        
    Returns:
        True si el formato es válido, False en caso contrario
    """
    try:
        datetime.strptime(fecha, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False


# ============================================================================
# Validaciones de Existencia
# ============================================================================

def validate_sede_exists(id_sede: int) -> bool:
    """
    Valida que una sede exista en la base de datos.
    
    Args:
        id_sede: ID de la sede a validar
        
    Returns:
        True si la sede existe, False en caso contrario
    """
    return id_sede in sedes_db


def validate_participante_exists(id_participante: int) -> bool:
    """
    Valida que un participante exista en la base de datos.
    
    Args:
        id_participante: ID del participante a validar
        
    Returns:
        True si el participante existe, False en caso contrario
    """
    return id_participante in participantes_db


def validate_acudiente_exists(id_acudiente: int) -> bool:
    """
    Valida que un acudiente exista en la base de datos.
    
    Args:
        id_acudiente: ID del acudiente a validar
        
    Returns:
        True si el acudiente existe, False en caso contrario
    """
    return id_acudiente in acudientes_db


# ============================================================================
# Validaciones de Unicidad
# ============================================================================

def validate_documento_unico_participante(
    numero_documento: str, 
    exclude_id: Optional[int] = None
) -> bool:
    """
    Valida que el número de documento de un participante sea único.
    
    Args:
        numero_documento: Número de documento a validar
        exclude_id: ID del participante a excluir de la validación (para updates)
        
    Returns:
        True si el documento es único, False si ya existe
    """
    for id_part, participante in participantes_db.items():
        if participante["numero_documento"] == numero_documento:
            if exclude_id is None or id_part != exclude_id:
                return False
    return True


def validate_documento_unico_acudiente(
    numero_documento: str, 
    exclude_id: Optional[int] = None
) -> bool:
    """
    Valida que el número de documento de un acudiente sea único.
    
    Args:
        numero_documento: Número de documento a validar
        exclude_id: ID del acudiente a excluir de la validación (para updates)
        
    Returns:
        True si el documento es único, False si ya existe
    """
    for id_acud, acudiente in acudientes_db.items():
        if acudiente["numero_documento"] == numero_documento:
            if exclude_id is None or id_acud != exclude_id:
                return False
    return True


def validate_nombre_sede_unico(
    nombre: str, 
    exclude_id: Optional[int] = None
) -> bool:
    """
    Valida que el nombre de una sede sea único.
    
    Args:
        nombre: Nombre de la sede a validar
        exclude_id: ID de la sede a excluir de la validación (para updates)
        
    Returns:
        True si el nombre es único, False si ya existe
    """
    nombre_lower = nombre.lower().strip()
    for id_sede, sede in sedes_db.items():
        if sede["nombre"].lower().strip() == nombre_lower:
            if exclude_id is None or id_sede != exclude_id:
                return False
    return True


def validate_mensualidad_unica(
    participant_id: int,
    mes: int,
    año: int,
    exclude_id: Optional[int] = None
) -> bool:
    """
    Valida que no exista otra mensualidad para el mismo participante, mes y año.
    
    Args:
        participant_id: ID del participante
        mes: Mes de la mensualidad
        año: Año de la mensualidad
        exclude_id: ID de la mensualidad a excluir (para updates)
        
    Returns:
        True si es única, False si ya existe
    """
    for id_mens, mensualidad in mensualidades_db.items():
        if (mensualidad["participant_id"] == participant_id and
            mensualidad["mes"] == mes and
            mensualidad["año"] == año):
            if exclude_id is None or id_mens != exclude_id:
                return False
    return True


# ============================================================================
# Validaciones de Relaciones
# ============================================================================

def validate_acudiente_belongs_to_participante(
    id_acudiente: int, 
    id_participante: int
) -> bool:
    """
    Valida que un acudiente pertenezca a un participante específico.
    
    Args:
        id_acudiente: ID del acudiente
        id_participante: ID del participante
        
    Returns:
        True si el acudiente pertenece al participante, False en caso contrario
    """
    if id_acudiente not in acudientes_db:
        return False
    
    acudiente = acudientes_db[id_acudiente]
    return acudiente["id_participante"] == id_participante


# ============================================================================
# Verificación de Dependencias
# ============================================================================

def check_participante_has_dependencies(id_participante: int) -> Dict[str, Any]:
    """
    Verifica si un participante tiene dependencias (acudientes o mensualidades).
    
    Args:
        id_participante: ID del participante a verificar
        
    Returns:
        Dict con has_dependencies (bool) y details (dict con conteos)
    """
    acudientes_count = sum(
        1 for acudiente in acudientes_db.values()
        if acudiente["id_participante"] == id_participante
    )
    
    mensualidades_count = sum(
        1 for mensualidad in mensualidades_db.values()
        if mensualidad["participant_id"] == id_participante
    )
    
    has_dependencies = acudientes_count > 0 or mensualidades_count > 0
    
    return {
        "has_dependencies": has_dependencies,
        "details": {
            "acudientes": acudientes_count,
            "mensualidades": mensualidades_count
        }
    }


def check_sede_has_participantes(id_sede: int) -> Dict[str, Any]:
    """
    Verifica si una sede tiene participantes asociados.
    
    Args:
        id_sede: ID de la sede a verificar
        
    Returns:
        Dict con has_dependencies (bool) y details (dict con conteo)
    """
    participantes_count = sum(
        1 for participante in participantes_db.values()
        if participante["id_sede"] == id_sede
    )
    
    has_dependencies = participantes_count > 0
    
    return {
        "has_dependencies": has_dependencies,
        "details": {
            "participantes": participantes_count
        }
    }


def check_acudiente_has_mensualidades(id_acudiente: int) -> Dict[str, Any]:
    """
    Verifica si un acudiente tiene mensualidades asociadas.
    
    Args:
        id_acudiente: ID del acudiente a verificar
        
    Returns:
        Dict con has_dependencies (bool) y details (dict con conteo)
    """
    mensualidades_count = sum(
        1 for mensualidad in mensualidades_db.values()
        if mensualidad.get("id_acudiente") == id_acudiente
    )
    
    has_dependencies = mensualidades_count > 0
    
    return {
        "has_dependencies": has_dependencies,
        "details": {
            "mensualidades": mensualidades_count
        }
    }


# ============================================================================
# Funciones de Enriquecimiento de Datos
# ============================================================================

def get_participante_with_sede(id_participante: int) -> Optional[Dict[str, Any]]:
    """
    Obtiene un participante con información de su sede.
    
    Args:
        id_participante: ID del participante
        
    Returns:
        Dict con datos del participante y sede, o None si no existe
    """
    if id_participante not in participantes_db:
        return None
    
    participante = participantes_db[id_participante].copy()
    id_sede = participante["id_sede"]
    
    if id_sede in sedes_db:
        participante["sede"] = sedes_db[id_sede].copy()
    else:
        participante["sede"] = None
    
    return participante


def get_acudiente_with_participante(id_acudiente: int) -> Optional[Dict[str, Any]]:
    """
    Obtiene un acudiente con información de su participante.
    
    Args:
        id_acudiente: ID del acudiente
        
    Returns:
        Dict con datos del acudiente y participante, o None si no existe
    """
    if id_acudiente not in acudientes_db:
        return None
    
    acudiente = acudientes_db[id_acudiente].copy()
    id_participante = acudiente["id_participante"]
    
    if id_participante in participantes_db:
        acudiente["participante"] = participantes_db[id_participante].copy()
    else:
        acudiente["participante"] = None
    
    return acudiente


def get_mensualidad_with_relations(id_mensualidad: int) -> Optional[Dict[str, Any]]:
    """
    Obtiene una mensualidad con información de participante, acudiente y sede.
    
    Args:
        id_mensualidad: ID de la mensualidad
        
    Returns:
        Dict con datos completos de la mensualidad, o None si no existe
    """
    if id_mensualidad not in mensualidades_db:
        return None
    
    mensualidad = mensualidades_db[id_mensualidad].copy()
    
    # Agregar información del participante
    participant_id = mensualidad["participant_id"]
    if participant_id in participantes_db:
        participante = participantes_db[participant_id]
        mensualidad["participant_name"] = f"{participante['nombres']} {participante['apellidos']}"
        mensualidad["participant_documento"] = participante["numero_documento"]

        # Agregar información de la sede
        id_sede = participante["id_sede"]
        if id_sede in sedes_db:
            mensualidad["sede_id"] = id_sede
            mensualidad["sede_name"] = sedes_db[id_sede]["nombre"]
    else:
        mensualidad["participant_name"] = "N/A"
        mensualidad["participant_documento"] = "N/A"
        mensualidad["sede_id"] = None
        mensualidad["sede_name"] = "N/A"

    # Agregar información del acudiente si existe
    id_acudiente = mensualidad.get("id_acudiente")
    if id_acudiente and id_acudiente in acudientes_db:
        acudiente = acudientes_db[id_acudiente]
        mensualidad["acudiente_name"] = f"{acudiente['nombres']} {acudiente['apellidos']}"
        mensualidad["acudiente_documento"] = acudiente["numero_documento"]
    else:
        mensualidad["acudiente_name"] = None
        mensualidad["acudiente_documento"] = None
    
    # Renombrar campos para compatibilidad con frontend
    mensualidad["valor"] = mensualidad["monto"]
    mensualidad["status"] = mensualidad["estado"]
    
    return mensualidad


def get_all_mensualidades_with_relations() -> list:
    """
    Obtiene todas las mensualidades con información completa.
    
    Returns:
        Lista de mensualidades con datos relacionados
    """
    mensualidades = []
    for id_mensualidad in mensualidades_db.keys():
        mensualidad = get_mensualidad_with_relations(id_mensualidad)
        if mensualidad:
            mensualidades.append(mensualidad)
    return mensualidades
