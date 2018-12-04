from security_monkey import app
from security_monkey.auditor import Auditor
from security_monkey.watchers.security_group import SecurityGroup

class UnusedSecurityGroupAuditor(Auditor):
    index = SecurityGroup.index
    i_am_singular = SecurityGroup.i_am_singular
    i_am_plural = SecurityGroup.i_am_plural

    def __init__(self, accounts=None, debug=False):
        super(UnusedSecurityGroupAuditor, self).__init__(accounts=accounts, debug=debug)

    def check_volume_not_attached(self, secgroup):
        """
        show secgroups that are not attached to any instance
        """
        # we dont care about aws default secgroups, as we cant remove them anyway
        if secgroup.config.get('name') != 'default':
            if secgroup.config.get('assigned_to') == []:
                self.add_issue(1, 'Security Group is not attached to any instance', secgroup, notes='None')