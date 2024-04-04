import unittest
import json
from uuid import uuid1


from soarca_fin_python_library.models.external_reference import ExternalReference
from soarca_fin_python_library.models.step_structure import StepStructure


class testStepStructureMessage(unittest.TestCase):
    def test_step_structure_generator(self):
        ext_name = "test"
        externalReference = ExternalReference(name=ext_name)

        step_type = "action"
        step_name = "test step"
        description = "test description"
        command = "test command"
        target = str(uuid1())

        stepStructureMessage = StepStructure(
            type=step_type, name=step_name, description=description, external_references=externalReference, command=command, target=target)

        self.assertEqual(stepStructureMessage.type, step_type,
                         "Types should be the same")
        self.assertEqual(stepStructureMessage.name, step_name,
                         "Names should be the same")
        self.assertEqual(stepStructureMessage.description,
                         description, "Descriptions should be the same")
        self.assertEqual(stepStructureMessage.command,
                         command, "Commands should be the same")
        self.assertEqual(stepStructureMessage.target, target,
                         "Targets should be the same")
        self.assertIsInstance(stepStructureMessage.external_references, ExternalReference,
                              "External references should be of external references type")
        self.assertEqual(stepStructureMessage.external_references.name,
                         ext_name, "External references names should match")

    def test_json_to_step_structure_message(self):
        ext_name = "test"
        externalReference = ExternalReference(name=ext_name)

        step_type = "action"
        step_name = "test step"
        description = "test description"
        command = "test command"
        target = str(uuid1())

        json_object = {
            "type": step_type,
            "name": step_name,
            "description": description,
            "command": command,
            "target": target,
            "external_references": externalReference.model_dump()
        }

        stepStructureMessage = StepStructure(**json_object)

        self.assertEqual(stepStructureMessage.type, step_type,
                         "Types should be the same")
        self.assertEqual(stepStructureMessage.name, step_name,
                         "Names should be the same")
        self.assertEqual(stepStructureMessage.description,
                         description, "Descriptions should be the same")
        self.assertEqual(stepStructureMessage.command,
                         command, "Commands should be the same")
        self.assertEqual(stepStructureMessage.target, target,
                         "Targets should be the same")

        self.assertIsInstance(stepStructureMessage.external_references, ExternalReference,
                              "External references should be of external references type")
        self.assertEqual(stepStructureMessage.external_references.name,
                         ext_name, "External references names should match")

    def test_step_structure_to_json(self):
        ext_name = "test"
        externalReference = ExternalReference(name=ext_name)

        step_type = "action"
        step_name = "test step"
        description = "test description"
        command = "test command"
        target = str(uuid1())

        stepStructureMessage = StepStructure(
            type=step_type, name=step_name, description=description, external_references=externalReference, command=command, target=target)

        json_str = stepStructureMessage.model_dump_json()

        json_object = {
            "type": step_type,
            "name": step_name,
            "description": description,
            "command": command,
            "target": target,
            "external_references": externalReference.model_dump()
        }

        self.assertEqual(json.loads(json_str), json_object,
                         "Json objects should match")
