from core.command_factory import CommandFactory


class Engine:
    def __init__(self, factory: CommandFactory) -> None:
        self._command_factory = factory

    def engine_starter(self) -> None:
        output: list[str] = []
        print(
            "\nHello and welcome to this program. In here you can create, delete and update existing different contacts from github to your freshdesk account. \n"
            "------------------------------------------------------------------------------------------------------------------------------------------------"
            "\nType your prefered command and after that put your desired github username and then the subdomain from your freshdesk account.\n"
            "------------------------------------------------------------------------------------------------------------------------------------------------"
            "\nCommand examples: createorupdate myusername mysubdomain | deletecontact myusername mysubdomain. \n"
            "------------------------------------------------------------------------------------------------------------------------------------------------"
            "\nAvailable commands: [createorupdate] | [deletecontact]")
        while True:
            try:
                input_line = input()
                if input_line.lower() == 'end':
                    break

                command = self._command_factory.commands_creator(input_line)
                output.append(command.execute())
            except ValueError as err:
                print(err.args[0])

        print('\n'.join(output))
