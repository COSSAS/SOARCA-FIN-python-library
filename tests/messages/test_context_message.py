import datetime
import json
import unittest
from uuid import uuid1

from soarca_fin_python_library.message_factory import generateContextMessage
from soarca_fin_python_library.models.context import Context


class TestContextMessage(unittest.TestCase):
    def test_context_message_generator_implicit(self):
        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        contextMessage = generateContextMessage(step_id, playbook_id, execution_id)

        self.assertEqual(step_id, contextMessage.step_id)
        self.assertEqual(playbook_id, contextMessage.playbook_id)
        self.assertEqual(execution_id, contextMessage.execution_id)

    def test_context_message_generator_explicit(self):
        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        completed_on = datetime.datetime.now().isoformat()
        generated_on = datetime.datetime.now().isoformat()
        timeout = datetime.datetime.now().isoformat()

        contextMessage = generateContextMessage(
            step_id, playbook_id, execution_id, completed_on, generated_on, timeout
        )

        self.assertEqual(step_id, contextMessage.step_id)
        self.assertEqual(playbook_id, contextMessage.playbook_id)
        self.assertEqual(execution_id, contextMessage.execution_id)

        self.assertEqual(completed_on, contextMessage.completed_on)
        self.assertEqual(generated_on, contextMessage.generated_on)
        self.assertEqual(timeout, contextMessage.timeout)

    def test_context_from_json(self):
        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        completed_on = datetime.datetime.now().isoformat()
        generated_on = datetime.datetime.now().isoformat()
        timeout = datetime.datetime.now().isoformat()

        json_obj = {
            "step_id": step_id,
            "playbook_id": playbook_id,
            "execution_id": execution_id,
            "completed_on": completed_on,
            "generated_on": generated_on,
            "timeout": timeout,
        }

        contextMessage = Context(**json_obj)

        self.assertEqual(step_id, contextMessage.step_id)
        self.assertEqual(playbook_id, contextMessage.playbook_id)
        self.assertEqual(execution_id, contextMessage.execution_id)

        self.assertEqual(completed_on, contextMessage.completed_on)
        self.assertEqual(generated_on, contextMessage.generated_on)
        self.assertEqual(timeout, contextMessage.timeout)

    def test_context_to_json(self):
        step_id = str(uuid1())
        playbook_id = str(uuid1())
        execution_id = str(uuid1())

        completed_on = datetime.datetime.now().isoformat()
        generated_on = datetime.datetime.now().isoformat()
        timeout = datetime.datetime.now().isoformat()

        json_obj = {
            "step_id": step_id,
            "playbook_id": playbook_id,
            "execution_id": execution_id,
            "completed_on": completed_on,
            "generated_on": generated_on,
            "timeout": timeout,
        }

        contextMessage = generateContextMessage(
            step_id, playbook_id, execution_id, completed_on, generated_on, timeout
        )

        json_str = contextMessage.model_dump_json()

        self.assertEqual(json.loads(json_str), json_obj)
