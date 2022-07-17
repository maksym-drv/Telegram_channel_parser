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
            
    async def create_node(self, node_name: str):
        with self.conn.cursor() as cursor:
            cursor.execute("""INSERT INTO nodes (node_name) VALUES (%s) RETURNING id;""", (node_name, ))
            self.conn.commit()
            return cursor.fetchone()[0]
            
    async def add_source(self, tg_id: int, tg_name: str, node_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""INSERT INTO sources (tg_id, tg_name, node_id) VALUES (%s, %s, %s);""", (tg_id, tg_name, node_id, ))
            self.conn.commit()
    
    async def add_recipient(self, tg_id: int, tg_name: str, node_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""INSERT INTO recipients (tg_id, tg_name, node_id) VALUES (%s, %s, %s);""", (tg_id, tg_name, node_id, ))
            self.conn.commit()

    async def add_ignore(self, string_ignore: str, replace: str, node_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""INSERT INTO ignore (string_ignore, replace, node_id) VALUES (%s, %s, %s);""", (string_ignore, replace, node_id, ))
            self.conn.commit()
    
    async def check_node(self, node_name: str):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT EXISTS(SELECT id FROM nodes WHERE node_name = %s);""", (node_name, ))
            return cursor.fetchone()[0]

    async def get_node_id(self, node_name: str):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT id FROM nodes WHERE node_name = %s;""", (node_name, ))
            return cursor.fetchone()[0]

    async def get_node_name(self, node_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT node_name FROM nodes WHERE id = %s;""", (node_id, ))
            return cursor.fetchone()[0]

    async def get_nodes(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT node_name FROM nodes;""")
            return cursor.fetchall()

    async def get_sources(self, node_name):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT tg_name, id FROM sources WHERE node_id = (SELECT id FROM nodes WHERE node_name = %s);""", (node_name, ))
            return cursor.fetchall()

    async def get_recipients(self, node_name):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT tg_name, id FROM recipients WHERE node_id = (SELECT id FROM nodes WHERE node_name = %s);""", (node_name, ))
            return cursor.fetchall()

    async def del_source(self, source_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""DELETE FROM sources WHERE id = %s;""", (source_id, ))
            self.conn.commit()

    async def del_recipient(self, recipient_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""DELETE FROM recipients WHERE id = %s;""", (recipient_id, ))
            self.conn.commit()

    async def del_node(self, node_name: str):
        with self.conn.cursor() as cursor:
            cursor.execute("""DELETE FROM ignore WHERE node_id = (SELECT id FROM nodes WHERE node_name = %s);""", (node_name, ))
            cursor.execute("""DELETE FROM sources WHERE node_id = (SELECT id FROM nodes WHERE node_name = %s);""", (node_name, ))
            cursor.execute("""DELETE FROM recipients WHERE node_id = (SELECT id FROM nodes WHERE node_name = %s);""", (node_name, ))
            cursor.execute("""DELETE FROM nodes WHERE node_name = %s;""", (node_name, ))
            self.conn.commit()

    async def add_ignore(self, string_text: str, replace: str, ignore: bool, node_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""INSERT INTO ignore (string_text, replace, node_id, ignore) VALUES (%s, %s, %s, %s);""", (string_text, replace, node_id, ignore, ))
            self.conn.commit()

    async def get_ignore(self, node_name):
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT string_text, replace, ignore, id FROM ignore WHERE node_id = (SELECT id FROM nodes WHERE node_name = %s);""", (node_name, ))
            return cursor.fetchall()

    async def del_ignore(self, id: int, node_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("""DELETE FROM ignore WHERE id = %s AND node_id = %s;""", (id, node_id, ))
            self.conn.commit()