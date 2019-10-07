import logging
import pysolr


class SolrForumHandler(object):
    _instance = None
    _solrNewsUrl = None
    _solr = None
    logger = None

    @staticmethod
    def getInstance(_solrNewsUrl, use_dict=False):
        """ Static access method. """
        if SolrForumHandler._instance is None:
            SolrForumHandler(_solrNewsUrl, use_dict)
        return SolrForumHandler._instance

    def __init__(self, _solrNewsUrl, use_dict=False):
        """ Virtually private constructor. """
        if SolrForumHandler._instance is not None:
            raise Exception("{} is a singleton!".format(__name__))
        else:
            self._solrNewsUrl = _solrNewsUrl
            SolrForumHandler._instance = self
            self.logger = logging.getLogger()
            if use_dict:
                self._solr = pysolr.Solr(_solrNewsUrl, timeout=10, always_commit=False, results_cls=dict)
            else:
                self._solr = pysolr.Solr(_solrNewsUrl, timeout=10, always_commit=False)

    def getSolr(self):
        return self._solr
