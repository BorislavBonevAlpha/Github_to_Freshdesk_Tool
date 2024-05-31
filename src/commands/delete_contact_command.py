from common.github_extraction_mapper import map_github_to_freshdesk
from common.validators import validate_params_count
from client_models.github import GitHubClient
from client_models.freshdesk import FreshdeskAPI


class DeleteContact:

    def __init__(self, params: list[str], github_token: str, fresh_desk_token: str) -> None:

        validate_params_count(params, 2)
        self._params = params
        self._github_client = GitHubClient(github_token)
        self._freshdesk_client = FreshdeskAPI(fresh_desk_token)

    def execute(self) -> None:

        github_username, freshdesk_subdomain = self._params

        github_user_info = self._github_client.get_github_user_information(github_username)

        if github_user_info:
            # If we have github_user_info present, we map the values to the needed ones for freshdesk
            mapped_user_info = map_github_to_freshdesk(github_user_info)
            delete_status = self._freshdesk_client.permanently_delete_contact(freshdesk_subdomain, mapped_user_info)
            if delete_status:
                print("Contact deleted successfully in Freshdesk.")
            else:
                print("Failed to delete contact in Freshdesk.")
        else:
            print("Failed to retrieve GitHub user information.")
