from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from models import (
    Participante, ParticipanteCreate, ParticipanteUpdate,
    Acudiente, AcudienteCreate, AcudienteUpdate,
    Sede, SedeCreate, SedeUpdate,
    Usuario, UsuarioCreate, UsuarioUpdate,
    Mensualidad, MensualidadCreate, MensualidadUpdate,
    ApiResponse, DashboardStats
)
from database import (
    db_service,
    validate_sede_exists,
    validate_documento_unico_participante,
    validate_documento_unico_acudiente,
    validate_participante_exists,
    validate_acudiente_exists,
    validate_nombre_sede_unico,
    validate_mensualidad_unica,
    validate_acudiente_belongs_to_participante,
    check_participante_has_dependencies,
    check_acudiente_has_mensualidades,
    check_sede_has_participantes,
    get_participante_with_sede,
    get_acudiente_with_participante,
    get_mensualidad_with_relations,
    get_all_mensualidades_with_relations
)
from services import (
    validate_sede_exists,
    validate_documento_unico_participante,
    validate_documento_unico_acudiente,
    validate_participante_exists,
    validate_acudiente_exists,
    validate_nombre_sede_unico,
    validate_mensualidad_unica,
    validate_acudiente_belongs_to_participante,
    check_participante_has_dependencies,
    check_acudiente_has_mensualidades,
    check_sede_has_participantes,
    get_participante_with_sede,
    get_acudiente_with_participante,
    get_mensualidad_with_relations,
    get_all_mensualidades_with_relations
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
        participantes = []
        for id_participante in participantes_db.keys():
            participante = get_participante_with_sede(id_participante)
            if participante:
                participantes.append(participante)
        
        return ApiResponse(data=participantes, error=None)
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al obtener participantes: {str(e)}"}
        )


@app.get("/api/participantes/{id}", response_model=ApiResponse)
async def get_participante(id: int):
    """Obtiene un participante por ID con información de sede"""
    try:
        participante = get_participante_with_sede(id)
        
        if not participante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Participante no encontrado"
            )
        
        return ApiResponse(data=participante, error=None)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al obtener participante: {str(e)}"}
        )


@app.post("/api/participantes", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def create_participante(participante: ParticipanteCreate):
    """Crea un nuevo participante"""
    try:
        # Validar que la sede exista
        if not validate_sede_exists(participante.id_sede):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La sede con ID {participante.id_sede} no existe"
            )
        
        # Validar que el documento sea único
        if not validate_documento_unico_participante(participante.numero_documento):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un participante con el documento {participante.numero_documento}"
            )
        
        # Generar nuevo ID
        new_id = counters["participantes"] + 1
        counters["participantes"] = new_id
        
        # Crear el participante
        participante_dict = participante.model_dump()
        participante_dict["id"] = new_id
        
        participantes_db[new_id] = participante_dict
        
        # Retornar con información de sede
        participante_created = get_participante_with_sede(new_id)
        
        return ApiResponse(data=participante_created, error=None)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al crear participante: {str(e)}"}
        )


@app.put("/api/participantes/{id}", response_model=ApiResponse)
async def update_participante(id: int, participante_update: ParticipanteUpdate):
    """Actualiza un participante existente"""
    try:
        # Verificar que el participante exista
        if id not in participantes_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Participante no encontrado"
            )
        
        participante_actual = participantes_db[id]
        update_data = participante_update.model_dump(exclude_unset=True)
        
        # Validar sede si se está actualizando
        if "id_sede" in update_data:
            if not validate_sede_exists(update_data["id_sede"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"La sede con ID {update_data['id_sede']} no existe"
                )
        
        # Validar documento único si se está actualizando
        if "numero_documento" in update_data:
            if not validate_documento_unico_participante(
                update_data["numero_documento"], 
                exclude_id=id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un participante con el documento {update_data['numero_documento']}"
                )
        
        # Actualizar campos
        for key, value in update_data.items():
            participante_actual[key] = value
        
        participantes_db[id] = participante_actual
        
        # Retornar con información de sede
        participante_updated = get_participante_with_sede(id)
        
        return ApiResponse(data=participante_updated, error=None)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al actualizar participante: {str(e)}"}
        )


