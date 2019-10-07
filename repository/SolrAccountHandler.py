import pysolr
import logging


class SolrAccountHandler(object):
    _instance = None
    _solrAccountCores = {}
    _solrAccountUrl = None
    _logger = None

    @staticmethod
    def getInstance(__solrAccountUrl):
        """ Static access method. """
        if SolrAccountHandler._instance is None:
            SolrAccountHandler(__solrAccountUrl)
        return SolrAccountHandler._instance

    def __init__(self, __solrAccountUrl):
        """ Virtually private constructor. """
        if SolrAccountHandler._instance is not None:
            raise Exception("{} is a singleton!".format(__name__))
        else:
            self._solrAccountUrl = __solrAccountUrl
            SolrAccountHandler._instance = self
            self._logger = logging.getLogger()

    def setLogger(self, logger):
        self._logger = logger

    def get_solr_core(self, _clientid, use_dict=False):
        if self._solrAccountUrl is None:
            return None
        if _clientid not in self._solrAccountCores:
            solr_account_core_url = "{}/account{}".format(self._solrAccountUrl, _clientid)
            self._logger.info("connecting to SOLR {}".format(solr_account_core_url))
            if use_dict:
                solr = pysolr.Solr(solr_account_core_url, timeout=60, always_commit=False, results_cls=dict)
            else:
                solr = pysolr.Solr(solr_account_core_url, timeout=60, always_commit=False)
            self._logger.info("connection establised to SOLR {}".format(solr_account_core_url))
            self._solrAccountCores[_clientid] = solr
        return self._solrAccountCores[_clientid]
