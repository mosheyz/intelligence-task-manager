from database.agent_db import agents
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from logs.logger_config import logger


class CreateAgent(BaseModel):
    name: str
    specialty: str
    agent_rank: str

class UpdateAgent(BaseModel):
    name: str | None = None
    specialty: str | None = None
    agent_rank: str | None = None


router = APIRouter(prefix="/agents", tags=["agents"])

@router.post("", status_code=201)
def create_agent(data: CreateAgent):
    logger.info("POST /agents called")
    logger.info("start creating agent..")
    
    result = agents.create_agent(data.model_dump())
    if result == "invalid data":
        logger.error("invalid data")
        raise HTTPException(status_code=400, detail="invalid data")
    
    logger.info(f"Agent created successfully: id={result["id"]}")
    return result


@router.get("")
def get_all_agents():
    logger.info("GET /agents called")
    
    result = agents.get_all_agents()
    
    logger.info("getting successfully all agents")
    return result


@router.get("/{id}")
def get_agent_by_id(id: int):
    logger.info(f"GET /agents/{id} called")

    result = agents.get_agent_by_id(id)
    if result == "id not found":
        logger.error(f"agent not found: {id}")
        raise HTTPException(status_code=404, detail=f"agent not found: {id}")
    
    logger.info(f"gettig agent: {id} successully")
    return result

@router.put("/{id}")
def update_agent(id: int, data: UpdateAgent):
    logger.info(f"PUT /agents/{id} called")
    logger.info(f"start updating agent {id}")

    result = agents.update_agent(id, data.model_dump(exclude_unset=True))
    
    if result == "id not found":
        logger.error(f"agent not found: {id}")
        raise HTTPException(status_code=404, detail=f"agent not found: {id}")
    
    if result == "invalid data":
        logger.error("invalid data")
        raise HTTPException(status_code=400, detail="invalid data")
    
    logger.info(f"agent {id} updated successfully")
    return result
    

@router.put("/{id}/deactivate")
def deactivate_agent(id: int):
    logger.info(f"PUT /agents/{id} called")
    logger.info(f"start deactivating agent {id}")

    result = agents.deactivate_agent(id)
    if result == "id not found":
        logger.error(f"agent not found: {id}")
        raise HTTPException(status_code=404, detail=f"agent not found: {id}")
    
    logger.info(f"deactivate agent {id} successfully")
    return {"message": f"deactivate agent {id} successfully"}


@router.get("/{id}/performance")
def get_agent_performance(id: int):
    logger.info("GET /{id}/performance called")

    result = agents.get_agent_performance(id)
    if result == "id not found":
        logger.error(f"agent not found: {id}")
        raise HTTPException(status_code=404, detail=f"agent not found: {id}")
    
    logger.info(f"getting agent {id} performance successfully")
    return result
