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
            if k in ("importance", "difficulty"):
                if data[k] > 10 or data[k] < 1:
                    raise Exception ("invalid data")
        
        checked_data["risk_level"] = self.calculate_risk_level(checked_data["difficulty"], checked_data["importance"])
        
        return self.create(checked_data)


    def calculate_risk_level(self, difficulty, importance):

        risk_num = (int(difficulty) * 2) + int(importance)
        
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
            if k in ("importance", "difficulty"):
                if data[k] > 10 or data[k] < 1:
                    raise Exception ("invalid data")
                            
        checked_data = {k:v for k, v in data.items() if k in valid_fields}
        
        if not checked_data:
            raise Exception ("invalid data")
        
        importance = checked_data.get("importance", mission["importance"])
        difficulty = checked_data.get("difficulty", mission["difficulty"])
        checked_data["risk_level"] = self.calculate_risk_level(difficulty, importance)
        
        if checked_data["risk_level"] == "CRITICAL" and agents.get_agent_by_id(mission["assigned_agent_id"])["agent_rank"] != "Commander":
            raise Exception ("to low rank for this mission")
        
        return self.update(id, checked_data)
    
    def update_mission_status(self, id, status):
        mission = self.get_mission_by_id(id)
        if mission == "id not found":
            return "id not found"

        if status not in valid_status:
            raise Exception ("invalid status")
        
        if status == "IN_PROGRESS" and mission["status"] != "ASSIGNED":
            raise Exception ("invalid change")
    
        if status in ("FAILED", "COMPLETED") and mission["status"] != "IN_PROGRESS":
            raise Exception ("invalid change")
        
        if status == "CANCELLED" and mission["status"] not in ("NEW", "ASSIGNED"):
            raise Exception ("invalid change")
        
        return self.update(id, {"status": status})

    
    def assign_mission(self, m_id, a_id):
        agent = agents.get_agent_by_id(a_id)
        if agent == "id not found":
            return "id not found"
        
        mission = self.get_mission_by_id(m_id)
        if mission == "id not found":
            return "id not found"
        
        if self.count_open_missions_by_agent(a_id) >= 3:
            raise Exception ("agent has more than 3 missions open")
        
        if not agent["is_active"]:
            raise Exception ("agent not active")
    
        if mission["risk_level"] == "CRITICAL" and agent["agent_rank"] != "Commander":
            raise Exception ("to low rank for this mission")
        
        if mission["status"] != "NEW":
            raise Exception ("invalid status")
        
        return self.update(m_id, {"assigned_agent_id": a_id, "status": "ASSIGNED"})
        
    def count_open_missions_by_agent(self, id):
        agent = agents.get_agent_by_id(id)
        if agent == "id not found":
            return "agent id not found"
        
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(F"""SELECT COUNT(*) AS total FROM {self.table_name}
                           WHERE assigned_agent_id = %s
                           AND status IN ('ASSIGNED', 'IN_PROGRESS')
                           """
                           , [id])
            num = cursor.fetchone()
            return num["total"]
    
    def get_open_missions_by_agent(self, id):
        agent = agents.get_agent_by_id(id)
        if agent == "id not found":
            return "agent id not found"
        
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(F"""SELECT * FROM {self.table_name}
                           WHERE assigned_agent_id = %s
                           AND status IN ('ASSIGNED', 'IN_PROGRESS')
                           """
                           , [id])
            _missions = cursor.fetchall()
            if not _missions:
                return []
            return _missions
        
    def count_all_missions(self):
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT COUNT(*) as total FROM {self.table_name}")
            missions = cursor.fetchone()["total"]
            return missions
        
    def count_by_status(self, status):
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT status, COUNT(*) as total FROM {self.table_name} WHERE status = %s", [status])
            missions = cursor.fetchone()["total"]
            return missions
        
    def count_open_missions(self):
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(f"""SELECT COUNT(*) AS total FROM {self.table_name}
                           WHERE status IN
                           ('ASSIGNED', 'IN_PROGRESS')""")
            open_missions =cursor.fetchone()["total"]
            return open_missions
        
    def count_critical_missions(self):
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(f"""SELECT COUNT(*) as total FROM {self.table_name}
                           WHERE risk_level = 'CRITICAL'
                           """)
            missions = cursor.fetchone()["total"]
            return missions
        
    def get_top_agent(self):
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT MAX(completed_missions) AS top_agent FROM {agents.table_name}")
            top = cursor.fetchone()["top_agent"]
            cursor.execute(f"""SELECT * FROM {agents.table_name}
                           WHERE completed_missions = %s
                           """
                           , [top])

            _agents = cursor.fetchall()
            if not _agents:
                return []
                
            return _agents


missions = MissionDB()




        
    
    