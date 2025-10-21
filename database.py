"""
Base de datos PostgreSQL para el sistema de dashboard.
Usa SQLAlchemy para interactuar con PostgreSQL.
"""

from database_models import (
    get_db_service, SedeModel, ParticipanteModel, AcudienteModel, UsuarioModel, MensualidadModel
)
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

# ============================================================================
# Funciones de compatibilidad con la API existente
# ============================================================================

def get_participante_with_sede(participante_id: int) -> Optional[Dict[str, Any]]:
    """Obtiene un participante con información de sede"""
    db = get_db_service().get_db()
    try:
        participante = db.query(ParticipanteModel).filter(ParticipanteModel.id == participante_id).first()
        if not participante:
            return None

        sede = db.query(SedeModel).filter(SedeModel.id == participante.id_sede).first()

        return {
            "id": participante.id,
            "nombres": participante.nombres,
            "apellidos": participante.apellidos,
            "tipo_documento": participante.tipo_documento,
            "numero_documento": participante.numero_documento,
            "fecha_nacimiento": participante.fecha_nacimiento,
            "genero": participante.genero,
            "fecha_ingreso": participante.fecha_ingreso,
            "estado": participante.estado,
            "id_sede": participante.id_sede,
            "telefono": participante.telefono,
            "sede": {
                "id": sede.id,
                "nombre": sede.nombre,
                "direccion": sede.direccion,
                "telefono": sede.telefono,
                "capacidad_maxima": sede.capacidad_maxima,
                "estado": sede.estado,
                "tipo": sede.tipo
            } if sede else None
        }
    finally:
        db.close()


def get_acudiente_with_participante(acudiente_id: int) -> Optional[Dict[str, Any]]:
    """Obtiene un acudiente con información del participante"""
    db = get_db_service().get_db()
    try:
        acudiente = db.query(AcudienteModel).filter(AcudienteModel.id_acudiente == acudiente_id).first()
        if not acudiente:
            return None

        participante = db.query(ParticipanteModel).filter(ParticipanteModel.id == acudiente.id_participante).first()

        return {
            "id_acudiente": acudiente.id_acudiente,
            "nombres": acudiente.nombres,
            "apellidos": acudiente.apellidos,
            "tipo_documento": acudiente.tipo_documento,
            "numero_documento": acudiente.numero_documento,
            "parentesco": acudiente.parentesco,
            "telefono": acudiente.telefono,
            "email": acudiente.email,
            "direccion": acudiente.direccion,
            "id_participante": acudiente.id_participante,
            "participante": {
                "id": participante.id,
                "nombres": participante.nombres,
                "apellidos": participante.apellidos
            } if participante else None
        }
    finally:
        db.close()


def get_mensualidad_with_relations(mensualidad_id: int) -> Optional[Dict[str, Any]]:
    """Obtiene una mensualidad con datos relacionados"""
    db = get_db_service().get_db()
    try:
        mensualidad = db.query(MensualidadModel).filter(MensualidadModel.id == mensualidad_id).first()
        if not mensualidad:
            return None

        participante = db.query(ParticipanteModel).filter(ParticipanteModel.id == mensualidad.participant_id).first()
        acudiente = None
        if mensualidad.id_acudiente:
            acudiente = db.query(AcudienteModel).filter(AcudienteModel.id_acudiente == mensualidad.id_acudiente).first()

        return {
            "id": mensualidad.id,
            "participant_id": mensualidad.participant_id,
            "id_acudiente": mensualidad.id_acudiente,
            "mes": mensualidad.mes,
            "año": mensualidad.año,
            "monto": mensualidad.monto,
            "estado": mensualidad.estado,
            "metodo_pago": mensualidad.metodo_pago,
            "fecha_pago": mensualidad.fecha_pago,
            "observaciones": mensualidad.observaciones,
            "participante": {
                "id": participante.id,
                "nombres": participante.nombres,
                "apellidos": participante.apellidos
            } if participante else None,
            "acudiente": {
                "id_acudiente": acudiente.id_acudiente,
                "nombres": acudiente.nombres,
                "apellidos": acudiente.apellidos
            } if acudiente else None
        }
    finally:
        db.close()


def get_all_mensualidades_with_relations() -> List[Dict[str, Any]]:
    """Obtiene todas las mensualidades con datos relacionados"""
    db = get_db_service().get_db()
    try:
        mensualidades = db.query(MensualidadModel).all()
        result = []

        for mensualidad in mensualidades:
            participante = db.query(ParticipanteModel).filter(ParticipanteModel.id == mensualidad.participant_id).first()
            acudiente = None
            if mensualidad.id_acudiente:
                acudiente = db.query(AcudienteModel).filter(AcudienteModel.id_acudiente == mensualidad.id_acudiente).first()

            result.append({
                "id": mensualidad.id,
                "participant_id": mensualidad.participant_id,
                "id_acudiente": mensualidad.id_acudiente,
                "mes": mensualidad.mes,
                "año": mensualidad.año,
                "monto": mensualidad.monto,
                "estado": mensualidad.estado,
                "metodo_pago": mensualidad.metodo_pago,
                "fecha_pago": mensualidad.fecha_pago,
                "observaciones": mensualidad.observaciones,
                "participante": {
                    "id": participante.id,
                    "nombres": participante.nombres,
                    "apellidos": participante.apellidos
                } if participante else None,
                "acudiente": {
                    "id_acudiente": acudiente.id_acudiente,
                    "nombres": acudiente.nombres,
                    "apellidos": acudiente.apellidos
                } if acudiente else None
            })

        return result
    finally:
        db.close()


