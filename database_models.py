from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey, Enum, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from typing import Optional
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Nalufis28++@corporacion-corporaciondb-4z75xa:5432/corporacion_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ============================================================================
# Modelos SQLAlchemy
# ============================================================================

class SedeModel(Base):
    """Modelo SQLAlchemy para Sede"""
    __tablename__ = "sedes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    direccion = Column(String(200), nullable=False)
    telefono = Column(String(20), nullable=True)
    capacidad_maxima = Column(Integer, nullable=True)
    estado = Column(String(20), nullable=False, default="Activa")
    tipo = Column(String(20), nullable=True, default="Principal")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    participantes = relationship("ParticipanteModel", back_populates="sede")


class ParticipanteModel(Base):
    """Modelo SQLAlchemy para Participante"""
    __tablename__ = "participantes"

    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    tipo_documento = Column(String(20), nullable=False)
    numero_documento = Column(String(50), nullable=False, unique=True)
    fecha_nacimiento = Column(String(10), nullable=False)
    genero = Column(String(20), nullable=False)
    fecha_ingreso = Column(String(10), nullable=False)
    estado = Column(String(20), nullable=False, default="ACTIVO")
    id_sede = Column(Integer, ForeignKey("sedes.id"), nullable=False)
    telefono = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    sede = relationship("SedeModel", back_populates="participantes")
    acudientes = relationship("AcudienteModel", back_populates="participante")
    mensualidades = relationship("MensualidadModel", back_populates="participante")


class AcudienteModel(Base):
    """Modelo SQLAlchemy para Acudiente"""
    __tablename__ = "acudientes"

    id_acudiente = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    tipo_documento = Column(String(20), nullable=False)
    numero_documento = Column(String(50), nullable=False, unique=True)
    parentesco = Column(String(50), nullable=False)
    telefono = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    direccion = Column(String(200), nullable=False)
    id_participante = Column(Integer, ForeignKey("participantes.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    participante = relationship("ParticipanteModel", back_populates="acudientes")
    mensualidades = relationship("MensualidadModel", back_populates="acudiente")


class UsuarioModel(Base):
    """Modelo SQLAlchemy para Usuario"""
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, unique=True)
    rol = Column(String(20), nullable=False, default="CONSULTA")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MensualidadModel(Base):
    """Modelo SQLAlchemy para Mensualidad"""
    __tablename__ = "mensualidades"

    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(Integer, ForeignKey("participantes.id"), nullable=False)
    id_acudiente = Column(Integer, ForeignKey("acudientes.id_acudiente"), nullable=True)
    mes = Column(Integer, nullable=False)
    año = Column(Integer, nullable=False)
    monto = Column(Float, nullable=False)
    estado = Column(String(20), nullable=False, default="PENDIENTE")
    metodo_pago = Column(String(20), nullable=False, default="TRANSFERENCIA")
    fecha_pago = Column(String(10), nullable=True)
    observaciones = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    participante = relationship("ParticipanteModel", back_populates="mensualidades")
    acudiente = relationship("AcudienteModel", back_populates="mensualidades")

    # Índice único compuesto para evitar duplicados
    __table_args__ = (
        {'schema': None},
    )


# ============================================================================
# Servicio de Base de Datos
# ============================================================================

class DatabaseService:
    """Servicio de base de datos usando SQLAlchemy"""

    def __init__(self):
        # Solo inicializar datos en desarrollo local
        if os.getenv("ENVIRONMENT") != "production":
            Base.metadata.create_all(bind=engine)
            self.initialize_default_data()

    def get_db(self) -> Session:
        """Obtener sesión de base de datos"""
        return SessionLocal()

    def initialize_default_data(self):
        """Inicializar datos por defecto"""
        db = self.get_db()
        try:
            # Verificar si ya existen datos
            if db.query(SedeModel).count() > 0:
                return

            # Crear sedes por defecto
            sedes_data = [
                {
                    "id": 1,
                    "nombre": "Bello Principal",
                    "direccion": "Calle 50 #45-30, Bello, Antioquia",
                    "telefono": "6044567890",
                    "capacidad_maxima": 50,
                    "estado": "Activa",
                    "tipo": "Principal"
                },
                {
                    "id": 2,
                    "nombre": "Bello Campestre",
                    "direccion": "Carrera 60 #30-15, Bello, Antioquia",
                    "telefono": "6044567891",
                    "capacidad_maxima": 30,
                    "estado": "Activa",
                    "tipo": "Secundaria"
                },
                {
                    "id": 3,
                    "nombre": "Apartadó",
                    "direccion": "Avenida Principal #20-10, Apartadó, Antioquia",
                    "telefono": "6048281234",
                    "capacidad_maxima": 40,
                    "estado": "Activa",
                    "tipo": "Principal"
                }
            ]

            for sede_data in sedes_data:
                sede = SedeModel(**sede_data)
                db.add(sede)

            # Crear usuarios por defecto
            usuarios_data = [
                {"id_usuario": 1, "email": "admin@example.com", "rol": "ADMINISTRADOR"},
                {"id_usuario": 2, "email": "consulta@example.com", "rol": "CONSULTA"}
            ]

            for usuario_data in usuarios_data:
                usuario = UsuarioModel(**usuario_data)
                db.add(usuario)

            db.commit()
            print("✅ Datos por defecto inicializados en PostgreSQL")

        except Exception as e:
            db.rollback()
            print(f"❌ Error inicializando datos por defecto: {e}")
        finally:
            db.close()

# Instancia global del servicio de base de datos (lazy initialization)
db_service = None

def get_db_service():
    """Obtener instancia del servicio de base de datos (lazy initialization)"""
    global db_service
    if db_service is None:
        db_service = DatabaseService()
    return db_service