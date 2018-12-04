from security_monkey.account_manager import AccountManager, CustomFieldConfig


class AzureAccountManager(AccountManager):
    account_type = 'Azure'
    identifier_label = 'Organization Name'
    identifier_tool_tip = 'Enter the Azure AD Tenant ID'
    access_token_tool_tip = "Enter the path to the file that contains the Azure personal access token." # az account get-access-token
    custom_field_configs = [
        CustomFieldConfig('access_token_file', "Personal Access Token", True, access_token_tool_tip),
        ]

    def __init__(self):
        super(AzureAccountManager, self).__init__()