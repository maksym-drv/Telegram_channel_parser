import datetime
import paramiko
import psycopg2
from config import Config

cfg = Config()

class Database: 
    def __init__(self):
        try:
            keepalive_kwargs = {
              "keepalives": 1,
              "keepalives_idle": 60,
              "keepalives_interval": 10,
              "keepalives_count": 5
            }
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(cfg.host, port=cfg.port, username=cfg.username, password=cfg.passw)
            print("A connection to the server has been established")
            self.conn = psycopg2.connect(
            database = cfg.database,
            user = cfg.user_data,
            password = cfg.password_data,
            host = cfg.host_data,
            port = cfg.port_data,
            **keepalive_kwargs
            )
            print ("Database connection established")
        except Exception as err:
            print(str(err))
            
    async def get_node_id(self, tg_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT node_id FROM sources WHERE tg_id = %s;""", (tg_id, ))
            return cursor.fetchall()

    async def get_recipients(self, node_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT tg_id FROM recipients WHERE node_id = %s;""", (node_id, ))
            return cursor.fetchall()

    async def add_history(self, from_id: int, to_id: int, from_word_id: int, to_word_id: int, send_time: datetime = datetime.datetime.now()):
        with self.conn.cursor() as cursor:
            cursor.execute("""INSERT INTO history (from_id, to_id, from_word_id, to_word_id, send_time) VALUES (%s, %s, %s, %s, %s);""", (from_id, to_id, from_word_id, to_word_id, send_time, ))
            self.conn.commit()

    async def get_reply_id(self, from_id: int, to_id: int, from_word_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT to_word_id FROM history WHERE from_id = %s AND to_id = %s AND from_word_id = %s;""", (from_id, to_id, from_word_id, ))
            return cursor.fetchone()[0]

    async def get_ignore(self, node_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT string_text, ignore, replace FROM ignore WHERE node_id = %s;""", (node_id, ))
            return cursor.fetchall()

    async def del_history(self, id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""DELETE FROM history WHERE id = %s;""", (id, ))
            self.conn.commit()