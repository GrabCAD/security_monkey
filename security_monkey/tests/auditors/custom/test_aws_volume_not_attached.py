from security_monkey import AWS_DEFAULT_REGION
from security_monkey.tests import SecurityMonkeyTestCase
from security_monkey.auditors.custom.aws_check_volume_not_attached import UnusedEBSVolumeAuditor
from security_monkey.watchers.ec2.ebs_volume import EBSVolumeItem
from security_monkey.datastore import Account, AccountType
from security_monkey import db

AWS_VOLUME_ATTACHED = {
    "attachments": [
      {
        "attach_time": "2018-12-04 00:48:38+00:00",
        "instance_id": "i-123456789",
        "state": "attached",
        "volume_id": "vol-068baec57e6592be6",
        "device": "/dev/xvda"
      }
    ],
    "availability_zone": "us-east-1e",
    "create_time": "2018-12-04 00:48:38.895000+00:00",
    "name": "test volume",
    "size": 20,
    "snapshot_id": "snap-1234546789",
    "state": "in-use",
    "volume_id": "vol-123456789",
    "volume_type": "gp2"
}

AWS_VOLUME_NOT_ATTACHED = {
    "attachments": [],
    "availability_zone": "us-east-1a",
    "create_time": "2018-12-06 09:27:39.718000+00:00",
    "name": "vol-123456789",
    "size": 5,
    "snapshot_id": "",
    "state": "available",
    "volume_id": "vol-123456789",
    "volume_type": "gp2"
}

class UnusedVolumeAttachedAuditorTestCase(SecurityMonkeyTestCase):

    def pre_test_setup(self):
        UnusedEBSVolumeAuditor(accounts=['TEST_ACCOUNT']).OBJECT_STORE.clear()
        account_type_result = AccountType(name='AWS')
        db.session.add(account_type_result)
        db.session.commit()

        # main
        account = Account(identifier="123456789123", name="TEST_ACCOUNT",
                          account_type_id=account_type_result.id, notes="TEST_ACCOUNT",
                          third_party=False, active=True)

        db.session.add(account)
        db.session.commit()

    def test_check_volume_not_attached(self):
        auditor = UnusedEBSVolumeAuditor(accounts=['TEST_ACCOUNT'])
        auditor.prep_for_audit()

        item = EBSVolumeItem(region=AWS_DEFAULT_REGION, account='TEST_ACCOUNT', name='AWS_VOLUME',
                                    config=AWS_VOLUME_NOT_ATTACHED)

        auditor.check_volume_not_attached(item)
        self.assertEquals(len(item.audit_issues), 1)
        self.assertEquals(item.audit_issues[0].score, 1)

    def test_check_volume_attached(self):
        auditor = UnusedEBSVolumeAuditor(accounts=['TEST_ACCOUNT'])
        auditor.prep_for_audit()

        item = EBSVolumeItem(region=AWS_DEFAULT_REGION, account='TEST_ACCOUNT', name='AWS_VOLUME',
                                    config=AWS_VOLUME_ATTACHED)

        auditor.check_volume_not_attached(item)
        self.assertFalse(item.audit_issues)