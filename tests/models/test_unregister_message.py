import json
import unittest
from uuid import uuid1


from soarca_fin_python_library.models.unregister import Unregister


class TestUnregisterMessage(unittest.TestCase):
    def test_unregister_message_generator_all(self):
        message_id = str(uuid1())
        register_all = True

        unregisterMessage = Unregister(message_id=message_id, all=register_all)

        self.assertEqual("unregister", unregisterMessage.type)
        self.assertEqual(register_all, unregisterMessage.all)
        self.assertIsNone(unregisterMessage.capability_id)
        self.assertIsNone(unregisterMessage.fin_id)
        self.assertIsNotNone(unregisterMessage.message_id)

    def test_unregister_message_generator_capability(self):
        capability_id = str(uuid1())
        message_id = str(uuid1())
        unregisterMessage = Unregister(
            message_id=message_id, capability_id=capability_id
        )

        self.assertEqual("unregister", unregisterMessage.type)
        self.assertEqual(False, unregisterMessage.all)
        self.assertEqual(capability_id, unregisterMessage.capability_id)
        self.assertIsNone(unregisterMessage.fin_id)
        self.assertIsNotNone(unregisterMessage.message_id)

    def test_unregister_message_generator_fin(self):
        fin_id = str(uuid1())
        message_id = str(uuid1())
        unregisterMessage = Unregister(message_id=message_id, fin_id=fin_id)

        self.assertEqual("unregister", unregisterMessage.type)
        self.assertEqual(False, unregisterMessage.all)
        self.assertEqual(fin_id, unregisterMessage.fin_id)
        self.assertIsNone(unregisterMessage.capability_id)
        self.assertIsNotNone(unregisterMessage.message_id)

    def test_json_to_unregister_message(self):
        message_id = str(uuid1())
        capability_id = None
        fin_id = str(uuid1())
        register_all = False

        json_object = {
            "type": "unregister",
            "message_id": message_id,
            "capability_id": capability_id,
            "fin_id": fin_id,
            "all": register_all,
        }

        unregisterMessage = Unregister(**json_object)

        self.assertEqual("unregister", unregisterMessage.type)
        self.assertEqual(False, unregisterMessage.all)
        self.assertEqual(fin_id, unregisterMessage.fin_id)
        self.assertIsNone(unregisterMessage.capability_id)
        self.assertIsNotNone(unregisterMessage.message_id)

    def test_unregister_to_json(self):
        message_id = str(uuid1())
        capability_id = None
        fin_id = str(uuid1())
        register_all = False

        unregisterMessage = Unregister(fin_id=fin_id, message_id=message_id)

        json_str = unregisterMessage.model_dump_json()

        json_object = {
            "type": "unregister",
            "message_id": message_id,
            "capability_id": capability_id,
            "fin_id": fin_id,
            "all": register_all,
        }

        self.assertEqual(json.loads(json_str), json_object)
