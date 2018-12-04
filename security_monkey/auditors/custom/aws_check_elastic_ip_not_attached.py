from security_monkey import app
from security_monkey.auditor import Auditor
from security_monkey.watchers.elastic_ip import ElasticIP

class UnusedElasticIPAuditor(Auditor):
    index = ElasticIP.index
    i_am_singular = ElasticIP.i_am_singular
    i_am_plural = ElasticIP.i_am_plural

    def __init__(self, accounts=None, debug=False):
        super(UnusedElasticIPAuditor, self).__init__(accounts=accounts, debug=debug)

    def check_volume_not_attached(self, elastic_ip):
        """
        show elastic ip's that are not attached to any instance
        """
        if elastic_ip.config.get('assigned_to') == None:
            self.add_issue(1, 'Elastic IP is not attached to any instance', elastic_ip, notes='None')