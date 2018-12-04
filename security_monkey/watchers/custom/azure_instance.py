from security_monkey.decorators import record_exception, iter_account_region
from security_monkey.watcher import Watcher
from security_monkey.watcher import ChangeItem
from security_monkey import app
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource.resources import ResourceManagementClient
import os


class AzureInstance(Watcher):
    index = 'azureinstance'
    i_am_singular = 'Azure Instance'
    i_am_plural = 'Azure Instances'
    account_type = 'Azure'

    def __init__(self, accounts=None, debug=True):
        super(AzureInstance, self).__init__(accounts=accounts, debug=debug)

    def list_instances(self, **kwargs):
        resource_groups = {}
        instances = []
        subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
        credentials = ServicePrincipalCredentials(
            client_id=os.environ['AZURE_CLIENT_ID'],
            secret=os.environ['AZURE_CLIENT_SECRET'],
            tenant=os.environ['AZURE_TENANT_ID'],
        )
        resource_client = ResourceManagementClient(credentials, subscription_id)

        for resource_group in resource_client.resource_groups.list():
            resource_groups[resource_group.name] = []
            for resource in resource_client.resources.list_by_resource_group(resource_group.name):
                if resource:
                    if resource.type == 'Microsoft.Compute/virtualMachines':
                        resource_groups[resource_group.name].append(resource)
        return resource_groups

    def slurp(self):
        """
        :returns: item_list - list of Azure instances in use by account
        :returns: exception_map - A dict where the keys are a tuple containing the
            location of the exception and the value is the actual exception

        """
        self.prep_for_slurp()

        def slurp_items(**kwargs):
            item_list = []
            exception_map = {}
            kwargs['exception_map'] = exception_map
            kwargs['account_name'] = 'azure-ci'

            resource_groups= self.list_instances(**kwargs)
            for resource_group, instances in resource_groups.items():
                if instances:
                    for instance in instances:
                        config = {
                            'name': instance.name,
                            'id': instance.id,
                            'tags': instance.tags,
                            'location': instance.location,
                            'resource_group': resource_group
                        }

                        app.logger.debug(config)


                        item = AzureInstanceItem(region=instance.location,
                                                account=kwargs['account_name'],
                                                name=instance.name, config=dict(config), source_watcher=self)

                        item_list.append(item)
            return item_list, exception_map
        return slurp_items()

class AzureInstanceItem(ChangeItem):
    def __init__(self, region=None, account=None, name=None, config=None, source_watcher=None):
        super(AzureInstanceItem, self).__init__(
            index=AzureInstance.index,
            region=region,
            account=account,
            name=name,
            new_config=config if config else {},
            source_watcher=source_watcher)
