import argparse
import configparser
import os
import sys

import logbook
from pysolr import SolrError

from repository import SolrAccountHandler


class HelloWorldSolrAccount(object):
    config = None
    logger = None
    solrAccount = None
    filename = ""
    solrCore = None

    SOLR_QPARAM = "published_date_i:[%s TO %s] AND channel_i:%d"

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
        self.solrAccount = SolrAccountHandler.getInstance((self.config.get('Solr', 'solr_url')))

    def get_sample_solr_data(self, start_date, end_date, channel_id):
        start_date = start_date.replace('-', '')
        end_date = end_date.replace('-', '')
        query = self.SOLR_QPARAM % (start_date, end_date, channel_id)
        idx = 0
        rows = 10
        params = {'rows': rows, 'start': idx}
        try:
            results = self.solrCore.search(query, None, **params)
            if results is not None and results['response']['numFound'] > 0 and len(results['response']['docs']) > 0:
                for doc1 in results['response']['docs']:
                    self.logger.debug(doc1)
                    id = doc1['id']
                    content = ''
                    if 'title_t' in doc1:
                        content = doc1['title_t']
                    elif 'message_t' in doc1:
                        content = doc1['message_t']
                    elif 'content_t' in doc1:
                        content = doc1['content_t']
                    elif 'caption_text_t' in doc1:
                        content = doc1['caption_text_t']
                    self.logger.info("ID: %s => CONTENT: %s" % (id, content))

        except SolrError as exc:
            self.logger.error(exc)

    def run(self):
        self.init()
        self.logger.info("Starting %s" % self.filename)

        # set which client_id to process
        client_id = 148
        self.solrCore = self.solrAccount.get_solr_core(client_id, True)

        start_date = '2018-11-05'
        end_date = '2018-11-07'

        self.logger.info("Get Sample Data for Twitter")
        channel_id = 1
        self.get_sample_solr_data(start_date, end_date, channel_id)

        self.logger.info("Get Sample Data for Facebook")
        channel_id = 2
        self.get_sample_solr_data(start_date, end_date, channel_id)

        self.logger.info("Get Sample Data for News")
        channel_id = 3
        self.get_sample_solr_data(start_date, end_date, channel_id)

        self.logger.info("Get Sample Data for Forum")
        channel_id = 4
        self.get_sample_solr_data(start_date, end_date, channel_id)

        self.logger.info("Get Sample Data for Blog")
        channel_id = 5
        self.get_sample_solr_data(start_date, end_date, channel_id)

        self.logger.info("Get Sample Data for Instagram")
        channel_id = 6
        self.get_sample_solr_data(start_date, end_date, channel_id)

        self.logger.info("Get Sample Data for Youtube")
        channel_id = 7
        self.get_sample_solr_data(start_date, end_date, channel_id)

        self.logger.info("Get Sample Data for Printed Media")
        channel_id = 8
        self.get_sample_solr_data(start_date, end_date, channel_id)

        self.logger.info("Finish %s" % self.filename)


def main():
    mainclass = HelloWorldSolrAccount()
    # try:
    mainclass.run()
    # except Exception as exc:
    #     mainclass.logger.error(exc)


if __name__ == '__main__':
    main()
