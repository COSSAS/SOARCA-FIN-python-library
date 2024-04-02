import json
import unittest
from uuid import uuid1


from soarca_fin_python_library.models.context import Context
from soarca_fin_python_library.models.result_structure import ResultStructure


class TestResultStructure(unittest.TestCase):

    def test_result_structure_message_generator(self):
        state = "failure"
        variables = {}

        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        contextMessage = Context(
            step_id, playbook_id, execution_id)

        resultStructureMessage = ResultStructure(
            state, contextMessage, variables)

        self.assertEqual(resultStructureMessage.state, state)
        self.assertEqual(resultStructureMessage.variables, variables)
        self.assertIsInstance(resultStructureMessage.context, Context)

    def test_result_structure_from_json(self):
        state = "failure"
        variables = {}

        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        contextMessage = Context(
            step_id, playbook_id, execution_id)

        json_object = {
            "state": state,
            "variables": variables,
            "context": contextMessage,
        }

        resultStructureMessage = ResultStructure(**json_object)

        self.assertEqual(resultStructureMessage.state, state)
        self.assertEqual(resultStructureMessage.variables, variables)
        self.assertIsInstance(resultStructureMessage.context, Context)

    def test_result_structure_to_json(self):
        state = "failure"
        variables = {}

        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        contextMessage = Context(
            step_id, playbook_id, execution_id)

        json_object = {
            "state": state,
            "variables": variables,
            "context": contextMessage.model_dump(),
        }

        resultStructureMessage = ResultStructure(
            state, contextMessage, variables)
        json_str = resultStructureMessage.model_dump_json()

        self.assertEqual(json.loads(json_str), json_object)
