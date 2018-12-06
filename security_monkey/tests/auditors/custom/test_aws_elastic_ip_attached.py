from security_monkey import AWS_DEFAULT_REGION
from security_monkey.tests import SecurityMonkeyTestCase
from security_monkey.auditors.custom.aws_check_elastic_ip_not_attached import UnusedElasticIPAuditor
from security_monkey.watchers.elastic_ip import ElasticIPItem
from security_monkey.datastore import Account, AccountType
from security_monkey import db

AWS_ELASTICIP_ATTACHED = {
    "allocation_id": "eipalloc-123456789",
    "assigned_to": "test",
    "association_id": "eipassoc-123456789",
    "domain": "vpc",
    "instance_id": "i-123456789",
    "network_interface_id": "eni-123456789",
    "network_interface_owner_id": "123456789",
    "private_ip_address": "172.1.1.1",
    "public_ip": "54.1.1.1"
}

AWS_ELASTICIP_NOT_ATTACHED = {
    "allocation_id": "eipalloc-123456789",
    "assigned_to": null,
    "association_id": null,
    "domain": "vpc",
    "instance_id": null,
    "network_interface_id": null,
    "network_interface_owner_id": null,
    "private_ip_address": null,
    "public_ip": "54.1.1.1"
}

class UnusedElasticIPAuditorTestCase(SecurityMonkeyTestCase):

    def pre_test_setup(self):
        UnusedElasticIPAuditor(accounts=['TEST_ACCOUNT']).OBJECT_STORE.clear()
        account_type_result = AccountType(name='AWS')
        db.session.add(account_type_result)
        db.session.commit()

        # main
        account = Account(identifier="123456789123", name="TEST_ACCOUNT",
                          account_type_id=account_type_result.id, notes="TEST_ACCOUNT",
                          third_party=False, active=True)

        db.session.add(account)
        db.session.commit()

    def test_check_elasticip_not_attached(self):
        auditor = UnusedElasticIPAuditor(accounts=['TEST_ACCOUNT'])
        auditor.prep_for_audit()

        item = ElasticIPItem(region=AWS_DEFAULT_REGION, account='TEST_ACCOUNT', name='AWS_ELASTICIP',
                                    config=AWS_ELASTICIP_NOT_ATTACHED)

        auditor.check_elasticip_not_attached(item)
        self.assertEquals(len(item.audit_issues), 1)
        self.assertEquals(item.audit_issues[0].score, 1)

    def test_check_elasticip_attached(self):
        auditor = UnusedElasticIPAuditor(accounts=['TEST_ACCOUNT'])
        auditor.prep_for_audit()

        item = ElasticIPItem(region=AWS_DEFAULT_REGION, account='TEST_ACCOUNT', name='AWS_ELASTICIP',
                                    config=AWS_ELASTICIP_ATTACHED)

        auditor.check_elasticip_not_attached(item)
        self.assertFalse(item.audit_issues)