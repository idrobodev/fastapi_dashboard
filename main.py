from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from database_models import db_service, SedeModel, ParticipanteModel, AcudienteModel, UsuarioModel, MensualidadModel, SessionLocal
from sqlalchemy.orm import Session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Dashboard API - Corporación Todo por un Alma",
    description="API REST para gestionar participantes, acudientes, sedes y mensualidades",
    version="1.0.0"
)

# Configurar CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "https://todoporunalma.org,https://www.todoporunalma.org").split(",")
logger.info(f"CORS allowed origins: {allowed_origins}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    """Obtener sesión de base de datos"""
    return SessionLocal()

@app.get("/")
async def root():
    """Root endpoint para el dashboard"""
    return {"message": "Dashboard API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint para verificar que el servidor está funcionando"""
    return {"status": "ok", "message": "API is running"}

@app.get("/test")
async def test_endpoint():
    return {"test": "ok"}

@app.get("/acudientes")
async def get_acudientes():
    """Obtiene la lista de todos los acudientes con información de participante"""
    try:
        db = get_db()
        acudientes = db.query(AcudienteModel).all()

        result = []
        for a in acudientes:
            participante = db.query(ParticipanteModel).filter(ParticipanteModel.id == a.id_participante).first()
            acudiente_data = {
                "id_acudiente": a.id_acudiente,
                "nombres": a.nombres,
                "apellidos": a.apellidos,
                "tipo_documento": a.tipo_documento,
                "numero_documento": a.numero_documento,
                "parentesco": a.parentesco,
                "telefono": a.telefono,
                "email": a.email,
                "direccion": a.direccion,
                "id_participante": a.id_participante,
                "participante": {
                    "id": participante.id,
                    "nombres": participante.nombres,
                    "apellidos": participante.apellidos
                } if participante else None
            }
            result.append(acudiente_data)

        return {"data": result, "error": None}
    finally:
        db.close()

@app.get("/sedes")
async def get_sedes():
    """Obtiene la lista de todas las sedes"""
    try:
        db = get_db()
        sedes = db.query(SedeModel).all()

        result = []
        for s in sedes:
            sede_data = {
                "id": s.id,
                "nombre": s.nombre,
                "direccion": s.direccion,
                "telefono": s.telefono,
                "capacidad_maxima": s.capacidad_maxima,
                "estado": s.estado,
                "tipo": s.tipo
            }
            result.append(sede_data)

        return {"data": result, "error": None}
    finally:
        db.close()

@app.get("/usuarios")
async def get_usuarios():
    """Obtiene la lista de todos los usuarios"""
    try:
        db = get_db()
        usuarios = db.query(UsuarioModel).all()

        result = []
        for u in usuarios:
            usuario_data = {
                "id_usuario": u.id_usuario,
                "email": u.email,
                "rol": u.rol
            }
            result.append(usuario_data)

        return {"data": result, "error": None}
    finally:
        db.close()

@app.get("/dashboard/stats")
async def get_dashboard_stats():
   """Obtiene estadísticas generales del dashboard"""
   try:
       db = get_db()
       stats = {
           "participantes": db.query(ParticipanteModel).count(),
           "acudientes": db.query(AcudienteModel).count(),
           "mensualidades": db.query(MensualidadModel).count()
       }
       return {"data": stats, "error": None}
   finally:
       db.close()

@app.get("/participantes")
async def get_participantes(request: Request):
   """Obtiene la lista de todos los participantes con información de sede"""
   logger.info(f"Request to /participantes from origin: {request.headers.get('origin')}")
   logger.info(f"Request headers: {dict(request.headers)}")
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

       logger.info(f"Returning {len(result)} participantes")
       return {"data": result, "error": None}
   except Exception as e:
       logger.error(f"Error in get_participantes: {str(e)}")
       raise
   finally:
       db.close()

@app.get("/mensualidades")
async def get_mensualidades():
    """Obtiene la lista de todas las mensualidades con información de participantes y acudientes"""
    try:
        db = get_db()
        mensualidades = db.query(MensualidadModel).all()

        result = []
        for m in mensualidades:
            # Obtener información del participante
            participante = db.query(ParticipanteModel).filter(ParticipanteModel.id == m.participant_id).first()
            sede = db.query(SedeModel).filter(SedeModel.id == participante.id_sede).first() if participante else None

            # Obtener información del acudiente (si existe)
            acudiente = None
            if m.id_acudiente:
                acudiente = db.query(AcudienteModel).filter(AcudienteModel.id_acudiente == m.id_acudiente).first()

            mensualidad_data = {
                "id": m.id,
                "participant_id": m.participant_id,
                "id_acudiente": m.id_acudiente,
                "mes": m.mes,
                "año": m.año,
                "monto": m.monto,
                "valor": m.monto,  # Alias para compatibilidad con frontend
                "estado": m.estado,
                "status": m.estado,  # Alias para compatibilidad con frontend
                "metodo_pago": m.metodo_pago,
                "fecha_pago": m.fecha_pago,
                "observaciones": m.observaciones,
                # Información del participante
                "participant_name": f"{participante.nombres} {participante.apellidos}" if participante else "N/A",
                "participant_documento": participante.numero_documento if participante else "N/A",
                "sede_id": participante.id_sede if participante else None,
                # Información del acudiente
                "acudiente_name": f"{acudiente.nombres} {acudiente.apellidos}" if acudiente else "N/A",
                "acudiente_documento": acudiente.numero_documento if acudiente else "N/A"
            }
            result.append(mensualidad_data)

        return {"data": result, "error": None}
    finally:
        db.close()

@app.post("/mensualidades")
async def create_mensualidad(mensualidad_data: dict):
    """Crea una nueva mensualidad"""
    try:
        db = get_db()

        # Validar que no exista una mensualidad duplicada para el mismo participante, mes y año
        existing = db.query(MensualidadModel).filter(
            MensualidadModel.participant_id == mensualidad_data["participant_id"],
            MensualidadModel.mes == mensualidad_data["mes"],
            MensualidadModel.año == mensualidad_data["año"]
        ).first()

        if existing:
            return {"data": None, "error": {"message": "Ya existe una mensualidad para este participante en el mes y año especificados"}}

        # Crear nueva mensualidad
        nueva_mensualidad = MensualidadModel(
            participant_id=mensualidad_data["participant_id"],
            id_acudiente=mensualidad_data.get("id_acudiente"),
            mes=mensualidad_data["mes"],
            año=mensualidad_data["año"],
            monto=mensualidad_data["monto"],
            estado=mensualidad_data.get("estado", "PENDIENTE"),
            metodo_pago=mensualidad_data.get("metodo_pago", "TRANSFERENCIA"),
            fecha_pago=mensualidad_data.get("fecha_pago"),
            observaciones=mensualidad_data.get("observaciones")
        )

        db.add(nueva_mensualidad)
        db.commit()
        db.refresh(nueva_mensualidad)

        return {"data": {"id": nueva_mensualidad.id, "message": "Mensualidad creada exitosamente"}, "error": None}
    except Exception as e:
        db.rollback()
        return {"data": None, "error": {"message": f"Error al crear mensualidad: {str(e)}"}}
    finally:
        db.close()

@app.put("/mensualidades/{mensualidad_id}")
async def update_mensualidad(mensualidad_id: int, mensualidad_data: dict):
    """Actualiza una mensualidad existente"""
    try:
        db = get_db()

        # Buscar la mensualidad
        mensualidad = db.query(MensualidadModel).filter(MensualidadModel.id == mensualidad_id).first()
        if not mensualidad:
            return {"data": None, "error": {"message": "Mensualidad no encontrada"}}

        # Validar que no exista una mensualidad duplicada si se cambian los datos únicos
        if ("participant_id" in mensualidad_data or "mes" in mensualidad_data or "año" in mensualidad_data):
            new_participant_id = mensualidad_data.get("participant_id", mensualidad.participant_id)
            new_mes = mensualidad_data.get("mes", mensualidad.mes)
            new_año = mensualidad_data.get("año", mensualidad.año)

            existing = db.query(MensualidadModel).filter(
                MensualidadModel.participant_id == new_participant_id,
                MensualidadModel.mes == new_mes,
                MensualidadModel.año == new_año,
                MensualidadModel.id != mensualidad_id
            ).first()

            if existing:
                return {"data": None, "error": {"message": "Ya existe una mensualidad para este participante en el mes y año especificados"}}

        # Actualizar campos
        for key, value in mensualidad_data.items():
            if hasattr(mensualidad, key):
                setattr(mensualidad, key, value)

        db.commit()

        return {"data": {"id": mensualidad.id, "message": "Mensualidad actualizada exitosamente"}, "error": None}
    except Exception as e:
        db.rollback()
        return {"data": None, "error": {"message": f"Error al actualizar mensualidad: {str(e)}"}}
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)