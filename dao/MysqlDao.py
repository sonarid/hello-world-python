import logging
import mysql.connector
from mysql.connector import pooling


class MysqlConnectionFactory(object):
    driverClassName = None
    connectionUrl = None
    dbUser = None
    dbPwd = None
    dbHost = None
    dbPort = None
    dbName = None
    _instance = None
    connection_pool = None

    @staticmethod
    def get_instance(_host, _port, _user, _pass, _dbname):
        """ Static access method. """
        if MysqlConnectionFactory._instance is None:
            MysqlConnectionFactory(_host, _port, _user, _pass, _dbname)
        return MysqlConnectionFactory._instance

    def __init__(self, _host, _port, _user, _pass, _dbname):
        """ Virtually private constructor. """
        if MysqlConnectionFactory._instance is not None:
            raise Exception("{} is a singleton!".format(__name__))
        else:
            self._host = _host
            self._port = _port
            self._user = _user
            self._pass = _pass
            self._dbname = _dbname
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="pynative_pool",
                                                                               pool_size=5,
                                                                               pool_reset_session=True,
                                                                               host=self._host,
                                                                               database=self._dbname,
                                                                               user=self._user,
                                                                               password=self._pass)
            MysqlConnectionFactory._instance = self

    def get_connection(self):
        return self.connection_pool.get_connection()


class MysqlDao(object):
    connection = None
    logger = None

    def __init__(self, _host, _port, _user, _pass, _dbname):
        """ Virtually private constructor. """
        conn_factory = MysqlConnectionFactory.get_instance(_host, _port, _user, _pass, _dbname)
        self.logger = logging.getLogger()
        self.connection = conn_factory.get_connection()
        MysqlDao._instance = self

    def setLogger(self, logger):
        self.logger = logger

    def __del__(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            # print('connection closed')

    def ensure_connected(self):
        self.connection.is_connected()

    def select_query(self, sql, tuple_values=None):
        self.ensure_connected()
        cursor = self.connection.cursor(named_tuple=True)
        cursor.execute(sql, tuple_values)
        records = cursor.fetchall()
        cursor.close()
        return records

    def update_query(self, sql, tuple_values=None):
        self.ensure_connected()
        cursor = self.connection.cursor(named_tuple=True)
        cursor.execute(sql, tuple_values)
        rowcount = cursor.rowcount
        cursor.close()
        self.connection.commit()
        return rowcount
