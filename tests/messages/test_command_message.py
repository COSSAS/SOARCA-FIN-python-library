import json
import unittest
from uuid import uuid1

from soarca_fin_python_library.models.command_sub_structure import CommandSubStructure
from soarca_fin_python_library.models.meta import Meta
from soarca_fin_python_library.models.command import Command
from soarca_fin_python_library.models.context import Context


class TestCommandMessage(unittest.TestCase):

    def test_command_message_generator(self):

        meta_id = str(uuid1())
        metaMessage = Meta(meta_id)

        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        contextMessage = Context(
            step_id, playbook_id, execution_id)

        command = "command"
        context = contextMessage
        variables = {}

        commandSubStructure = CommandSubStructure(
            command, context, variables)

        commandMessage = Command(
            commandSubStructure, metaMessage)

        self.assertIsInstance(commandMessage.command, CommandSubStructure)
        self.assertIsInstance(commandMessage.meta, Meta)
        self.assertIsNotNone(commandMessage.message_id)

    def test_command_from_json(self):

        meta_id = str(uuid1())
        metaMessage = Meta(meta_id)

        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        contextMessage = Context(
            step_id, playbook_id, execution_id)

        command = "command"
        context = contextMessage
        variables = {}

        commandSubStructure = Command(
            command, context, variables)

        command_id = str(uuid1())

        json_obj = {
            "type": "command",
            "message_id": command_id,
            "command": commandSubStructure.model_dump(),
            "meta": metaMessage.model_dump(),
        }

        commandMessage = Command(**json_obj)

        self.assertIsInstance(commandMessage.command, CommandSubStructure)
        self.assertIsInstance(commandMessage.meta, Meta)
        self.assertIsNotNone(commandMessage.message_id)

    def test_command_to_json(self):
        meta_id = str(uuid1())
        metaMessage = Meta(meta_id)

        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        contextMessage = Context(
            step_id, playbook_id, execution_id)

        command = "command"
        context = contextMessage
        variables = {}

        commandSubStructure = CommandSubStructure(
            command, context, variables)

        command_id = str(uuid1())

        json_obj = {
            "type": "command",
            "message_id": command_id,
            "command": commandSubStructure.model_dump(),
            "meta": metaMessage.model_dump(),
        }

        commandMessage = Command(
            commandSubStructure, metaMessage, command_id)

        json_str = commandMessage.model_dump_json()

        self.assertEqual(json.loads(json_str), json_obj)