@app.delete("/api/participantes/{id}", response_model=ApiResponse)
async def delete_participante(id: int):
    """Elimina un participante si no tiene dependencias"""
    try:
        # Verificar que el participante exista
        if id not in participantes_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Participante no encontrado"
            )
        
        # Verificar dependencias
        dependencies = check_participante_has_dependencies(id)
        if dependencies["has_dependencies"]:
            details = dependencies["details"]
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"No se puede eliminar el participante porque tiene {details['acudientes']} acudiente(s) y {details['mensualidades']} mensualidad(es) asociadas"
            )
        
        # Eliminar participante
        deleted_participante = participantes_db.pop(id)
        
        return ApiResponse(
            data={"message": "Participante eliminado exitosamente", "id": id},
            error=None
        )
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al eliminar participante: {str(e)}"}
        )


# ============================================================================
# Endpoints de Acudientes
# ============================================================================

@app.get("/api/acudientes", response_model=ApiResponse)
async def get_acudientes():
    """Obtiene la lista de todos los acudientes"""
    try:
        acudientes = []
        for id_acudiente in acudientes_db.keys():
            acudiente = get_acudiente_with_participante(id_acudiente)
            if acudiente:
                acudientes.append(acudiente)
        
        return ApiResponse(data=acudientes, error=None)
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al obtener acudientes: {str(e)}"}
        )


@app.get("/api/acudientes/{id}", response_model=ApiResponse)
async def get_acudiente(id: int):
    """Obtiene un acudiente por ID"""
    try:
        acudiente = get_acudiente_with_participante(id)
        
        if not acudiente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Acudiente no encontrado"
            )
        
        return ApiResponse(data=acudiente, error=None)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al obtener acudiente: {str(e)}"}
        )


@app.get("/api/acudientes/participante/{id_participante}", response_model=ApiResponse)
async def get_acudientes_by_participante(id_participante: int):
    """Obtiene todos los acudientes de un participante específico"""
    try:
        # Verificar que el participante exista
        if not validate_participante_exists(id_participante):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Participante con ID {id_participante} no encontrado"
            )
        
        # Filtrar acudientes por participante
        acudientes = []
        for acudiente in acudientes_db.values():
            if acudiente["id_participante"] == id_participante:
                acudientes.append(acudiente)
        
        return ApiResponse(data=acudientes, error=None)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al obtener acudientes del participante: {str(e)}"}
        )


@app.post("/api/acudientes", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def create_acudiente(acudiente: AcudienteCreate):
    """Crea un nuevo acudiente"""
    try:
        # Validar que el participante exista
        if not validate_participante_exists(acudiente.id_participante):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El participante con ID {acudiente.id_participante} no existe"
            )
        
        # Validar que el documento sea único
        if not validate_documento_unico_acudiente(acudiente.numero_documento):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un acudiente con el documento {acudiente.numero_documento}"
            )
        
        # Generar nuevo ID
        new_id = counters["acudientes"] + 1
        counters["acudientes"] = new_id
        
        # Crear el acudiente
        acudiente_dict = acudiente.model_dump()
        acudiente_dict["id_acudiente"] = new_id
        
        acudientes_db[new_id] = acudiente_dict
        
        # Retornar con información del participante
        acudiente_created = get_acudiente_with_participante(new_id)
        
        return ApiResponse(data=acudiente_created, error=None)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al crear acudiente: {str(e)}"}
        )


