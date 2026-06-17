from .base_db import BaseDB
from database.db_connection import db
from .agent_db import agents

valid_fields = ["title", "description", "location", "difficulty", "importance"]
optional_fields = ["status", "assigned_agent_id"]
valid_status = ["NEW", "ASSIGNED", "IN_PROGRESS", "COMPLETED", "CANCELLED"]


class MissionDB(BaseDB):
    def __init__(self):
        super().__init__("missions")

    def create_mission(self, data: dict):
        checked_data = {k:v for k, v in data.items() if k in valid_fields}
        if len(checked_data) < len(data):
            return "invalid data"
        
        for k, v in data.items():
            if k == "importance" or k == "difficulty":
                if data[k] > 10 or data[k] < 1:
                    raise Exception ("invalid data")
                
            if k == "status":
                if data[k] not in valid_status:
                    raise Exception ("invalid status")
                
            if k in optional_fields:
                checked_data[k] = v
        
        checked_data["risk_level"] = self.calculate_risk_level(checked_data["difficulty"], checked_data["importance"])
        
        return self.create(checked_data)

    def calculate_risk_level(self, difficulty, importanse):

        risk_num = difficulty * 2 + importanse
        
        if 9 >= risk_num > 0:
            risk_level = "LOW"
        elif 17 >= risk_num >= 10:
            risk_level = "MEDIUM"
        elif 24 >= risk_num >= 18:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"
        
        return risk_level

    def get_all_missions(self):
        return self.get_all()
    
    def get_mission_by_id(self, id):
        mission = self.get_by_id(id)
        if mission == "id not found":
            return "id not found"
        
        return mission
    
    def update_mission(self, id, data):
        mission = self.get_mission_by_id(id)
        if mission == "id not found":
            return "id not found"
        
        for k, v in data.items():
            if k == "importance" or k == "difficulty":
                if data[k] > 10 or data[k] < 1:
                    raise Exception ("invalid data")
                
            if k == "status":
                if data[k] not in valid_status:
                    raise Exception ("invalid status")
                            
        checked_data = {k:v for k, v in data.items() if k in valid_fields or k in optional_fields}
        for k, v in checked_data.items():

            if k == "status":
                if checked_data[k] == "IN_PROGRESS" and mission[k] != "ASSIGNED":
                    raise Exception ("invalid change")
            
                if checked_data[k] == "FAILED" or checked_data[k] == "COMPLETED" and mission[k] != "IN_PROGRESS":
                    raise Exception ("invalid change")
                
                if checked_data[k] == "CANCELLED" and (mission[k] != "NEW" or mission[k] != "ASSIGNED"):
                    raise Exception ("invalid change")

                
        if not checked_data:
            raise Exception ("invalid data")
        
        return self.update(id, data)
    
    def assign_mission(self, m_id, a_id):
        agent = agents.get_agent_by_id(a_id)
        if agent == "id not found":
            return "agent id not found"
        
        mission = self.get_mission_by_id(m_id)
        if mission == "id not found":
            return "id not found"
        
        if self.count_open_missions_by_agent(a_id) >= 3:
            raise Exception ("agent has more than 3 missions open")
        
        if agent["is_active"] == 0:
            raise Exception ("agent not active")
    
        if mission["risk_level"] == "CRITICAL" and agent["agent_rank"] != "Commander":
            raise Exception ("to low rank for this mission")
        
        if mission["status"] != "NEW":
            raise Exception ("invalid status")
        
        return self.update_mission(m_id, {"assigned_agent_id": a_id, "status": "ASSIGNED"})
        
    def count_open_missions_by_agent(self, id):
        agent = agents.get_agent_by_id(id)
        if agent == "id not found":
            return "agent id not found"
        
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(F"SELECT COUNT(*) AS total FROM {self.table_name} WHERE assigned_agent_id = %s", [id])
            num = cursor.fetchone()
            return num["total"]
    
    def get_open_missions_by_agent(self, id):
        agent = agents.get_agent_by_id(id)
        if agent == "id not found":
            return "agent id not found"
        
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(F"SELECT * FROM {self.table_name} WHERE assigned_agent_id = %s", [id])
            mis = cursor.fetchall()
            if not mis:
                return "no open missions"
            return mis
        
    def count_all_missions(self):
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT COUNT(*) as total FROM {self.table_name}")
            missions = cursor.fetchone["total"]
            return missions
        
    def count_by_status(self, status):
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT status, COUNT(*) as total FROM {self.table_name} WHERE status = %s", [status])
            missions = cursor.fetchall()
            return missions
        
    def count_open_misions(self):
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(F"SELECT COUNT(*) FROM {self.table_name} WHERE status = ASSIGNED")
            num1 = cursor.fetchone()
            cursor.execute(F"SELECT COUNT(*) FROM {self.table_name} WHERE status = IN_PROGRESS")
            num2 = cursor.fetchone()
            return num1 + num2
        
    def count_critical_missions(self):
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT COUNT(*) as total FROM {self.table_name} WHERE risk_level = CRITICAL")
            missions = cursor.fetchone["total"]
            return missions
        
    def get_top_agent(self):
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT MAX(completed_missions) AS top_agent FROM {agents.table_name}")
            top = cursor.fetchone["top_agent"]
            cursor.execute(f"SELECT * FROM {agents.table_name} WHERE completed_missions = {top}")

            agents = cursor.fetchall()

            return agents
        
missions = MissionDB()




        
    
    