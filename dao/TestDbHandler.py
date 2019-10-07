import configparser

from dao.MysqlDao import MysqlDao


class TestDbHandler(MysqlDao):

    @staticmethod
    def getInstance(_host, _port, _user, _pass, _dbname):
        return TestDbHandler(_host, _port, _user, _pass, _dbname)

    @staticmethod
    def instantiate_from_configparser(cfg, logger):
        if isinstance(cfg, configparser.ConfigParser):
            dbhandler = TestDbHandler.getInstance(cfg.get('Database', 'host'), cfg.get('Database', 'port'),
                                                  cfg.get('Database', 'username'),
                                                  cfg.get('Database', 'password'),
                                                  cfg.get('Database', 'dbname'))
            dbhandler.setLogger(logger)
            return dbhandler
        else:
            raise Exception('cfg is not an instance of configparser')

    def get_active_campaigns(self):
        sql = """SELECT * FROM sonar_data.tbl_campaign WHERE n_status = 1"""
        return self.select_query(sql)

    def get_campaign_detail(self, campaign_id):
        sql = """SELECT * FROM sonar_data.tbl_campaign WHERE id = %s"""
        return self.select_query(sql, (campaign_id,))

    def set_tracking_method(self, campaign_id, tracking_method):
        sql = """UPDATE sonar_data.tbl_campaign SET tracking_method = %s WHERE id = %s"""
        return self.update_query(sql, (tracking_method, campaign_id,))
