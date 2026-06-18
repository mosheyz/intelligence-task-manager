from database.agent_db import agents
from database.mission_db import missions
from fastapi import APIRouter
from logs.logger_config import logger


router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/summary")
def get_summary():
    logger.info("GET /reports/summary called")

    result = {"active_agents_count": agents.count_active_agents(),
              "total_missions": missions.count_all_missions(),
              "open_missions": missions.count_open_missions(),
              "completed_missions": missions.count_by_status("COMPLETED"),
              "failed_missions": missions.count_by_status("FAILED"),
              "critical_missions": missions.count_critical_missions()}
    
    logger.info("succesfully get summary")
    return {"message": "succesfully get summary",
            "data": result}


@router.get("/missions-by-status")
def get_by_status():
    logger.info("GET /reports/missions-by-status called")
    result =  missions.count_group_by_status()

    logger.info("succesfully get missions by status")
    return {"message": "succesfully get missions by status",
            "data": result}

@router.get("/top-agent")
def get_top_agent():
    logger.info("GET /reports/top-agent")
    result =  missions.get_top_agent()

    logger.info("succesfully get top member")
    return {"message": "succesfully get top member",
            "data": result}