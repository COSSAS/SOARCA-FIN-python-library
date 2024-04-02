import json
import unittest
from uuid import uuid1
from soarca_fin_python_library.enums.workflow_step_enum import WorkFlowStepEnum

from soarca_fin_python_library.models.security import Security
from soarca_fin_python_library.models.agent_structure import AgentStructure
from soarca_fin_python_library.models.external_reference import ExternalReference
from soarca_fin_python_library.models.capability_structure import CapabilityStructure
from soarca_fin_python_library.models.register import Register
from soarca_fin_python_library.models.step_structure import StepStructure
from soarca_fin_python_library.models.meta import Meta


class testRegisterMessage(unittest.TestCase):

    def test_register_message_generator(self):

        security_version = "0.0.1"
        channel_security = "plaintext"
        securityMessage = Security(
            security_version, channel_security)

        agent_name = "test"
        uuid_agent = str(uuid1())
        agentStructure = AgentStructure(agent_name, uuid_agent)

        ext_name = "test"
        externalReference = ExternalReference(ext_name)

        type = "action"
        step_name = "test step"
        description = "test description"
        command = "test command"
        target = str(uuid1())

        stepStructure = StepStructure(
            type, step_name, description, [externalReference], command, target)

        capability_id = str(uuid1())
        type = WorkFlowStepEnum.action
        capability_name = "test name"
        version = "0.0.1"

        capabilityStructure = CapabilityStructure(
            capability_id, type, capability_name, version, stepStructure, agentStructure)

        fin_id = str(uuid1())
        protocol_version = "test version"

        registerMessage = Register(
            fin_id, protocol_version, securityMessage, [capabilityStructure])

        self.assertEqual(registerMessage.type, "register")
        self.assertEqual(registerMessage.fin_id, fin_id)
        self.assertIsNotNone(registerMessage.message_id)
        self.assertEqual(registerMessage.protocol_version, protocol_version)
        self.assertEqual(registerMessage.security, securityMessage)
        self.assertIsNotNone(registerMessage.meta)

    def test_json_to_register_message(self):
        security_version = "0.0.1"
        channel_security = "plaintext"
        securityMessage = Security(
            security_version, channel_security)

        agent_name = "test"
        uuid_agent = str(uuid1())
        agentStructure = AgentStructure(agent_name, uuid_agent)

        ext_name = "test"
        externalReference = ExternalReference(ext_name)

        type = "action"
        step_name = "test step"
        description = "test description"
        command = "test command"
        target = str(uuid1())

        stepStructure = StepStructure(
            type, step_name, description, [externalReference], command, target)

        capability_id = str(uuid1())
        type = WorkFlowStepEnum.action
        capability_name = "test name"
        version = "0.0.1"

        capabilityStructure = CapabilityStructure(
            capability_id, type, capability_name, version, stepStructure, agentStructure)

        fin_id = str(uuid1())
        message_id = str(uuid1())
        protocol_version = "test version"

        meta = Meta(fin_id)

        registerMessage = Register(fin_id, protocol_version, securityMessage, [
            capabilityStructure], meta, message_id)

        json_object = {
            "type": "register",
            "message_id": message_id,
            "fin_id": fin_id,
            "protocol_version": protocol_version,
            "security": securityMessage.model_dump(),
            "capabilities": [capabilityStructure.model_dump()],
            "meta": meta.model_dump()
        }

        json_str = registerMessage.model_dump_json()

        self.assertEqual(json.loads(json_str), json_object)
