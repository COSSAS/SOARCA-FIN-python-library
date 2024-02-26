import unittest
import json
from uuid import uuid1

from messages.nackMessage import NackMessage
from messageFactory import generateNackMessage
from models.nack import Nack


class TestAckMessage(unittest.TestCase):

    def test_ack_message_generator(self):
        id = str(uuid1())
        nack = generateNackMessage(id)

        self.assertEqual(nack.type, "nack", "Type should be an nack")
        self.assertEqual(nack.message_id, id, "Message_id's should match")

    def test_json_to_nack(self):

        id = str(uuid1())

        json_obj = {
            "type": "nack",
            "message_id": id
        }

        nack = Nack(**json_obj)

        self.assertEqual(nack.type, "nack", "Type should be a nack")
        self.assertEqual(nack.message_id, id, "Message_id's should match")

    def test_ack_to_json(self):
        id = str(uuid1())
        nack = generateNackMessage(id)

        json_str = nack.model_dump_json()

        json_obj = {
            "message_id": id,
            "type": "nack",
        }

        self.assertEqual(json.loads(json_str), json_obj,
                         "Json objects should match")
