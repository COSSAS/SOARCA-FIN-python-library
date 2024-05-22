from datetime import datetime, timezone
import json
import unittest
from uuid import uuid1


from soarca_fin_python_library.models.meta import Meta


class testMetaMessage(unittest.TestCase):
    def test_meta_message_generator(self):
        message_id = str(uuid1())
        timestamp = datetime.now(timezone.utc).isoformat()
        metaMessage = Meta(sender_id=message_id, timestamp=timestamp)

        self.assertEqual(metaMessage.sender_id, message_id)
        self.assertIsNotNone(metaMessage.timestamp)
        self.assertEqual(metaMessage.timestamp, timestamp)

    def test_json_to_meta_message(self):
        message_id = str(uuid1())
        timestamp = datetime.now(timezone.utc).isoformat()

        json_object = {
            "sender_id": message_id,
            "timestamp": timestamp,
        }

        metaMessage = Meta(**json_object)

        self.assertEqual(metaMessage.sender_id, message_id)
        self.assertEqual(metaMessage.timestamp, timestamp)

    def test_meta_message_to_json(self):
        message_id = str(uuid1())
        timestamp = datetime.now(timezone.utc).isoformat()
        metaMessage = Meta(sender_id=message_id, timestamp=timestamp)

        json_str = metaMessage.model_dump_json()

        json_object = {
            "sender_id": message_id,
            "timestamp": timestamp,
        }

        self.assertEqual(json.loads(json_str), json_object)