@app.put("/api/acudientes/{id}", response_model=ApiResponse)
async def update_acudiente(id: int, acudiente_update: AcudienteUpdate):
    """Actualiza un acudiente existente"""
    try:
        # Verificar que el acudiente exista
        if id not in acudientes_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Acudiente no encontrado"
            )
        
        acudiente_actual = acudientes_db[id]
        update_data = acudiente_update.model_dump(exclude_unset=True)
        
        # Validar participante si se está actualizando
        if "id_participante" in update_data:
            if not validate_participante_exists(update_data["id_participante"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El participante con ID {update_data['id_participante']} no existe"
                )
        
        # Validar documento único si se está actualizando
        if "numero_documento" in update_data:
            if not validate_documento_unico_acudiente(
                update_data["numero_documento"], 
                exclude_id=id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un acudiente con el documento {update_data['numero_documento']}"
                )
        
        # Actualizar campos
        for key, value in update_data.items():
            acudiente_actual[key] = value
        
        acudientes_db[id] = acudiente_actual
        
        # Retornar con información del participante
        acudiente_updated = get_acudiente_with_participante(id)
        
        return ApiResponse(data=acudiente_updated, error=None)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al actualizar acudiente: {str(e)}"}
        )


@app.delete("/api/acudientes/{id}", response_model=ApiResponse)
async def delete_acudiente(id: int):
    """Elimina un acudiente si no tiene dependencias"""
    try:
        # Verificar que el acudiente exista
        if id not in acudientes_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Acudiente no encontrado"
            )
        
        # Verificar dependencias
        dependencies = check_acudiente_has_mensualidades(id)
        if dependencies["has_dependencies"]:
            details = dependencies["details"]
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"No se puede eliminar el acudiente porque tiene {details['mensualidades']} mensualidad(es) asociadas"
            )
        
        # Eliminar acudiente
        deleted_acudiente = acudientes_db.pop(id)
        
        return ApiResponse(
            data={"message": "Acudiente eliminado exitosamente", "id": id},
            error=None
        )
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al eliminar acudiente: {str(e)}"}
        )


# ============================================================================
# Endpoints de Sedes
# ============================================================================

@app.get("/api/sedes", response_model=ApiResponse)
async def get_sedes():
    """Obtiene la lista de todas las sedes"""
    try:
        sedes = list(sedes_db.values())
        return ApiResponse(data=sedes, error=None)
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al obtener sedes: {str(e)}"}
        )


@app.get("/api/sedes/{id}", response_model=ApiResponse)
async def get_sede(id: int):
    """Obtiene una sede por ID"""
    try:
        if id not in sedes_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sede no encontrada"
            )
        
        sede = sedes_db[id]
        return ApiResponse(data=sede, error=None)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al obtener sede: {str(e)}"}
        )


@app.post("/api/sedes", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def create_sede(sede: SedeCreate):
    """Crea una nueva sede"""
    try:
        # Validar que el nombre sea único
        if not validate_nombre_sede_unico(sede.nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una sede con el nombre '{sede.nombre}'"
            )
        
        # Generar nuevo ID
        new_id = counters["sedes"] + 1
        counters["sedes"] = new_id
        
        # Crear la sede
        sede_dict = sede.model_dump()
        sede_dict["id"] = new_id
        
        sedes_db[new_id] = sede_dict
        
        return ApiResponse(data=sede_dict, error=None)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al crear sede: {str(e)}"}
        )


@app.put("/api/sedes/{id}", response_model=ApiResponse)
async def update_sede(id: int, sede_update: SedeUpdate):
    """Actualiza una sede existente"""
    try:
        # Verificar que la sede exista
        if id not in sedes_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sede no encontrada"
            )
        
        sede_actual = sedes_db[id]
        update_data = sede_update.model_dump(exclude_unset=True)
        
        # Validar nombre único si se está actualizando
        if "nombre" in update_data:
            if not validate_nombre_sede_unico(update_data["nombre"], exclude_id=id):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe una sede con el nombre '{update_data['nombre']}'"
                )
        
        # Actualizar campos
        for key, value in update_data.items():
            sede_actual[key] = value
        
        sedes_db[id] = sede_actual
        
        return ApiResponse(data=sede_actual, error=None)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al actualizar sede: {str(e)}"}
        )


