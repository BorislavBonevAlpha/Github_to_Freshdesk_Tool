from commands.create_or_update_command import CreateOrUpdate
from commands.delete_contact_command import DeleteContact
from core.config import Config
from typing import Any


class CommandFactory:

    def __init__(self) -> None:
        self.github_token = Config.GITHUB_TOKEN
        self.fresh_desk_token = Config.FRESHDESK_TOKEN

    def commands_creator(self, input_line: str) -> Any:
        cmd, *params = input_line.split()

        if cmd.lower() == "createorupdate":
            return CreateOrUpdate(params, self.github_token, self.fresh_desk_token)
        if cmd.lower() == "deletecontact":
            return DeleteContact(params, self.github_token, self.fresh_desk_token)

        raise ValueError(f'This command: [{cmd}] doesn\'t exist!')
