import mysql.connector


class DB():
    def __init__(self):
        self.conn = self.get_connection()
        self.create_database()
        self.create_tables()


    def get_connection(self):
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="1234"
        )
        return conn
    

    @property
    def connect(self):
        if not self.conn.is_connected():
            self.conn = self.get_connection()
        return self.conn
    

    def create_database(self):
        create_query = "CREATE DATABASE IF NOT EXISTS Intelligence_db"
        use_query = "USE Intelligence_db"

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(create_query)

            if cursor.warning_count == 0:
                print("database created successfuly")
                
            cursor.execute(use_query)
            

    def create_tables(self):
        agents_query ="""
            CREATE TABLE IF NOT EXISTS agents (
            id INT PRIMARY KEY AUTO_INCREMENT ,
            name VARCHAR(50) NOT NULL ,
            specialty VARCHAR(100) NOT NULL ,
            is_active BOOLEAN DEFAULT TRUE NOT NULL ,
            complete_missions INT DEFAULT 0 ,
            failed_missions INT DEFAULT 0 ,
            agent_rank ENUM("junior", "senior", "commander")
            )"""
        
        missions_query ="""
            CREATE TABLE IF NOT EXISTS missions (
            id INT PRIMARY KEY AUTO_INCREMENT ,
            title VARCHAR(100) NOT NULL ,
            description TEXT NOT NULL ,
            location VARCHAR(100) NOT NULL ,
            difficulty INT NOT NULL ,
            importance INT NOT NULL ,
            status ENUM("new", "assigned", "in_progress", "completed", "failed", "cancelled") ,
            risk_level ENUM("low", "medium", "high", "critical") ,
            assigned_agent_id INT
            )"""

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(agents_query)
            cursor.execute(missions_query)
            
            if cursor.warning_count == 0:
                print("tables created successfuly")
        
db = DB()