@app.delete("/api/sedes/{id}", response_model=ApiResponse)
async def delete_sede(id: int):
    """Elimina una sede si no tiene participantes asociados"""
    try:
        # Verificar que la sede exista
        if id not in sedes_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sede no encontrada"
            )
        
        # Verificar dependencias
        dependencies = check_sede_has_participantes(id)
        if dependencies["has_dependencies"]:
            details = dependencies["details"]
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"No se puede eliminar la sede porque tiene {details['participantes']} participante(s) asociado(s)"
            )
        
        # Eliminar sede
        deleted_sede = sedes_db.pop(id)
        
        return ApiResponse(
            data={"message": "Sede eliminada exitosamente", "id": id},
            error=None
        )
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al eliminar sede: {str(e)}"}
        )


# ============================================================================
# Endpoints de Mensualidades
# ============================================================================

@app.get("/api/mensualidades", response_model=ApiResponse)
async def get_mensualidades():
    """Obtiene la lista de todas las mensualidades con datos relacionados"""
    try:
        mensualidades = get_all_mensualidades_with_relations()
        return ApiResponse(data=mensualidades, error=None)
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al obtener mensualidades: {str(e)}"}
        )


@app.get("/api/mensualidades/{id}", response_model=ApiResponse)
async def get_mensualidad(id: int):
    """Obtiene una mensualidad por ID con datos relacionados"""
    try:
        mensualidad = get_mensualidad_with_relations(id)
        
        if not mensualidad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensualidad no encontrada"
            )
        
        return ApiResponse(data=mensualidad, error=None)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al obtener mensualidad: {str(e)}"}
        )


@app.get("/api/mensualidades/participante/{id_participante}", response_model=ApiResponse)
async def get_mensualidades_by_participante(id_participante: int):
    """Obtiene todas las mensualidades de un participante específico"""
    try:
        # Verificar que el participante exista
        if not validate_participante_exists(id_participante):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Participante con ID {id_participante} no encontrado"
            )
        
        # Filtrar mensualidades por participante
        mensualidades = []
        for mensualidad in mensualidades_db.values():
            if mensualidad["participant_id"] == id_participante:
                mensualidad_with_relations = get_mensualidad_with_relations(mensualidad["id"])
                if mensualidad_with_relations:
                    mensualidades.append(mensualidad_with_relations)
        
        return ApiResponse(data=mensualidades, error=None)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al obtener mensualidades del participante: {str(e)}"}
        )


@app.post("/api/mensualidades", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def create_mensualidad(mensualidad: MensualidadCreate):
    """Crea una nueva mensualidad"""
    try:
        # Validar que el participante exista
        if not validate_participante_exists(mensualidad.participant_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El participante con ID {mensualidad.participant_id} no existe"
            )
        
        # Validar acudiente si se proporciona
        if mensualidad.id_acudiente:
            if not validate_acudiente_exists(mensualidad.id_acudiente):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El acudiente con ID {mensualidad.id_acudiente} no existe"
                )
            
            # Validar que el acudiente pertenezca al participante
            if not validate_acudiente_belongs_to_participante(
                mensualidad.id_acudiente, 
                mensualidad.participant_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El acudiente con ID {mensualidad.id_acudiente} no pertenece al participante con ID {mensualidad.participant_id}"
                )
        
        # Validar que no exista otra mensualidad para el mismo participante, mes y año
        if not validate_mensualidad_unica(
            mensualidad.participant_id,
            mensualidad.mes,
            mensualidad.año
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una mensualidad para el participante {mensualidad.participant_id} en {mensualidad.mes}/{mensualidad.año}"
            )
        
        # Validar fecha de pago si el estado es PAGADA
        if mensualidad.estado == "PAGADA" and not mensualidad.fecha_pago:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de pago es requerida cuando el estado es PAGADA"
            )
        
        # Generar nuevo ID
        new_id = counters["mensualidades"] + 1
        counters["mensualidades"] = new_id
        
        # Crear la mensualidad
        mensualidad_dict = mensualidad.model_dump()
        mensualidad_dict["id"] = new_id
        
        mensualidades_db[new_id] = mensualidad_dict
        
        # Retornar con información completa
        mensualidad_created = get_mensualidad_with_relations(new_id)
        
        return ApiResponse(data=mensualidad_created, error=None)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al crear mensualidad: {str(e)}"}
        )


