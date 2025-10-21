from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.orm import Session

from models import (
    Participante, ParticipanteCreate, ParticipanteUpdate,
    Acudiente, AcudienteCreate, AcudienteUpdate,
    Sede, SedeCreate, SedeUpdate,
    Usuario, UsuarioCreate, UsuarioUpdate,
    Mensualidad, MensualidadCreate, MensualidadUpdate,
    ApiResponse, DashboardStats
)
from database_models import (
    db_service, SedeModel, ParticipanteModel, AcudienteModel,
    UsuarioModel, MensualidadModel, SessionLocal
)

# ============================================================================
# Configuración de la aplicación
# ============================================================================

app = FastAPI(
    title="Dashboard API - Corporación Todo por un Alma",
    description="API REST para gestionar participantes, acudientes, sedes y mensualidades",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Funciones auxiliares
# ============================================================================

def get_db():
    """Obtener sesión de base de datos"""
    return SessionLocal()

# ============================================================================
# Health Check Endpoint
# ============================================================================

@app.get("/api/health")
async def health_check():
    """Health check endpoint para verificar que el servidor está funcionando"""
    return {"status": "ok", "message": "API is running"}

# ============================================================================
# Endpoints de Participantes
# ============================================================================

@app.get("/api/participantes", response_model=ApiResponse)
async def get_participantes():
    """Obtiene la lista de todos los participantes con información de sede"""
    try:
        db = get_db()
        participantes = db.query(ParticipanteModel).all()

        result = []
        for p in participantes:
            sede = db.query(SedeModel).filter(SedeModel.id == p.id_sede).first()
            participante_data = {
                "id": p.id,
                "nombres": p.nombres,
                "apellidos": p.apellidos,
                "tipo_documento": p.tipo_documento,
                "numero_documento": p.numero_documento,
                "fecha_nacimiento": p.fecha_nacimiento,
                "genero": p.genero,
                "fecha_ingreso": p.fecha_ingreso,
                "estado": p.estado,
                "id_sede": p.id_sede,
                "telefono": p.telefono,
                "sede": {
                    "id": sede.id,
                    "nombre": sede.nombre,
                    "direccion": sede.direccion
                } if sede else None
            }
            result.append(participante_data)

        return ApiResponse(data=result, error=None)
    finally:
        db.close()

@app.get("/api/participantes/{id}", response_model=ApiResponse)
async def get_participante(id: int):
    """Obtiene un participante por ID con información de sede"""
    try:
        db = get_db()
        participante = db.query(ParticipanteModel).filter(ParticipanteModel.id == id).first()

        if not participante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Participante no encontrado"
            )

        sede = db.query(SedeModel).filter(SedeModel.id == participante.id_sede).first()
        participante_data = {
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
                "direccion": sede.direccion
            } if sede else None
        }

        return ApiResponse(data=participante_data, error=None)
    finally:
        db.close()

@app.post("/api/participantes", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def create_participante(participante: ParticipanteCreate):
    """Crea un nuevo participante"""
    try:
        db = get_db()

        # Validar que la sede exista
        sede = db.query(SedeModel).filter(SedeModel.id == participante.id_sede).first()
        if not sede:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La sede con ID {participante.id_sede} no existe"
            )

        # Validar que el documento sea único
        existing = db.query(ParticipanteModel).filter(
            ParticipanteModel.numero_documento == participante.numero_documento
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un participante con el documento {participante.numero_documento}"
            )

        # Crear el participante
        db_participante = ParticipanteModel(
            nombres=participante.nombres,
            apellidos=participante.apellidos,
            tipo_documento=participante.tipo_documento,
            numero_documento=participante.numero_documento,
            fecha_nacimiento=participante.fecha_nacimiento,
            genero=participante.genero,
            fecha_ingreso=participante.fecha_ingreso,
            estado=participante.estado,
            id_sede=participante.id_sede,
            telefono=participante.telefono
        )

        db.add(db_participante)
        db.commit()
        db.refresh(db_participante)

        # Retornar con información de sede
        participante_data = {
            "id": db_participante.id,
            "nombres": db_participante.nombres,
            "apellidos": db_participante.apellidos,
            "tipo_documento": db_participante.tipo_documento,
            "numero_documento": db_participante.numero_documento,
            "fecha_nacimiento": db_participante.fecha_nacimiento,
            "genero": db_participante.genero,
            "fecha_ingreso": db_participante.fecha_ingreso,
            "estado": db_participante.estado,
            "id_sede": db_participante.id_sede,
            "telefono": db_participante.telefono,
            "sede": {
                "id": sede.id,
                "nombre": sede.nombre,
                "direccion": sede.direccion
            }
        }

        return ApiResponse(data=participante_data, error=None)
    finally:
        db.close()

# ============================================================================
# Dashboard Stats
# ============================================================================

@app.get("/api/dashboard/stats", response_model=ApiResponse)
async def get_dashboard_stats():
    """Obtiene estadísticas generales del dashboard"""
    try:
        db = get_db()
        stats = DashboardStats(
            participantes=db.query(ParticipanteModel).count(),
            acudientes=db.query(AcudienteModel).count(),
            mensualidades=db.query(MensualidadModel).count()
        )
        return ApiResponse(data=stats.model_dump(), error=None)
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)