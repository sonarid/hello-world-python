import configparser
import logging

import records


class AdhocDatabaseHandler(object):
    _db = None
    _host = None
    _port = None
    _user = None
    _pass = None
    _dbname = None
    logger = None

    @staticmethod
    def getInstance(_host, _port, _user, _pass, _dbname):
        """ Static access method. """
        return AdhocDatabaseHandler(_host, _port, _user, _pass, _dbname)

    def __init__(self, _host, _port, _user, _pass, _dbname):
        """ Virtually private constructor. """
        self._host = _host
        self._port = _port
        self._user = _user
        self._pass = _pass
        self._dbname = _dbname
        self.logger = logging.getLogger()
        self.connect()

    def setLogger(self, logger):
        self.logger = logger

    def connect(self):
        # try:
        self.logger.debug('connecting to MySQL database...')
        # print('connecting to MySQL database...')
        conn_string = 'mysql://{}:{}/{}?user={}&password={}&charset=utf8mb4'. \
            format(self._host, self._port, self._dbname, self._user, self._pass)
        self.logger.debug(conn_string)
        self._db = records.Database(conn_string)
        rs = self._db.query('SELECT VERSION() as ver', fetchall=True)
        if len(rs) > 0:
            db_version = rs[0].ver
        # except sqlalchemy.exc.OperationalError as error:
        #     self.logger.info('Error: connection not established {}'.format(error))
        AdhocDatabaseHandler._instance = None
        # else:
        self.logger.debug('connection established: {}'.format(db_version))

    @staticmethod
    def instantiate_from_configparser(cfg, logger):
        if isinstance(cfg, configparser.ConfigParser):
            dbhandler = AdhocDatabaseHandler.getInstance(cfg.get('Database', 'host'), cfg.get('Database', 'port'),
                                                         cfg.get('Database', 'username'),
                                                         cfg.get('Database', 'password'),
                                                         cfg.get('Database', 'dbname'))
            dbhandler.setLogger(logger)
            return dbhandler
        else:
            raise Exception('cfg is not an instance of configparser')

    def get_active_campaigns(self):
        sql = """SELECT * FROM sonar_data.tbl_campaign WHERE n_status = 1"""
        rs = self._db.query(sql, fetchall=True)
        return rs

    def get_campaign_detail(self, campaign_id):
        sql = """SELECT * FROM sonar_data.tbl_campaign WHERE id = :id"""
        rs = self._db.query(sql, fetchall=True, id=campaign_id)
        return rs

    def set_tracking_method(self, campaign_id, tracking_method):
        sql = """UPDATE sonar_data.tbl_campaign SET tracking_method = :method WHERE id = :id"""
        rs = self._db.query(sql, id=campaign_id, method=tracking_method)
        return rs
