import psycopg2, os, sys
from comm.Log import logger
from comm.config import Config, CONFIG_FILE, LOG_PATH


class PostgreDB(object):  # Mysql can refer to this class, it's basically no change.
    """docstring for PostgreDB"""

    def __init__(self):
        c = Config().get('postgresql')
        self.host = c.get('host') if c and c.get('host') else '192.168.0.100'
        self.port = c.get('port') if c and c.get('port') else '5432'
        self.user = c.get('user') if c and c.get('user') else 'postgres'
        self.password = c.get('password') if c and c.get('password') else 'postgres'
        self.datebase = c.get('database') if c and c.get('datebase') else 'testdb'

        super(PostgreDB, self).__init__()
        self.conn = psycopg2.connect(database=self.datebase, user=self.user, password=self.password,
                                     host=self.host, port=self.port)
        self.cur = self.conn.cursor()
        logger.info('connect DB successfully!')

    def reConnect(self):
        try:
            self.conn.ping()
        except:
            self.conn()

    def db(self, sql):
        try:
            self.cur.execute(sql)
            logger.info(sql)
            self.conn.commit()
            rows = self.cur.fetchall()
            logger.info(rows)
            return rows
        except Exception as e:
            # self.conn.ca
            logger.error('************\nError Message：', str(e), '\n')

    def closeDB(self):
        self.cur.close()
        logger.info("Database closed!")

