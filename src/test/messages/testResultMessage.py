import json
import unittest
from uuid import uuid1

from messageFactory import generateContextMessage, generateMetaMessage, generateResultMessage, generateResultStructureMessage
from models.resultStructure import ResultStructure
from models.meta import Meta
from models.result import Result


class TestResultMessage(unittest.TestCase):

    def test_result_generator(self):
        state = "failure"
        variables = {}

        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        contextMessage = generateContextMessage(
            step_id, playbook_id, execution_id)

        resultStructureMessage = generateResultStructureMessage(
            state, contextMessage, variables)

        fin_id = str(uuid1())
        metaMessage = generateMetaMessage(fin_id)

        resultMessage = generateResultMessage(
            resultStructureMessage, metaMessage)

        self.assertIsInstance(resultMessage.result, ResultStructure)
        self.assertIsInstance(resultMessage.meta, Meta)
        self.assertIsNotNone(resultMessage.message_id)

    def test_result_from_json(self):
        state = "failure"
        variables = {}

        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        contextMessage = generateContextMessage(
            step_id, playbook_id, execution_id)

        resultStructureMessage = generateResultStructureMessage(
            state, contextMessage, variables)

        fin_id = str(uuid1())
        metaMessage = generateMetaMessage(fin_id)

        message_id = str(uuid1())

        json_obj = {
            "type": "result",
            "message_id": message_id,
            "result": resultStructureMessage.model_dump(),
            "meta": metaMessage.model_dump(),
        }

        resultMessage = Result(**json_obj)

        self.assertEqual(resultMessage.message_id, message_id)
        self.assertIsInstance(resultMessage.result, ResultStructure)
        self.assertIsInstance(resultMessage.meta, Meta)
        self.assertIsNotNone(resultMessage.message_id)

    def test_result_to_json(self):
        state = "failure"
        variables = {}

        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        contextMessage = generateContextMessage(
            step_id, playbook_id, execution_id)

        resultStructureMessage = generateResultStructureMessage(
            state, contextMessage, variables)

        fin_id = str(uuid1())
        metaMessage = generateMetaMessage(fin_id)

        message_id = str(uuid1())

        json_obj = {
            "type": "result",
            "message_id": message_id,
            "result": resultStructureMessage.model_dump(),
            "meta": metaMessage.model_dump(),
        }

        resultMessage = generateResultMessage(
            resultStructureMessage, metaMessage, message_id)

        json_str = resultMessage.model_dump_json()

        self.assertEqual(json.loads(json_str), json_obj)
