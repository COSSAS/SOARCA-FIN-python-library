import json
import unittest
from uuid import uuid1
from soarca_fin_python_library.enums.workflow_step_enum import WorkFlowStepEnum

from soarca_fin_python_library.models.agent_structure import AgentStructure
from soarca_fin_python_library.models.step_structure import StepStructure
from soarca_fin_python_library.models.external_reference import ExternalReference
from soarca_fin_python_library.models.capability_structure import CapabilityStructure


class testCapabilityStructureMessage(unittest.TestCase):

    def test_capability_structure_generator(self):
        agent_name = "test"
        uuid_agent = str(uuid1())
        name = f"soarca-fin--{agent_name}-{uuid_agent}"
        agentStructure = AgentStructure(name=name)

        ext_name = "test"
        externalReference = ExternalReference(name=ext_name)

        step_name = "test step"
        description = "test description"
        command = "test command"
        target = str(uuid1())

        stepStructure = StepStructure(name=step_name, description=description, external_references=[
                                      externalReference], command=command, target=target)

        capability_id = str(uuid1())
        capability_type = WorkFlowStepEnum.action
        capability_name = "test name"
        version = "0.0.1"

        capabilityStructure = CapabilityStructure(
            capability_id=capability_id, type=capability_type, name=capability_name, version=version, step={"step": stepStructure}, agent={"agent": agentStructure})

        self.assertEqual(capabilityStructure.capability_id, capability_id)
        self.assertEqual(capabilityStructure.type, capability_type)
        self.assertEqual(capabilityStructure.name, capability_name)
        self.assertEqual(capabilityStructure.version, version)

        self.assertIsInstance(
            capabilityStructure.agent["agent"], AgentStructure)
        self.assertEqual(capabilityStructure.agent["agent"].name,
                         f"soarca-fin--{agent_name}-{uuid_agent}")

        self.assertIsInstance(capabilityStructure.step["step"], StepStructure)
        self.assertIsInstance(
            capabilityStructure.step["step"].external_references[0],
            ExternalReference)

    def test_json_to_capability_structure_message(self):
        agent_name = "test"
        uuid_agent = str(uuid1())
        name = f"soarca-fin--{agent_name}-{uuid_agent}"
        agentStructure = AgentStructure(name=name)

        ext_name = "test"
        externalReference = ExternalReference(name=ext_name)

        step_name = "test step"
        description = "test description"
        command = "test command"
        target = str(uuid1())

        stepStructure = StepStructure(name=step_name, description=description, external_references=[
                                      externalReference], command=command, target=target)

        capability_id = str(uuid1())
        capability_type = WorkFlowStepEnum.action
        capability_name = "test name"
        version = "0.0.1"

        json_object = {
            "capability_id": capability_id,
            "type": capability_type,
            "name": capability_name,
            "version": version,
            "agent": {"agent": agentStructure.model_dump()},
            "step": {"step": stepStructure.model_dump()},
        }

        capabilityStructure = CapabilityStructure(**json_object)

        self.assertEqual(capabilityStructure.capability_id, capability_id)
        self.assertEqual(capabilityStructure.type, capability_type)
        self.assertEqual(capabilityStructure.name, capability_name)
        self.assertEqual(capabilityStructure.version, version)

        self.assertIsInstance(
            capabilityStructure.agent["agent"], AgentStructure)
        self.assertEqual(capabilityStructure.agent["agent"].name,
                         f"soarca-fin--{agent_name}-{uuid_agent}")

        self.assertIsInstance(capabilityStructure.step["step"], StepStructure)
        self.assertIsInstance(
            capabilityStructure.step["step"].external_references[0], ExternalReference)

    def test_capability_structure_to_json(self):
        agent_name = "test"
        uuid_agent = str(uuid1())
        name = f"soarca-fin--{agent_name}-{uuid_agent}"
        agentStructure = AgentStructure(name=name)

        ext_name = "test"
        externalReference = ExternalReference(name=ext_name)

        step_name = "test step"
        description = "test description"
        command = "test command"
        target = str(uuid1())

        stepStructure = StepStructure(name=step_name, description=description, external_references=[
                                      externalReference], command=command, target=target)

        capability_id = str(uuid1())
        capability_type = WorkFlowStepEnum.action
        capability_name = "test name"
        version = "0.0.1"

        capabilityStructure = CapabilityStructure(
            capability_id=capability_id, type=capability_type, name=capability_name, version=version, step={"step": stepStructure}, agent={"agent": agentStructure})

        json_str = capabilityStructure.model_dump_json()

        json_object = {
            "capability_id": capability_id,
            "type": capability_type,
            "name": capability_name,
            "version": version,
            "agent": {"agent": agentStructure.model_dump()},
            "step": {"step": stepStructure.model_dump()},
        }

        self.assertEqual(json.loads(json_str), json_object)
