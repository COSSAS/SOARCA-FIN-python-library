import json
import unittest
from uuid import uuid1
from src.enums.workflow_step_enum import WorkFlowStepEnum

from src.message_factory import generateAgentStructureMessage, generateCapabilityStructureMessage, generateExternalReferenceMessage, generateStepStructureMessage
from src.models.agent_structure import AgentStructure
from src.models.step_structure import StepStructure
from src.models.external_reference import ExternalReference
from src.models.capability_structure import CapabilityStructure


class testCapabilityStructureMessage(unittest.TestCase):

    def test_capability_structure_generator(self):
        agent_name = "test"
        uuid_agent = str(uuid1())
        agentStructure = generateAgentStructureMessage(agent_name, uuid_agent)

        ext_name = "test"
        externalReference = generateExternalReferenceMessage(ext_name)

        type = "action"
        step_name = "test step"
        description = "test description"
        command = "test command"
        target = str(uuid1())

        stepStructure = generateStepStructureMessage(
            type, step_name, description, [externalReference], command, target)

        capability_id = str(uuid1())
        type = WorkFlowStepEnum.action
        capability_name = "test name"
        version = "0.0.1"

        capabilityStructure = generateCapabilityStructureMessage(
            capability_id, type, capability_name, version, stepStructure, agentStructure)

        self.assertEqual(capabilityStructure.capability_id, capability_id)
        self.assertEqual(capabilityStructure.type, type)
        self.assertEqual(capabilityStructure.name, capability_name)
        self.assertEqual(capabilityStructure.version, version)

        self.assertIsInstance(capabilityStructure.agent, AgentStructure)
        self.assertEqual(capabilityStructure.agent.name,
                         f"soarca-fin--{agent_name}-{uuid_agent}")

        self.assertIsInstance(capabilityStructure.step, StepStructure)
        self.assertIsInstance(
            capabilityStructure.step.external_references[0], ExternalReference)

    def test_json_to_capability_structure_message(self):
        agent_name = "test"
        uuid_agent = str(uuid1())
        agentStructure = generateAgentStructureMessage(agent_name, uuid_agent)

        ext_name = "test"
        externalReference = generateExternalReferenceMessage(ext_name)

        type = "action"
        step_name = "test step"
        description = "test description"
        command = "test command"
        target = str(uuid1())

        stepStructure = generateStepStructureMessage(
            type, step_name, description, [externalReference], command, target)

        capability_id = str(uuid1())
        type = WorkFlowStepEnum.action
        capability_name = "test name"
        version = "0.0.1"

        json_object = {
            "capability_id": capability_id,
            "type": type,
            "name": capability_name,
            "version": version,
            "agent": agentStructure.model_dump(),
            "step": stepStructure.model_dump(),
        }

        capabilityStructure = CapabilityStructure(**json_object)

        self.assertEqual(capabilityStructure.capability_id, capability_id)
        self.assertEqual(capabilityStructure.type, type)
        self.assertEqual(capabilityStructure.name, capability_name)
        self.assertEqual(capabilityStructure.version, version)

        self.assertIsInstance(capabilityStructure.agent, AgentStructure)
        self.assertEqual(capabilityStructure.agent.name,
                         f"soarca-fin--{agent_name}-{uuid_agent}")

        self.assertIsInstance(capabilityStructure.step, StepStructure)
        self.assertIsInstance(
            capabilityStructure.step.external_references[0], ExternalReference)

    def test_capability_structure_to_json(self):
        agent_name = "test"
        uuid_agent = str(uuid1())
        agentStructure = generateAgentStructureMessage(agent_name, uuid_agent)

        ext_name = "test"
        externalReference = generateExternalReferenceMessage(ext_name)

        type = "action"
        step_name = "test step"
        description = "test description"
        command = "test command"
        target = str(uuid1())

        stepStructure = generateStepStructureMessage(
            type, step_name, description, [externalReference], command, target)

        capability_id = str(uuid1())
        type = WorkFlowStepEnum.action
        capability_name = "test name"
        version = "0.0.1"

        capabilityStructure = generateCapabilityStructureMessage(
            capability_id, type, capability_name, version, stepStructure, agentStructure)

        json_str = capabilityStructure.model_dump_json()

        json_object = {
            "capability_id": capability_id,
            "type": type,
            "name": capability_name,
            "version": version,
            "agent": agentStructure.model_dump(),
            "step": stepStructure.model_dump(),
        }

        self.assertEqual(json.loads(json_str), json_object)
