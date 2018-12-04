from security_monkey import app
from security_monkey.auditor import Auditor
from security_monkey.watchers.custom.azure_instance import AzureInstance
import datetime

class AzureInstanceRunningAuditor(Auditor):
    index = AzureInstance.index
    i_am_singular = AzureInstance.i_am_singular
    i_am_plural = AzureInstance.i_am_plural

    def __init__(self, accounts=None, debug=True):
        super(AzureInstanceRunningAuditor, self).__init__(accounts=accounts, debug=debug)

    def check_running_instances(self, instance):
        """
        show instances that have been running longer then 48 hours
        """
        if instance:
            creation_timestamp = instance.config.get('tags').get('creation_timestamp')
            if creation_timestamp:
                date_time_obj = datetime.datetime.strptime(creation_timestamp, '%Y%m%d%H%M%S')
                if date_time_obj < datetime.datetime.now() - datetime.timedelta(days=2):
                    app.logger.debug(instance.name + ' instance is older than 2 days')
                    self.add_issue(10, 'Instance has been running more than 2 days', instance, notes='None')
            else:
                self.add_issue(1, 'Instance lacks creation_timestamp', instance, notes='None')