# ============================================================================
# Funciones de validación
# ============================================================================

def validate_sede_exists(sede_id: int) -> bool:
    """Valida que una sede exista"""
    db = get_db_service().get_db()
    try:
        return db.query(SedeModel).filter(SedeModel.id == sede_id).first() is not None
    finally:
        db.close()


def validate_participante_exists(participante_id: int) -> bool:
    """Valida que un participante exista"""
    db = get_db_service().get_db()
    try:
        return db.query(ParticipanteModel).filter(ParticipanteModel.id == participante_id).first() is not None
    finally:
        db.close()


def validate_acudiente_exists(acudiente_id: int) -> bool:
    """Valida que un acudiente exista"""
    db = get_db_service().get_db()
    try:
        return db.query(AcudienteModel).filter(AcudienteModel.id_acudiente == acudiente_id).first() is not None
    finally:
        db.close()


def validate_documento_unico_participante(documento: str, exclude_id: Optional[int] = None) -> bool:
    """Valida que el documento de participante sea único"""
    db = get_db_service().get_db()
    try:
        query = db.query(ParticipanteModel).filter(ParticipanteModel.numero_documento == documento)
        if exclude_id:
            query = query.filter(ParticipanteModel.id != exclude_id)
        return query.first() is None
    finally:
        db.close()


def validate_documento_unico_acudiente(documento: str, exclude_id: Optional[int] = None) -> bool:
    """Valida que el documento de acudiente sea único"""
    db = get_db_service().get_db()
    try:
        query = db.query(AcudienteModel).filter(AcudienteModel.numero_documento == documento)
        if exclude_id:
            query = query.filter(AcudienteModel.id_acudiente != exclude_id)
        return query.first() is None
    finally:
        db.close()


def validate_nombre_sede_unico(nombre: str, exclude_id: Optional[int] = None) -> bool:
    """Valida que el nombre de sede sea único"""
    db = get_db_service().get_db()
    try:
        query = db.query(SedeModel).filter(SedeModel.nombre == nombre)
        if exclude_id:
            query = query.filter(SedeModel.id != exclude_id)
        return query.first() is None
    finally:
        db.close()


def validate_mensualidad_unica(participant_id: int, mes: int, año: int, exclude_id: Optional[int] = None) -> bool:
    """Valida que no exista otra mensualidad para el mismo participante, mes y año"""
    db = get_db_service().get_db()
    try:
        query = db.query(MensualidadModel).filter(
            MensualidadModel.participant_id == participant_id,
            MensualidadModel.mes == mes,
            MensualidadModel.año == año
        )
        if exclude_id:
            query = query.filter(MensualidadModel.id != exclude_id)
        return query.first() is None
    finally:
        db.close()


def validate_acudiente_belongs_to_participante(acudiente_id: int, participante_id: int) -> bool:
    """Valida que el acudiente pertenezca al participante"""
    db = get_db_service().get_db()
    try:
        acudiente = db.query(AcudienteModel).filter(
            AcudienteModel.id_acudiente == acudiente_id,
            AcudienteModel.id_participante == participante_id
        ).first()
        return acudiente is not None
    finally:
        db.close()


def check_participante_has_dependencies(participante_id: int) -> Dict[str, Any]:
    """Verifica si un participante tiene dependencias"""
    db = get_db_service().get_db()
    try:
        acudientes_count = db.query(AcudienteModel).filter(AcudienteModel.id_participante == participante_id).count()
        mensualidades_count = db.query(MensualidadModel).filter(MensualidadModel.participant_id == participante_id).count()

        return {
            "has_dependencies": acudientes_count > 0 or mensualidades_count > 0,
            "details": {
                "acudientes": acudientes_count,
                "mensualidades": mensualidades_count
            }
        }
    finally:
        db.close()


def check_acudiente_has_mensualidades(acudiente_id: int) -> Dict[str, Any]:
    """Verifica si un acudiente tiene mensualidades asociadas"""
    db = get_db_service().get_db()
    try:
        mensualidades_count = db.query(MensualidadModel).filter(MensualidadModel.id_acudiente == acudiente_id).count()

        return {
            "has_dependencies": mensualidades_count > 0,
            "details": {
                "mensualidades": mensualidades_count
            }
        }
    finally:
        db.close()


def check_sede_has_participantes(sede_id: int) -> Dict[str, Any]:
    """Verifica si una sede tiene participantes asociados"""
    db = get_db_service().get_db()
    try:
        participantes_count = db.query(ParticipanteModel).filter(ParticipanteModel.id_sede == sede_id).count()

        return {
            "has_dependencies": participantes_count > 0,
            "details": {
                "participantes": participantes_count
            }
        }
    finally:
        db.close()


# ============================================================================
# Funciones de inicialización (legacy compatibility)
# ============================================================================

def initialize_database():
    """Función de compatibilidad - la inicialización se hace en database_models.py"""
    pass
