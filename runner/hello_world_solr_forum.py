import argparse
import configparser
import os
import sys

import logbook
from pysolr import SolrError

from repository import SolrForumHandler


class HelloWorldSolrForum(object):
    config = None
    logger = None
    solrForum = None
    filename = ""

    SOLR_QPARAM = "created_date:[%s TO %s] "

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
        self.solrForum = SolrForumHandler.getInstance((self.config.get('Solr', 'solr_forum_url')), True)

    def get_sample_solr_data(self, start_date, end_date):
        self.logger.info("Get Sample Forum Data")
        start_date = start_date.replace('-', '')
        end_date = end_date.replace('-', '')
        query = self.SOLR_QPARAM % (start_date, end_date)
        idx = 0
        rows = 10
        params = {'rows': rows, 'start': idx}
        try:
            results = self.solrForum.getSolr().search(query, None, **params)
            while results is not None and results['response']['numFound'] > 0 and len(results['response']['docs']) > 0:
                for doc1 in results['response']['docs']:
                    self.logger.debug(doc1)
                    title = doc1['title']
                    url = doc1['url']
                    self.logger.info("URL: %s => TITLE: %s" % (url, title))
                idx = idx + rows
                params = {'rows': rows, 'start': idx}
                results = self.solrForum.getSolr().search(query, None, **params)

        except SolrError as exc:
            self.logger.error(exc)

    def run(self):
        self.init()
        self.logger.info("Starting %s" % self.filename)

        start_date = '2018-11-05'
        end_date = '2018-11-07'
        self.get_sample_solr_data(start_date, end_date)

        self.logger.info("Finish %s" % self.filename)


def main():
    mainclass = HelloWorldSolrForum()
    # try:
    mainclass.run()
    # except Exception as exc:
    #     mainclass.logger.error(exc)


if __name__ == '__main__':
    main()
