import json
import unittest

from src.enums.auth_type_enum import AuthTypeEnum
from src.message_factory import generateAuthenticationInformationMessage
from src.models.authentication_information import AuthenticationInformation


class TestAuthenticationInformationMessage(unittest.TestCase):

    def test_authentication_information_message_generator_implicit(self):

        type = AuthTypeEnum.http_basic

        aiMessage = generateAuthenticationInformationMessage(type=type)

        self.assertEqual(aiMessage.type, type)
        self.assertIsNone(aiMessage.name)
        self.assertIsNone(aiMessage.description)
        self.assertIsNone(aiMessage.authentication_info_extensions)

    def test_authentication_information_message_generator_explicit(self):

        type = AuthTypeEnum.http_basic
        ai_name = "test name"
        ai_description = "test description"
        ai_extensions = {"key": "value"}

        aiMessage = generateAuthenticationInformationMessage(
            type, ai_name, ai_description, ai_extensions)

        self.assertEqual(aiMessage.type, type)
        self.assertEqual(aiMessage.name, ai_name)
        self.assertEqual(aiMessage.description, ai_description)
        self.assertEqual(
            aiMessage.authentication_info_extensions, ai_extensions)

    def test_authentication_information_from_json(self):
        type = AuthTypeEnum.http_basic
        ai_name = "test name"
        ai_description = "test description"
        ai_extensions = {"key": "value"}

        json_obj = {
            "type": type,
            "name": ai_name,
            "description": ai_description,
            "authentication_info_extensions": ai_extensions,
        }

        aiMessage = AuthenticationInformation(**json_obj)

        self.assertEqual(aiMessage.type, type)
        self.assertEqual(aiMessage.name, ai_name)
        self.assertEqual(aiMessage.description, ai_description)
        self.assertEqual(
            aiMessage.authentication_info_extensions, ai_extensions)

    def test_authentication_to_json(self):
        type = AuthTypeEnum.http_basic
        ai_name = "test name"
        ai_description = "test description"
        ai_extensions = {"key": "value"}

        json_obj = {
            "type": type,
            "name": ai_name,
            "description": ai_description,
            "authentication_info_extensions": ai_extensions,
        }

        aiMessage = generateAuthenticationInformationMessage(
            type, ai_name, ai_description, ai_extensions)

        json_str = aiMessage.model_dump_json()

        self.assertEqual(json.loads(json_str), json_obj)
