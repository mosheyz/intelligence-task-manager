from .db_connection import db


class BaseDB:
    def __init__(self, table_name):
        self.table_name = table_name
    

    def create(self, data:dict):
        columns = data.keys()
        plase_holders = ", ".join("%s" * len(columns))
        values = list(data.values())
        query = f"""
                INSERT INTO {self.table_name}
                ({columns})
                VALUES ({plase_holders})
                """

        with db.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, values)
            agent_id = cursor.lastrowid
            db.conn.commit()
        
        return self.get_by_id(agent_id)


    def get_all(self):
        with db.conn.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT * FROM {self.table_name}")
            all = cursor.fetchall()
        
        return all
    

    def get_by_id(self, id):
        with db.conn.cursor(dictionary=True) as cursor:
            cursor.execute(f"""
                            SELECT * FROM {self.table_name}
                            WHERE id = %s"""
                            , [id])
            
            line = cursor.fetchone()
        
        return line


    def update(self, id, data):
        columns = ", ".join(f"{k} = %s" for k in data.keys())
        values = list(data.values()) + [id]
        query = f"""
                UPDATE {self.table_name}
                SET {columns}
                WHERE id = %s
                )"""
        
        with db.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, values)
            db.conn.commit()
        
        agent_id = self.get_by_id(id)
        return self.get_by_id(agent_id)
