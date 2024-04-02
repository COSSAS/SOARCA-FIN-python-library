import unittest
import json
from uuid import uuid1
from soarca_fin_python_library.models.ack import Ack


class TestAckMessage(unittest.TestCase):

    def test_ack_message_generator(self):
        id = str(uuid1())
        ack = Ack(message_id=id)
        self.assertEqual(ack.type, "ack", "Type should be an ack")
        self.assertEqual(ack.message_id, id, "Message_id's should match")

    def test_json_to_ack(self):

        id = str(uuid1())

        json_obj = {
            "type": "ack",
            "message_id": id
        }

        ack = Ack(**json_obj)

        self.assertEqual(ack.type, "ack", "Type should be an ack")
        self.assertEqual(ack.message_id, id, "Message_id's should match")

    def test_ack_to_json(self):
        id = str(uuid1())
        ack = Ack(message_id=id)

        json_str = ack.model_dump_json()

        json_obj = {
            "message_id": id,
            "type": "ack",
        }

        self.assertEqual(json.loads(json_str), json_obj,
                         "Json objects should match")
