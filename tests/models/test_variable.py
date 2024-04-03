import json
import unittest

from soarca_fin_python_library.enums.variable_type_enum import VariableTypeEnum

from soarca_fin_python_library.models.variable import Variable


class TestVariable(unittest.TestCase):

    def test_variable_message_generator(self):
        variable_type = VariableTypeEnum.string
        name = "__var_name__"
        description = "test description"
        value = "test value"
        constant = True
        external = False

        variableMessage = Variable(
            type=variable_type, name=name, description=description, value=value, constant=constant, external=external)

        self.assertEqual(variable_type, variableMessage.type)
        self.assertEqual(description, variableMessage.description)
        self.assertEqual(value, variableMessage.value)
        self.assertEqual(constant, variableMessage.constant)
        self.assertEqual(external, variableMessage.external)

    def test_variable_message_from_json(self):
        variable_type = VariableTypeEnum.string
        name = "__var_name__"
        description = "test description"
        value = "test value"
        constant = True
        external = False

        json_obj = {
            "type": variable_type,
            "name": name,
            "description": description,
            "value": value,
            "constant": constant,
            "external": external,
        }

        variableMessage = Variable(**json_obj)

        self.assertEqual(variable_type, variableMessage.type)
        self.assertEqual(description, variableMessage.description)
        self.assertEqual(value, variableMessage.value)
        self.assertEqual(constant, variableMessage.constant)
        self.assertEqual(external, variableMessage.external)

    def test_variable_to_json(self):
        variable_type = VariableTypeEnum.string
        name = "__var_name__"
        description = "test description"
        value = "test value"
        constant = True
        external = False

        variableMessage = Variable(
            type=variable_type, name=name, description=description, value=value, constant=constant, external=external)

        json_str = variableMessage.model_dump_json()

        json_obj = {
            "type": variable_type,
            "name": name,
            "description": description,
            "value": value,
            "constant": constant,
            "external": external,
        }

        self.assertEqual(json.loads(json_str), json_obj)
