from security_monkey import app
from security_monkey.auditor import Auditor
from security_monkey.watchers.ec2.ec2_instance import EC2Instance

class EC2InstanceTagsAuditor(Auditor):
    index = EC2Instance.index
    i_am_singular = EC2Instance.i_am_singular
    i_am_plural = EC2Instance.i_am_plural

    def __init__(self, accounts=None, debug=False):
        super(EC2InstanceTagsAuditor, self).__init__(accounts=accounts, debug=debug)



    def check_instance_tags(self, instance):
        """
        show instances that have no tags
        """
        allowed_tags = ['Name', 'owner', 'service', 'product']
        existing_tags = set([])
        issues = set([])
        tags = instance.config.get('tags')
        for tag in tags:
            if tag['Key'] in allowed_tags:
                existing_tags.add(tag['Key'])
        count = 0
        while count < len(allowed_tags):
            count += 1
            if 'Name' not in existing_tags:
                issues.add('Name')
                existing_tags.add('Name')
            elif 'owner' not in existing_tags:
                issues.add('owner')
                existing_tags.add('owner')
            elif 'product' not in existing_tags:
                issues.add('product')
                existing_tags.add('product')
            elif 'service' not in existing_tags:
                issues.add('service')
                existing_tags.add('service')
            else:
                continue
        for issue in issues:
            app.logger.warning('issues list' + str(issues))
            self.add_issue(1, 'Instance lacks tag(s):' + str(issue), instance, notes='None')