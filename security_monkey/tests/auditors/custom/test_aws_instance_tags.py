from security_monkey import AWS_DEFAULT_REGION
from security_monkey.tests import SecurityMonkeyTestCase
from security_monkey.auditors.custom.aws_check_instance_tags import EC2InstanceTagsAuditor
from security_monkey.watchers.ec2.ec2_instance import EC2InstanceItem
from security_monkey.datastore import Account, AccountType
from security_monkey import db

AWS_INSTANCE_TAGS = {
  "image_id": "ami-123456789",
  "instance_id": "i-123456789",
  "instance_type": "r4.xlarge",
  "launch_time": "2018-10-29 10:17:33+00:00",
  "name": "test123",
  "private_dns_name": "ip-172-1-1-1.ec2.internal",
  "private_ip_address": "172.1.1.11",
  "public_dns_name": "ec2-107-11-1-11.compute-1.amazonaws.com",
  "public_ip_address": "107.11.11.11",
  "security_groups": [
    {
      "GroupName": "test_secgroup",
      "GroupId": "sg-12345"
    }
  ],
  "state": {
    "Code": 16,
    "Name": "running"
  },
  "subnet_id": "subnet-111aaaaa",
  "tags": [
    {
      "Value": "test123",
      "Key": "Description"
    },
    {
      "Value": "test123",
      "Key": "Name"
    },
    {
      "Value": "ci",
      "Key": "account"
    },
    {
      "Value": "ci",
      "Key": "product"
    },
    {
      "Value": "test",
      "Key": "service"
    },
    {
      "Value": "test@gc.com",
      "Key": "owner"
    }
  ],
  "vpc_id": "vpc-111aaabbb"
}

class EC2InstanceTagsAuditorTestCase(SecurityMonkeyTestCase):

    def pre_test_setup(self):

        EC2InstanceTagsAuditor(accounts=['TEST_ACCOUNT']).OBJECT_STORE.clear()
        account_type_result = AccountType(name='AWS')
        db.session.add(account_type_result)
        db.session.commit()

        # main
        account = Account(identifier="123456789123", name="TEST_ACCOUNT",
                          account_type_id=account_type_result.id, notes="TEST_ACCOUNT",
                          third_party=False, active=True)

        db.session.add(account)
        db.session.commit()

    def test_check_instance_tags(self):
        auditor = EC2InstanceTagsAuditor(accounts=['TEST_ACCOUNT'])
        auditor.prep_for_audit()

        item = EC2InstanceItem(region=AWS_DEFAULT_REGION, account='TEST_ACCOUNT', name='AWS_INSTANCE_TAGS',
                                    config=AWS_INSTANCE_TAGS)

        print('test!!!' + str(item))
        test = auditor.check_instance_tags(item)
        print('test!!!' + str(test))
        print(dir(auditor))
        self.assertEquals(len(item.audit_issues), 1)
        #self.assertEquals(item.audit_issues[0].score, None)