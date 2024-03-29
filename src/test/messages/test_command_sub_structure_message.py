import json
import unittest
from uuid import uuid1

from src.message_factory import generateCommandSubStructureMessage, generateContextMessage
from src.models.context import Context
from src.models.command_sub_structure import CommandSubStructure


class TestCommandSubStructureMessage(unittest.TestCase):

    def test_command_sub_structure_message(self):

        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        contextMessage = generateContextMessage(
            step_id, playbook_id, execution_id)

        command = "command"
        context = contextMessage
        variables = {}

        commandSubStructure = generateCommandSubStructureMessage(
            command, context, variables)

        self.assertEqual(commandSubStructure.command, command)
        self.assertIsNone(commandSubStructure.authentication)
        self.assertEqual(commandSubStructure.variables, variables)
        self.assertIsInstance(commandSubStructure.context, Context)

    def test_command_sub_structure_from_json(self):
        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        contextMessage = generateContextMessage(
            step_id, playbook_id, execution_id)

        command = "command"
        context = contextMessage
        variables = {}

        json_obj = {
            "command": command,
            "authentication": None,
            "context": context,
            "variables": variables,
        }

        commandSubStructure = CommandSubStructure(**json_obj)

        self.assertEqual(commandSubStructure.command, command)
        self.assertIsNone(commandSubStructure.authentication)
        self.assertEqual(commandSubStructure.variables, variables)
        self.assertIsInstance(commandSubStructure.context, Context)

    def test_command_sub_structure_to_json(self):
        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        contextMessage = generateContextMessage(
            step_id, playbook_id, execution_id)

        command = "command"
        context = contextMessage
        variables = {}

        json_obj = {
            "command": command,
            "context": context.model_dump(),
            "variables": variables,
            "authentication": None,
        }

        commandSubStructure = generateCommandSubStructureMessage(
            command, context, variables)

        json_str = commandSubStructure.model_dump_json()

        self.assertEqual(json.loads(json_str), json_obj)
