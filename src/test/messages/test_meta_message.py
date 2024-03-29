import datetime
import json
import unittest
from uuid import uuid1

from src.message_factory import generateMetaMessage
from models.meta import Meta


class testMetaMessage(unittest.TestCase):

    def test_meta_message_generator_implicit(self):
        id = str(uuid1())
        metaMessage = generateMetaMessage(id)

        datetime_now = datetime.datetime.now()
        datetime_object = datetime.datetime.fromisoformat(
            metaMessage.timestamp)

        self.assertEqual(metaMessage.sender_id, id)
        self.assertIsNotNone(metaMessage.timestamp)
        self.assertTrue(datetime_object < datetime_now)

    def test_meta_message_generator_explicit(self):
        id = str(uuid1())
        timestamp = datetime.datetime.now().isoformat()
        metaMessage = generateMetaMessage(id, timestamp)

        self.assertEqual(metaMessage.sender_id, id)
        self.assertIsNotNone(metaMessage.timestamp)
        self.assertEqual(metaMessage.timestamp, timestamp)

    def test_json_to_meta_message(self):
        id = str(uuid1())
        timestamp = datetime.datetime.now().isoformat()

        json_object = {
            "sender_id": id,
            "timestamp": timestamp,
        }

        metaMessage = Meta(**json_object)

        self.assertEqual(metaMessage.sender_id, id)
        self.assertEqual(metaMessage.timestamp, timestamp)

    def test_meta_message_to_json(self):
        id = str(uuid1())
        timestamp = datetime.datetime.now().isoformat()
        metaMessage = generateMetaMessage(id, timestamp)

        json_str = metaMessage.model_dump_json()

        json_object = {
            "sender_id": id,
            "timestamp": timestamp,
        }

        self.assertEqual(json.loads(json_str), json_object)
