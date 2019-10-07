import argparse
import configparser
import logbook
import os
import sys

from dao import AdhocDatabaseHandler


class HelloWorldConnDb2(object):
    config = None
    logger = None
    db = None
    filename = ""

    def init(self):
        """init all helpers and services"""
        self.filename, file_extension = os.path.splitext(os.path.basename(__file__))

        # parse argument
        parser = argparse.ArgumentParser()
        parser.add_argument("--configdir", help="your config.ini directory", type=str)
        parser.add_argument("--logdir", help="your log directory", type=str)
        args = parser.parse_args()

        # determine config directory
        if args.configdir:
            config_file = os.path.join(args.configdir, 'config.ini')
        else:
            config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../config', 'config.ini')

        if args.logdir:
            log_file = os.path.join(args.logdir, '%s.log' % self.filename)
        else:
            log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../logs', '%s.log' % self.filename)

        # load config
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        # init logger
        logbook.set_datetime_format("local")
        self.logger = logbook.Logger(name=self.filename)
        format_string = '%s %s' % ('[{record.time:%Y-%m-%d %H:%M:%S.%f%z}] {record.level_name}',
                                   '{record.module}:{record.lineno}: {record.message}')
        if self.config.has_option('handler_stream_handler', 'verbose'):
            log_handler = logbook.StreamHandler(sys.stdout, level=self.config.get('Logger', 'level'), bubble=True,
                                                format_string=format_string)
            self.logger.handlers.append(log_handler)
            log_handler = logbook.TimedRotatingFileHandler(log_file, level=self.config.get('Logger', 'level'),
                                                           date_format='%Y%m%d', backup_count=5, bubble=True,
                                                           format_string=format_string)
            self.logger.handlers.append(log_handler)
        else:
            log_handler = logbook.TimedRotatingFileHandler(log_file, level=self.config.get('Logger', 'level'),
                                                           date_format='%Y%m%d', backup_count=5, bubble=True,
                                                           format_string=format_string)
            self.logger.handlers.append(log_handler)

        # init database
        self.db = AdhocDatabaseHandler.instantiate_from_configparser(self.config, self.logger)

    def run(self):
        self.init()
        self.logger.info("Starting %s" % self.filename)

        self.logger.info("Get All Active Campaigns")
        records = self.db.get_active_campaigns()
        for row in records:
            self.logger.info("Campaign #%d: %s" % (row.id, row.campaign_name))

        campaign_id = 330
        tracking_method = -2
        rowcount = self.db.set_tracking_method(campaign_id, tracking_method)
        self.logger.info("Set Tracking of Campaign #%d = %d" % (campaign_id, tracking_method))

        records = self.db.get_campaign_detail(campaign_id)
        if len(records) > 0:
            row = records[0]
            self.logger.info("Campaign #%d: %s" % (row.id, row.campaign_name))
            self.logger.info("  start: %s - %s" % (str(row.campaign_start), str(row.campaign_end)))
            self.logger.info("  tracking_method: %d" % row.tracking_method)

        self.logger.info("Finish %s" % self.filename)


def main():
    mainclass = HelloWorldConnDb2()
    # try:
    mainclass.run()
    # except Exception as exc:
    #     mainclass.logger.error(exc)


if __name__ == '__main__':
    main()
