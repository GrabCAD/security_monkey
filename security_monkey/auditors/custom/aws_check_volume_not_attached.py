from security_monkey import app
from security_monkey.auditor import Auditor
from security_monkey.watchers.ec2.ebs_volume import EBSVolume

class UnusedEBSVolumeAuditor(Auditor):
    index = EBSVolume.index
    i_am_singular = EBSVolume.i_am_singular
    i_am_plural = EBSVolume.i_am_plural

    def __init__(self, accounts=None, debug=False):
        super(UnusedEBSVolumeAuditor, self).__init__(accounts=accounts, debug=debug)

    def check_volume_not_attached(self, volume):
        """
        show volumes that are not attached to any instance
        """
        if volume.config.get('state') == 'available':
            self.add_issue(1, 'Volume is not attached to any instance', volume, notes='None')