import mysql.connector
from logs.logger_config import logger


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
            with self.conn.cursor(dictionary=True) as cursor:
                cursor.execute("USE Intelligence_db")
            logger.info("connected to database successfully")
        return self.conn
    

    def create_database(self):
        create_query = "CREATE DATABASE IF NOT EXISTS Intelligence_db"
        use_query = "USE Intelligence_db"

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(create_query)

            if cursor.warning_count == 0:
                logger.info("database created successfuly")

            cursor.execute(use_query)


    def create_tables(self):
        agents_query ="""
            CREATE TABLE IF NOT EXISTS agents (
            id INT PRIMARY KEY AUTO_INCREMENT ,
            name VARCHAR(50) NOT NULL ,
            specialty VARCHAR(100) NOT NULL ,
            is_active BOOLEAN DEFAULT TRUE NOT NULL ,
            completed_missions INT DEFAULT 0 ,
            failed_missions INT DEFAULT 0 ,
            agent_rank ENUM("Junior", "Senior", "Commander")
            )"""
        
        missions_query ="""
            CREATE TABLE IF NOT EXISTS missions (
            id INT PRIMARY KEY AUTO_INCREMENT ,
            title VARCHAR(100) NOT NULL ,
            description TEXT NOT NULL ,
            location VARCHAR(100) NOT NULL ,
            difficulty INT NOT NULL CHECK(difficulty BETWEEN 1 AND 10) ,
            importance INT NOT NULL CHECK(importance BETWEEN 1 AND 10) ,
            status ENUM('NEW', 'ASSIGNED', 'IN_PROGRESS', 'COMPLETED', 'FAILED', 'CANCELLED') DEFAULT 'NEW' ,
            risk_level ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') ,
            assigned_agent_id INT
            )"""

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(agents_query)

            if cursor.warning_count == 0:
                logger.info("table created successfuly")

            cursor.execute(missions_query)
            
            if cursor.warning_count == 0:
                print("table created successfuly")
        
db = DB()