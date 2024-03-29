import json
import unittest

from soarca_fin_python_library.message_factory import generateSecurityMessage
from soarca_fin_python_library.models.security import Security


class testSecurityMessage(unittest.TestCase):

    def test_security_message_generator(self):
        version = "0.0.1"
        channel_security = "plaintext"

        securityMessage = generateSecurityMessage(version, channel_security)

        self.assertEqual(securityMessage.version, version)
        self.assertEqual(securityMessage.channel_security, channel_security)

    def test_json_to_security_message(self):
        version = "0.0.1"
        channel_security = "plaintext"

        json_obj = {
            "version": version,
            "channel_security": channel_security,
        }

        securityMessage = Security(**json_obj)

        self.assertEqual(securityMessage.version, version)
        self.assertEqual(securityMessage.channel_security, channel_security)

    def test_security_message_to_json(self):
        version = "0.0.1"
        channel_security = "plaintext"

        securityMessage = generateSecurityMessage(version, channel_security)

        json_str = securityMessage.model_dump_json()

        json_obj = {
            "version": version,
            "channel_security": channel_security,
        }

        self.assertEqual(json.loads(json_str), json_obj)
