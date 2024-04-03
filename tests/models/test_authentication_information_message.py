import json
import unittest

from soarca_fin_python_library.enums.auth_type_enum import AuthTypeEnum
from soarca_fin_python_library.models.authentication_information import AuthenticationInformation


class TestAuthenticationInformationMessage(unittest.TestCase):

    def test_authentication_information_message_generator_implicit(self):

        auth_type = AuthTypeEnum.http_basic

        aiMessage = AuthenticationInformation(id="some", type=auth_type)

        self.assertEqual(aiMessage.type, auth_type)
        self.assertIsNone(aiMessage.name)
        self.assertIsNone(aiMessage.description)
        self.assertIsNone(aiMessage.authentication_info_extensions)

    def test_authentication_information_message_generator_explicit(self):

        auth_type = AuthTypeEnum.http_basic
        ai_name = "test name"
        ai_description = "test description"
        ai_extensions = {"key": "value"}

        aiMessage = AuthenticationInformation(id="someid",
                                              type=auth_type,
                                              name=ai_name,
                                              description=ai_description,
                                              authentication_info_extensions=ai_extensions)

        self.assertEqual(aiMessage.type, auth_type)
        self.assertEqual(aiMessage.name, ai_name)
        self.assertEqual(aiMessage.description, ai_description)
        self.assertEqual(
            aiMessage.authentication_info_extensions, ai_extensions)

    def test_authentication_information_from_json(self):
        auth_type = AuthTypeEnum.http_basic
        ai_name = "test name"
        ai_description = "test description"
        ai_extensions = {"key": "value"}

        json_obj = {
            "type": auth_type,
            "id": "someid",
            "name": ai_name,
            "description": ai_description,
            "authentication_info_extensions": ai_extensions,
        }

        aiMessage = AuthenticationInformation(**json_obj)

        self.assertEqual(aiMessage.type, auth_type)
        self.assertEqual(aiMessage.name, ai_name)
        self.assertEqual(aiMessage.description, ai_description)
        self.assertEqual(
            aiMessage.authentication_info_extensions, ai_extensions)

    def test_authentication_to_json(self):
        auth_type = AuthTypeEnum.http_basic
        auth_id = "someID"
        ai_name = "test name"
        ai_description = "test description"
        ai_extensions = {"key": "value"}

        json_obj = {
            "id": "someID",
            "type": auth_type.value,
            "name": ai_name,
            "description": ai_description,
            "authentication_info_extensions": ai_extensions,
        }

        aiMessage = AuthenticationInformation(
            id=auth_id,
            type=auth_type,
            name=ai_name,
            description=ai_description,
            authentication_info_extensions=ai_extensions)

        json_str = aiMessage.model_dump_json(exclude_none=True)

        self.assertEqual(json.loads(json_str), json_obj)
