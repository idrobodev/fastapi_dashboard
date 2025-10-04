from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any, Dict
from datetime import datetime

# ============================================================================
# Modelos de Entidades
# ============================================================================

class Participante(BaseModel):
    id: Optional[int] = None
    nombres: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    tipo_documento: str = Field(..., pattern="^(CC|TI|CE|PASAPORTE)$")
    numero_documento: str = Field(..., min_length=1, max_length=50)
    fecha_nacimiento: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    genero: str = Field(..., pattern="^(MASCULINO|FEMENINO)$")
    fecha_ingreso: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    estado: str = Field(..., pattern="^(ACTIVO|INACTIVO)$")
    id_sede: int = Field(..., gt=0)
    telefono: Optional[str] = Field(None, max_length=20)

    @field_validator('fecha_nacimiento', 'fecha_ingreso')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """Valida que la fecha tenga formato YYYY-MM-DD y sea válida"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError(f'Fecha inválida: {v}. Debe tener formato YYYY-MM-DD')


class ParticipanteCreate(BaseModel):
    nombres: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    tipo_documento: str = Field(..., pattern="^(CC|TI|CE|PASAPORTE)$")
    numero_documento: str = Field(..., min_length=1, max_length=50)
    fecha_nacimiento: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    genero: str = Field(..., pattern="^(MASCULINO|FEMENINO)$")
    fecha_ingreso: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    estado: str = Field(default="ACTIVO", pattern="^(ACTIVO|INACTIVO)$")
    id_sede: int = Field(..., gt=0)
    telefono: Optional[str] = Field(None, max_length=20)

    @field_validator('fecha_nacimiento', 'fecha_ingreso')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError(f'Fecha inválida: {v}. Debe tener formato YYYY-MM-DD')


class ParticipanteUpdate(BaseModel):
    nombres: Optional[str] = Field(None, min_length=1, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=1, max_length=100)
    tipo_documento: Optional[str] = Field(None, pattern="^(CC|TI|CE|PASAPORTE)$")
    numero_documento: Optional[str] = Field(None, min_length=1, max_length=50)
    fecha_nacimiento: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    genero: Optional[str] = Field(None, pattern="^(MASCULINO|FEMENINO)$")
    fecha_ingreso: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    estado: Optional[str] = Field(None, pattern="^(ACTIVO|INACTIVO)$")
    id_sede: Optional[int] = Field(None, gt=0)
    telefono: Optional[str] = Field(None, max_length=20)

    @field_validator('fecha_nacimiento', 'fecha_ingreso')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
                return v
            except ValueError:
                raise ValueError(f'Fecha inválida: {v}. Debe tener formato YYYY-MM-DD')
        return v


class Acudiente(BaseModel):
    id_acudiente: Optional[int] = None
    nombres: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    tipo_documento: str = Field(..., pattern="^(CC|TI|CE|PASAPORTE)$")
    numero_documento: str = Field(..., min_length=1, max_length=50)
    parentesco: str = Field(..., min_length=1, max_length=50)
    telefono: str = Field(..., min_length=1, max_length=20)
    email: str = Field(..., min_length=1, max_length=100)
    direccion: str = Field(..., min_length=1, max_length=200)
    id_participante: int = Field(..., gt=0)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Valida formato básico de email"""
        if '@' not in v or '.' not in v.split('@')[-1]:
            raise ValueError('Email inválido')
        return v.lower()


class AcudienteCreate(BaseModel):
    nombres: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    tipo_documento: str = Field(..., pattern="^(CC|TI|CE|PASAPORTE)$")
    numero_documento: str = Field(..., min_length=1, max_length=50)
    parentesco: str = Field(..., min_length=1, max_length=50)
    telefono: str = Field(..., min_length=1, max_length=20)
    email: str = Field(..., min_length=1, max_length=100)
    direccion: str = Field(..., min_length=1, max_length=200)
    id_participante: int = Field(..., gt=0)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if '@' not in v or '.' not in v.split('@')[-1]:
            raise ValueError('Email inválido')
        return v.lower()


class AcudienteUpdate(BaseModel):
    nombres: Optional[str] = Field(None, min_length=1, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=1, max_length=100)
    tipo_documento: Optional[str] = Field(None, pattern="^(CC|TI|CE|PASAPORTE)$")
    numero_documento: Optional[str] = Field(None, min_length=1, max_length=50)
    parentesco: Optional[str] = Field(None, min_length=1, max_length=50)
    telefono: Optional[str] = Field(None, min_length=1, max_length=20)
    email: Optional[str] = Field(None, min_length=1, max_length=100)
    direccion: Optional[str] = Field(None, min_length=1, max_length=200)
    id_participante: Optional[int] = Field(None, gt=0)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if '@' not in v or '.' not in v.split('@')[-1]:
                raise ValueError('Email inválido')
            return v.lower()
        return v


