from .base_db import BaseDB
from database.db_connection import db


valid_fields = ["name", "specialty", "agent_rank"]
valid_rank = ["Junior", "Senior", "Commander"]


class AgentDB(BaseDB):
    def __init__(self):
        super().__init__("agents")
    
    def create_agent(self, data: dict):
        checked_data = {k:v for k, v in data.items() if k in valid_fields}
        if len(checked_data) < len(data):
            return "invalid data"
        
        if data["agent_rank"] not in valid_rank:
            return "invalid data"
                
        return self.create(data)


    def get_all_agents(self):
        return self.get_all()


    def get_agent_by_id(self, id):
        agent = self.get_by_id(id)
        if agent == "id not found":
            return "id not found"
        
        return agent


    def update_agent(self, id, data):
        agent = self.get_agent_by_id(id)
        if agent == "id not found":
            return "id not found"
        
        checked_data = {k:v for k, v in data.items() if k in valid_fields}
        if not checked_data:
            return "invalid data"
        
        for k, v in data.items():
            if k == "agent_rank":
                if data[k] not in valid_rank:
                    return "invalid data"
        
        return self.update(id, data)
    

    def deactivate_agent(self, id):
        agent = self.get_by_id(id)
        if agent == "id not found":
            return "id not found"
        
        return self.update(id, {"is_active": 0})
    

    def increment_completed(self, id):
        agent = self.get_agent_by_id(id)
        if agent == "id not found":
            return "id not found"
        
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(f"""
                           UPDATE {self.table_name}
                            SET completed_missions = completed_missions + 1
                            WHERE id = %s
                            """, [id])
            db.connect.commit()

            return self.get_agent_by_id(id)
    

    def increment_failed(self, id):
        agent = self.get_agent_by_id(id)
        if agent == "id not found":
            return "id not found"
        
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(f"""
                           UPDATE {self.table_name}
                            SET failed_missions = failed_missions + 1
                            WHERE id = %s
                           """, [id])
            db.connect.commit()

            return self.get_agent_by_id(id)
        

    def get_agent_performance(self, id):
        agent = self.get_agent_by_id(id)
        if agent == "id not found":
            return "id not found"
        
        total = agent["completed_missions"] + agent["failed_missions"]
        success_rate = 0
        if total != 0:
            success_rate = agent["completed_missions"] / total * 100
        
        agent_performance = {
            "completed": agent["completed_missions"],
            "failed": agent["failed_missions"],
            "total": total,
            "success_rate": success_rate
        }

        return agent_performance
    

    def count_active_agents(self):
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(f"""
                           SELECT COUNT(*) AS active_agents
                           FROM {self.table_name}
                           WHERE is_active = TRUE
                           """)
            active_num = cursor.fetchone()
            return active_num
    
    
agents = AgentDB()
