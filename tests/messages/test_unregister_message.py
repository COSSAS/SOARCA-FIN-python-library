import json
import unittest
from uuid import uuid1


from soarca_fin_python_library.models.unregister import Unregister


class TestUnregisterMessage(unittest.TestCase):

    def test_unregister_message_generator_invalid(self):

        self.assertRaises(ValueError, Unregister)

    def test_unregister_message_generator_all(self):
        all = True

        unregisterMessage = Unregister(all)

        self.assertEqual("unregister", unregisterMessage.type)
        self.assertEqual(all, unregisterMessage.all)
        self.assertIsNone(unregisterMessage.capability_id)
        self.assertIsNone(unregisterMessage.fin_id)
        self.assertIsNotNone(unregisterMessage.message_id)

    def test_unregister_message_generator_capability(self):
        capability_id = str(uuid1())

        unregisterMessage = Unregister(
            capability_id=capability_id)

        self.assertEqual("unregister", unregisterMessage.type)
        self.assertEqual(False, unregisterMessage.all)
        self.assertEqual(capability_id, unregisterMessage.capability_id)
        self.assertIsNone(unregisterMessage.fin_id)
        self.assertIsNotNone(unregisterMessage.message_id)

    def test_unregister_message_generator_fin(self):
        fin_id = str(uuid1())

        unregisterMessage = Unregister(
            fin_id=fin_id)

        self.assertEqual("unregister", unregisterMessage.type)
        self.assertEqual(False, unregisterMessage.all)
        self.assertEqual(fin_id, unregisterMessage.fin_id)
        self.assertIsNone(unregisterMessage.capability_id)
        self.assertIsNotNone(unregisterMessage.message_id)

    def test_json_to_unregister_message(self):

        message_id = str(uuid1())
        capability_id = None
        fin_id = str(uuid1())
        all = False

        json_object = {
            "type": "unregister",
            "message_id": message_id,
            "capability_id": capability_id,
            "fin_id": fin_id,
            "all": all,
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
        all = False

        unregisterMessage = Unregister(
            fin_id=fin_id, message_id=message_id)

        json_str = unregisterMessage.model_dump_json()

        json_object = {
            "type": "unregister",
            "message_id": message_id,
            "capability_id": capability_id,
            "fin_id": fin_id,
            "all": all,
        }

        self.assertEqual(json.loads(json_str), json_object)