@app.put("/api/mensualidades/{id}", response_model=ApiResponse)
async def update_mensualidad(id: int, mensualidad_update: MensualidadUpdate):
    """Actualiza una mensualidad existente"""
    try:
        # Verificar que la mensualidad exista
        if id not in mensualidades_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensualidad no encontrada"
            )
        
        mensualidad_actual = mensualidades_db[id]
        update_data = mensualidad_update.model_dump(exclude_unset=True)
        
        # Validar participante si se está actualizando
        if "participant_id" in update_data:
            if not validate_participante_exists(update_data["participant_id"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El participante con ID {update_data['participant_id']} no existe"
                )
        
        # Validar acudiente si se está actualizando
        if "id_acudiente" in update_data and update_data["id_acudiente"]:
            if not validate_acudiente_exists(update_data["id_acudiente"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El acudiente con ID {update_data['id_acudiente']} no existe"
                )
            
            # Obtener el participant_id (actual o actualizado)
            participant_id = update_data.get("participant_id", mensualidad_actual["participant_id"])
            
            # Validar que el acudiente pertenezca al participante
            if not validate_acudiente_belongs_to_participante(
                update_data["id_acudiente"], 
                participant_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El acudiente con ID {update_data['id_acudiente']} no pertenece al participante con ID {participant_id}"
                )
        
        # Validar unicidad si se actualizan mes, año o participante
        if any(key in update_data for key in ["participant_id", "mes", "año"]):
            participant_id = update_data.get("participant_id", mensualidad_actual["participant_id"])
            mes = update_data.get("mes", mensualidad_actual["mes"])
            año = update_data.get("año", mensualidad_actual["año"])
            
            if not validate_mensualidad_unica(participant_id, mes, año, exclude_id=id):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe una mensualidad para el participante {participant_id} en {mes}/{año}"
                )
        
        # Validar fecha de pago si el estado es PAGADA
        estado = update_data.get("estado", mensualidad_actual["estado"])
        fecha_pago = update_data.get("fecha_pago", mensualidad_actual.get("fecha_pago"))
        
        if estado == "PAGADA" and not fecha_pago:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de pago es requerida cuando el estado es PAGADA"
            )
        
        # Actualizar campos
        for key, value in update_data.items():
            mensualidad_actual[key] = value
        
        mensualidades_db[id] = mensualidad_actual
        
        # Retornar con información completa
        mensualidad_updated = get_mensualidad_with_relations(id)
        
        return ApiResponse(data=mensualidad_updated, error=None)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al actualizar mensualidad: {str(e)}"}
        )


@app.delete("/api/mensualidades/{id}", response_model=ApiResponse)
async def delete_mensualidad(id: int):
    """Elimina una mensualidad"""
    try:
        # Verificar que la mensualidad exista
        if id not in mensualidades_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensualidad no encontrada"
            )
        
        # Eliminar mensualidad
        deleted_mensualidad = mensualidades_db.pop(id)
        
        return ApiResponse(
            data={"message": "Mensualidad eliminada exitosamente", "id": id},
            error=None
        )
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al eliminar mensualidad: {str(e)}"}
        )


# ============================================================================
# Endpoints de Usuarios
# ============================================================================

@app.get("/api/usuarios", response_model=ApiResponse)
async def get_usuarios():
    """Obtiene la lista de todos los usuarios"""
    try:
        usuarios = list(usuarios_db.values())
        return ApiResponse(data=usuarios, error=None)
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al obtener usuarios: {str(e)}"}
        )


