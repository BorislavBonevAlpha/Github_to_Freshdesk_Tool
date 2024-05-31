import unittest
from commands.create_or_update_command import CreateOrUpdate
from commands.delete_contact_command import DeleteContact
from core.command_factory import CommandFactory
from core.config import Config
from unittest.mock import patch


class TestCommandFactory(unittest.TestCase):
    @patch.object(Config, 'GITHUB_TOKEN', 'mock_github_token')
    @patch.object(Config, 'FRESHDESK_TOKEN', 'mock_freshdesk_token')
    def setUp(self):
        self.factory = CommandFactory()

    # Testing if every command has two parameters
    def test_create_or_update_command(self):
        cmd = self.factory.commands_creator("createorupdate parameter1 parameter2")
        self.assertIsInstance(cmd, CreateOrUpdate)

    def test_delete_command(self):
        cmd = self.factory.commands_creator("deletecontact parameter1 parameter2")
        self.assertIsInstance(cmd, DeleteContact)

    # Testing if there is an unknown command
    def test_unknown_command(self):
        with self.assertRaises(ValueError):
            self.factory.commands_creator("InvalidCommand")
