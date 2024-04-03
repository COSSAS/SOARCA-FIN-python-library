from datetime import datetime, timezone
import json
import unittest
from uuid import uuid1


from soarca_fin_python_library.models.result_structure import ResultStructure
from soarca_fin_python_library.models.meta import Meta
from soarca_fin_python_library.models.result import Result
from soarca_fin_python_library.models.context import Context


from soarca_fin_python_library.models.security import Security
from soarca_fin_python_library.models.agent_structure import AgentStructure
from soarca_fin_python_library.models.external_reference import ExternalReference
from soarca_fin_python_library.models.capability_structure import CapabilityStructure
from soarca_fin_python_library.models.register import Register
from soarca_fin_python_library.models.step_structure import StepStructure


class TestResultMessage(unittest.TestCase):

    def test_result_generator(self):
        state = "failure"
        variables = {}

        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        contextMessage = Context(
            step_id=step_id, playbook_id=playbook_id, execution_id=execution_id)

        resultStructureMessage = ResultStructure(
            state=state, context=contextMessage, variables=variables)

        fin_id = str(uuid1())
        timestamp = datetime.now(timezone.utc).isoformat()
        metaMessage = Meta(sender_id=fin_id, timestamp=timestamp)

        message_id = str(uuid1())
        resultMessage = Result(message_id=message_id,
                               result=resultStructureMessage, meta=metaMessage)

        self.assertIsInstance(resultMessage.result, ResultStructure)
        self.assertIsInstance(resultMessage.meta, Meta)
        self.assertIsNotNone(resultMessage.message_id)

    def test_result_from_json(self):
        state = "failure"
        variables = {}

        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        contextMessage = Context(
            step_id=step_id, playbook_id=playbook_id, execution_id=execution_id)

        resultStructureMessage = ResultStructure(
            state=state, context=contextMessage, variables=variables)

        fin_id = str(uuid1())
        timestamp = datetime.now(timezone.utc).isoformat()
        metaMessage = Meta(sender_id=fin_id, timestamp=timestamp)

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

        contextMessage = Context(
            step_id=step_id, playbook_id=playbook_id, execution_id=execution_id)

        resultStructureMessage = ResultStructure(
            state=state, context=contextMessage, variables=variables)

        fin_id = str(uuid1())
        timestamp = datetime.now(timezone.utc).isoformat()
        metaMessage = Meta(sender_id=fin_id, timestamp=timestamp)

        message_id = str(uuid1())

        json_obj = {
            "type": "result",
            "message_id": message_id,
            "result": resultStructureMessage.model_dump(),
            "meta": metaMessage.model_dump(),
        }

        resultMessage = Result(
            result=resultStructureMessage, meta=metaMessage, message_id=message_id)

        json_str = resultMessage.model_dump_json()

        self.assertEqual(json.loads(json_str), json_obj)