@app.get("/api/usuarios/{id}", response_model=ApiResponse)
async def get_usuario(id: int):
    """Obtiene un usuario por ID"""
    try:
        if id not in usuarios_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        usuario = usuarios_db[id]
        return ApiResponse(data=usuario, error=None)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al obtener usuario: {str(e)}"}
        )


@app.post("/api/usuarios", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def create_usuario(usuario: UsuarioCreate):
    """Crea un nuevo usuario"""
    try:
        # Verificar que el email no exista
        for existing_usuario in usuarios_db.values():
            if existing_usuario["email"] == usuario.email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un usuario con el email {usuario.email}"
                )

        # Generar nuevo ID
        new_id = counters["usuarios"] + 1
        counters["usuarios"] = new_id

        # Crear el usuario
        usuario_dict = usuario.model_dump()
        usuario_dict["id_usuario"] = new_id

        usuarios_db[new_id] = usuario_dict

        return ApiResponse(data=usuario_dict, error=None)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al crear usuario: {str(e)}"}
        )


@app.put("/api/usuarios/{id}", response_model=ApiResponse)
async def update_usuario(id: int, usuario_update: UsuarioUpdate):
    """Actualiza un usuario existente"""
    try:
        # Verificar que el usuario exista
        if id not in usuarios_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        usuario_actual = usuarios_db[id]
        update_data = usuario_update.model_dump(exclude_unset=True)

        # Verificar email único si se está actualizando
        if "email" in update_data:
            for existing_id, existing_usuario in usuarios_db.items():
                if existing_id != id and existing_usuario["email"] == update_data["email"]:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Ya existe un usuario con el email {update_data['email']}"
                    )

        # Actualizar campos
        for key, value in update_data.items():
            usuario_actual[key] = value

        usuarios_db[id] = usuario_actual

        return ApiResponse(data=usuario_actual, error=None)
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al actualizar usuario: {str(e)}"}
        )


@app.delete("/api/usuarios/{id}", response_model=ApiResponse)
async def delete_usuario(id: int):
    """Elimina un usuario"""
    try:
        # Verificar que el usuario exista
        if id not in usuarios_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        # Eliminar usuario
        deleted_usuario = usuarios_db.pop(id)

        return ApiResponse(
            data={"message": "Usuario eliminado exitosamente", "id": id},
            error=None
        )
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al eliminar usuario: {str(e)}"}
        )


# ============================================================================
# Endpoints de Dashboard y Health
# ============================================================================

@app.get("/api/dashboard/stats", response_model=ApiResponse)
async def get_dashboard_stats():
    """Obtiene estadísticas generales del dashboard"""
    try:
        stats = {
            "participantes": len(participantes_db),
            "mensualidades": len(mensualidades_db),
            "acudientes": len(acudientes_db)
        }
        
        return ApiResponse(data=stats, error=None)
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al obtener estadísticas: {str(e)}"}
        )


@app.get("/api/health", response_model=ApiResponse)
async def health_check():
    """Verifica el estado de la API"""
    try:
        health_status = {
            "status": "healthy",
            "service": "Dashboard API - Corporación Todo por un Alma",
            "version": "1.0.0"
        }
        
        return ApiResponse(data=health_status, error=None)
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error en health check: {str(e)}"}
        )


# ============================================================================
# Dashboard Stats
# ============================================================================

@app.get("/api/dashboard/stats", response_model=ApiResponse)
async def get_dashboard_stats():
    """Obtiene estadísticas generales del dashboard"""
    try:
        stats = DashboardStats(
            participantes=len(participantes_db),
            acudientes=len(acudientes_db),
            mensualidades=len(mensualidades_db)
        )
        return ApiResponse(data=stats.model_dump(), error=None)
    except Exception as e:
        return ApiResponse(
            data=None,
            error={"message": f"Error al obtener estadísticas: {str(e)}"}
        )


# ============================================================================
# Health Check
# ============================================================================

@app.get("/api/health")
async def health_check():
    """Endpoint de health check"""
    return {"status": "ok", "message": "API is running"}
