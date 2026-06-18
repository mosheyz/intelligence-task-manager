from fastapi import FastAPI
from routers.agent_routes import router as agents_router
from routers.mission_routes import router as missions_router
from routers.report_routes import router as reports_router
from contextlib import asynccontextmanager
from logs.logger_config import logger
from database.db_connection import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("connection start")

    try:
        yield

    finally:
        db.conn.close()
        logger.info("connection close")


app = FastAPI(lifespan=lifespan)

app.include_router(agents_router)
app.include_router(missions_router)
app.include_router(reports_router)