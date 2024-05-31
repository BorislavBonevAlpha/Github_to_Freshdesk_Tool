from core.command_factory import CommandFactory
from core.engine import Engine
from database.data import create_database

create_database()

cmd_factory = CommandFactory()
engine = Engine(cmd_factory)

engine.engine_starter()

