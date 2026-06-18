from database.agent_db import agents
from database.mission_db import missions
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from logs.logger_config import logger


class CreateMission(BaseModel):
    title: str
    description: str
    location: str
    difficulty: int
    importance: int

class UpdateMission(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    difficulty: int | None = None
    importance: int | None = None


router = APIRouter(prefix="/missions", tags=["missions"])

@router.post("", status_code=201)
def create_mission(data: CreateMission):
    logger.info("POST /missions called")
    logger.info("start creating mission..")
    
    result = missions.create_mission(data.model_dump())
    if result == "invalid data":
        logger.error("invalid data")
        raise HTTPException(status_code=400, detail="invalid data")
    
    logger.info(f"mission created successfully: id={result["id"]}")
    return result


@router.get("")
def get_all_missions():
    logger.info("GET /missions called")
    
    result = missions.get_all_missions()
    
    logger.info("getting successfully all missions")
    return result


@router.get("/{id}")
def get_mission_by_id(id: int):
    logger.info(f"GET /missions/{id} called")

    result = missions.get_mission_by_id(id)
    if result == "id not found":
        logger.error(f"mission not found: {id}")
        raise HTTPException(status_code=404, detail=f"mission not found: {id}")
    
    logger.info(f"gettig mission: {id} successully")
    return result


@router.put("/{id}/assign/{agent_id}")
def assign_mission(id: int, agent_id: int):
    logger.info(f"PUT /{id}/assign/{agent_id} called")
    logger.info(f"start assigning mission {id} for agent {agent_id}..")

    result = missions.assign_mission(id, agent_id)
    if result == "id not found":
        logger.error(f"mission not found: {id}")
        raise HTTPException(status_code=404, detail=f"mission not found: {id}")
    
    if result == "id not found":
        logger.error(f"agent not found: {agent_id}")
        raise HTTPException(status_code=404, detail=f"agent not found: {agent_id}")
    
    if result == "agent has reached maximum missions":
        logger.error(f"agent {agent_id} has reached maximum missions")
        raise HTTPException(status_code=400, detail=f"agent {id} has reached maximum missions")
    
    if result == "mission not available":
        logger.error(f"mission {id} not available")
        raise HTTPException(status_code=400, detail=f"mission {id} not available")
    
    if result == "agent is not active":
        logger.error(f"agent {agent_id} is not active")
        raise HTTPException(status_code=400, detail=f"agent {agent_id} is not active")
    
    if result == "only Commander can handle critical missions":
        logger.error("only Commander can handle critical missions")
        raise HTTPException(status_code=400, detail="only Commander can handle critical missions")

    logger.info(f"assigning mission {id} for agent {agent_id}")
    return result


@router.put("/{id}/start")
def start_mission(id: int):
    logger.info(f"PUT /{id}/start called")

    result = missions.update_mission_status(id, "IN_PROGRESS")
    if result == "id not found":
        logger.error(f"mission not found: {id}")
        raise HTTPException(status_code=404, detail=f"mission not found: {id}")
    
    if result == "invalid status":
        logger.error("invalid status")
        raise HTTPException(status_code=400, detail="invalid status")
    
    if result == "invalid change":
        logger.error("invalid change")
        raise HTTPException(status_code=400, detail="invalid change")
    
    logger.info(f"start mission {id} successfully")
    return {"message": f"start mission {id} successfully",
            "data": result}


@router.put("/{id}/complete")
def complete_mission(id: int):
    logger.info(f"PUT /{id}/complete called")

    result = missions.update_mission_status(id, "COMPLETED")
    if result == "id not found":
        logger.error(f"mission not found: {id}")
        raise HTTPException(status_code=404, detail=f"mission not found: {id}")
    
    if result == "invalid status":
        logger.error("invalid status")
        raise HTTPException(status_code=400, detail="invalid status")
    
    if result == "invalid change":
        logger.error("invalid change")
        raise HTTPException(status_code=400, detail="invalid change")
    
    logger.info(f"complete mission {id} successfully")
    return {"message": f"complete mission {id} successfully",
            "data": result}


@router.put("/{id}/fail")
def fail_mission(id: int):
    logger.info(f"PUT /{id}/fail called")

    result = missions.update_mission_status(id, "FAILED")
    if result == "id not found":
        logger.error(f"mission not found: {id}")
        raise HTTPException(status_code=404, detail=f"mission not found: {id}")
    
    if result == "invalid status":
        logger.error("invalid status")
        raise HTTPException(status_code=400, detail="invalid status")
    
    if result == "invalid change":
        logger.error("invalid change")
        raise HTTPException(status_code=400, detail="invalid change")
    
    logger.info(f"fail mission {id} successfully")
    return {"message": f"fail mission {id} successfully",
            "data": result}


@router.put("/{id}/cancel")
def cancel_mission(id: int):
    logger.info(f"PUT /{id}/cancel called")

    result = missions.update_mission_status(id, "CANCELLED")
    if result == "id not found":
        logger.error(f"mission not found: {id}")
        raise HTTPException(status_code=404, detail=f"mission not found: {id}")
    
    if result == "invalid status":
        logger.error("invalid status")
        raise HTTPException(status_code=400, detail="invalid status")
    
    if result == "invalid change":
        logger.error("invalid change")
        raise HTTPException(status_code=400, detail="invalid change")
    
    logger.info(f"cancel mission {id} successfully")
    return {"message": f"cancel mission {id} successfully",
            "data": result}