class Sede(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(..., min_length=1, max_length=100)
    direccion: str = Field(..., min_length=1, max_length=200)
    telefono: Optional[str] = Field(None, max_length=20)
    capacidad_maxima: Optional[int] = Field(None, gt=0)
    estado: str = Field(default="Activa", pattern="^(Activa|Inactiva)$")
    tipo: Optional[str] = Field(default="Principal", pattern="^(Principal|Secundaria|Temporal)$")


class SedeCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    direccion: str = Field(..., min_length=1, max_length=200)
    telefono: Optional[str] = Field(None, max_length=20)
    capacidad_maxima: Optional[int] = Field(None, gt=0)
    estado: str = Field(default="Activa", pattern="^(Activa|Inactiva)$")
    tipo: Optional[str] = Field(default="Principal", pattern="^(Principal|Secundaria|Temporal)$")


class SedeUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    direccion: Optional[str] = Field(None, min_length=1, max_length=200)
    telefono: Optional[str] = Field(None, max_length=20)
    capacidad_maxima: Optional[int] = Field(None, gt=0)
    estado: Optional[str] = Field(None, pattern="^(Activa|Inactiva)$")
    tipo: Optional[str] = Field(None, pattern="^(Principal|Secundaria|Temporal)$")


class Mensualidad(BaseModel):
    id: Optional[int] = None
    participant_id: int = Field(..., gt=0)
    id_acudiente: Optional[int] = Field(None, gt=0)
    mes: int = Field(..., ge=1, le=12)
    año: int = Field(..., ge=2020, le=2030)
    monto: float = Field(..., gt=0)
    estado: str = Field(..., pattern="^(PAGADA|PENDIENTE)$")
    metodo_pago: str = Field(..., pattern="^(TRANSFERENCIA|EFECTIVO)$")
    fecha_pago: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    observaciones: Optional[str] = Field(None, max_length=500)

    @field_validator('fecha_pago')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
                return v
            except ValueError:
                raise ValueError(f'Fecha inválida: {v}. Debe tener formato YYYY-MM-DD')
        return v


class MensualidadCreate(BaseModel):
    participant_id: int = Field(..., gt=0)
    id_acudiente: Optional[int] = Field(None, gt=0)
    mes: int = Field(..., ge=1, le=12)
    año: int = Field(..., ge=2020, le=2030)
    monto: float = Field(..., gt=0)
    estado: str = Field(default="PENDIENTE", pattern="^(PAGADA|PENDIENTE)$")
    metodo_pago: str = Field(default="TRANSFERENCIA", pattern="^(TRANSFERENCIA|EFECTIVO)$")
    fecha_pago: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    observaciones: Optional[str] = Field(None, max_length=500)

    @field_validator('fecha_pago')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
                return v
            except ValueError:
                raise ValueError(f'Fecha inválida: {v}. Debe tener formato YYYY-MM-DD')
        return v


class MensualidadUpdate(BaseModel):
    participant_id: Optional[int] = Field(None, gt=0)
    id_acudiente: Optional[int] = Field(None, gt=0)
    mes: Optional[int] = Field(None, ge=1, le=12)
    año: Optional[int] = Field(None, ge=2020, le=2030)
    monto: Optional[float] = Field(None, gt=0)
    estado: Optional[str] = Field(None, pattern="^(PAGADA|PENDIENTE)$")
    metodo_pago: Optional[str] = Field(None, pattern="^(TRANSFERENCIA|EFECTIVO)$")
    fecha_pago: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    observaciones: Optional[str] = Field(None, max_length=500)

    @field_validator('fecha_pago')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
                return v
            except ValueError:
                raise ValueError(f'Fecha inválida: {v}. Debe tener formato YYYY-MM-DD')
        return v


# ============================================================================
# Modelos de Respuesta
# ============================================================================

class ApiResponse(BaseModel):
    data: Optional[Any] = None
    error: Optional[Dict[str, str]] = None


class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    email: str = Field(..., min_length=1, max_length=100)
    rol: str = Field(..., pattern="^(ADMINISTRADOR|CONSULTA)$")

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Valida formato básico de email"""
        if '@' not in v or '.' not in v.split('@')[-1]:
            raise ValueError('Email inválido')
        return v.lower()


class UsuarioCreate(BaseModel):
    email: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    rol: str = Field(default="CONSULTA", pattern="^(ADMINISTRADOR|CONSULTA)$")

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if '@' not in v or '.' not in v.split('@')[-1]:
            raise ValueError('Email inválido')
        return v.lower()


class UsuarioUpdate(BaseModel):
    email: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    rol: Optional[str] = Field(None, pattern="^(ADMINISTRADOR|CONSULTA)$")

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if '@' not in v or '.' not in v.split('@')[-1]:
                raise ValueError('Email inválido')
            return v.lower()
        return v


class DashboardStats(BaseModel):
    participantes: int
    mensualidades: int
    acudientes: int
