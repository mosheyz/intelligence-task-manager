from .db_connection import db


class BaseDB:
    def __init__(self, table_name):
        self.table_name = table_name
    

    def create(self, data:dict):
        columns = ", ".join([k for k in data.keys()])
        plase_holders = ", ".join(["%s"] * len(data.keys()))
        values = list(data.values())
        query = f"""
                INSERT INTO {self.table_name}
                ({columns})
                VALUES ({plase_holders})
                """

        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(query, values)
            id = cursor.lastrowid
            db.connect.commit()
        
        return self.get_by_id(id)


    def get_all(self):
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT * FROM {self.table_name}")
            
            all = cursor.fetchall()
            if not all:
                return []
        
        return all
    

    def get_by_id(self, id):
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(f"""
                            SELECT * FROM {self.table_name}
                            WHERE id = %s"""
                            , [id])
            
            line = cursor.fetchone()
            if not line:
                return "id not found"
            
        return line


    def update(self, id, data):
        columns = ", ".join([f"{k} = %s" for k in data.keys()])
        values = list(data.values()) + [id]
        query = f"""
                UPDATE {self.table_name}
                SET {columns}
                WHERE id = %s
                """
        
        with db.connect.cursor(dictionary=True) as cursor:
            cursor.execute(query, values)
            db.connect.commit()
        
        return self.get_by_id(id)
