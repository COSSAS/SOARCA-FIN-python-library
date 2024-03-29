import unittest
import json
from uuid import uuid1

from src.message_factory import generateExternalReferenceMessage, generateStepStructureMessage
from src.models.external_reference import ExternalReference
from src.models.step_structure import StepStructure


class testStepStructureMessage(unittest.TestCase):
    def test_step_structure_generator(self):
        ext_name = "test"
        externalReference = generateExternalReferenceMessage(ext_name)

        type = "action"
        step_name = "test step"
        description = "test description"
        command = "test command"
        target = str(uuid1())

        stepStructureMessage = generateStepStructureMessage(
            type, step_name, description, [externalReference], command, target)

        self.assertEqual(stepStructureMessage.type, type,
                         "Types should be the same")
        self.assertEqual(stepStructureMessage.name, step_name,
                         "Names should be the same")
        self.assertEqual(stepStructureMessage.description,
                         description, "Descriptions should be the same")
        self.assertEqual(stepStructureMessage.command,
                         command, "Commands should be the same")
        self.assertEqual(stepStructureMessage.target, target,
                         "Targets should be the same")
        self.assertIsInstance(stepStructureMessage.external_references[0], ExternalReference,
                              "External references should be of external references type")
        self.assertEqual(stepStructureMessage.external_references[0].name,
                         ext_name, "External references names should match")

    def test_json_to_step_structure_message(self):
        ext_name = "test"
        externalReference = generateExternalReferenceMessage(ext_name)

        type = "action"
        step_name = "test step"
        description = "test description"
        command = "test command"
        target = str(uuid1())

        json_object = {
            "type": type,
            "name": step_name,
            "description": description,
            "command": command,
            "target": target,
            "external_references": [externalReference.model_dump()]
        }

        stepStructureMessage = StepStructure(**json_object)

        self.assertEqual(stepStructureMessage.type, type,
                         "Types should be the same")
        self.assertEqual(stepStructureMessage.name, step_name,
                         "Names should be the same")
        self.assertEqual(stepStructureMessage.description,
                         description, "Descriptions should be the same")
        self.assertEqual(stepStructureMessage.command,
                         command, "Commands should be the same")
        self.assertEqual(stepStructureMessage.target, target,
                         "Targets should be the same")

        self.assertIsInstance(stepStructureMessage.external_references[0], ExternalReference,
                              "External references should be of external references type")
        self.assertEqual(stepStructureMessage.external_references[0].name,
                         ext_name, "External references names should match")

    def test_step_structure_to_json(self):
        ext_name = "test"
        externalReference = generateExternalReferenceMessage(ext_name)

        type = "action"
        step_name = "test step"
        description = "test description"
        command = "test command"
        target = str(uuid1())

        stepStructureMessage = generateStepStructureMessage(
            type, step_name, description, [externalReference], command, target)

        json_str = stepStructureMessage.model_dump_json()

        json_object = {
            "type": type,
            "name": step_name,
            "description": description,
            "command": command,
            "target": target,
            "external_references": [externalReference.model_dump()]
        }

        self.assertEqual(json.loads(json_str), json_object,
                         "Json objects should match")
