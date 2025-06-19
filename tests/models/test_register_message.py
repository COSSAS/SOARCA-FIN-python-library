from datetime import datetime, timezone
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
            version=security_version, channel_security=channel_security
        )

        agent_name = "test"
        uuid_agent = str(uuid1())
        name = f"soarca-fin--{agent_name}-{uuid_agent}"
        agentStructure = AgentStructure(name=name)

        ext_name = "test"
        externalReference = ExternalReference(name=ext_name)

        step_type = "action"
        step_name = "test step"
        description = "test description"
        command = "test command"
        target = str(uuid1())

        stepStructure = StepStructure(
            type=step_type,
            name=step_name,
            description=description,
            external_references=[externalReference],
            command=command,
            target=target,
        )

        capability_id = str(uuid1())
        capability_type = WorkFlowStepEnum.action
        capability_name = "test name"
        version = "0.0.1"

        capabilityStructure = CapabilityStructure(
            capability_id=capability_id,
            type=capability_type,
            name=capability_name,
            version=version,
            step={"step": stepStructure},
            agent={"agent": agentStructure},
        )

        message_id = str(uuid1())
        fin_id = str(uuid1())
        protocol_version = "test version"

        meta_id = str(uuid1())
        timestamp = datetime.now(timezone.utc).isoformat()
        metaMessage = Meta(timestamp=timestamp, sender_id=meta_id)

        registerMessage = Register(
            message_id=message_id,
            fin_id=fin_id,
            protocol_version=protocol_version,
            security=securityMessage,
            capabilities=[capabilityStructure],
            meta=metaMessage,
        )

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
            version=security_version, channel_security=channel_security
        )

        agent_name = "test"
        uuid_agent = str(uuid1())
        name = f"soarca-fin--{agent_name}-{uuid_agent}"
        agentStructure = AgentStructure(name=name)

        ext_name = "test"
        externalReference = ExternalReference(name=ext_name)

        step_type = "action"
        step_name = "test step"
        description = "test description"
        command = "test command"
        target = str(uuid1())

        stepStructure = StepStructure(
            type=step_type,
            name=step_name,
            description=description,
            external_references=[externalReference],
            command=command,
            target=target,
        )

        capability_id = str(uuid1())
        capability_type = WorkFlowStepEnum.action
        capability_name = "test name"
        version = "0.0.1"

        capabilityStructure = CapabilityStructure(
            capability_id=capability_id,
            type=capability_type,
            name=capability_name,
            version=version,
            step={"step": stepStructure},
            agent={"agent": agentStructure},
        )

        fin_id = str(uuid1())
        message_id = str(uuid1())
        protocol_version = "test version"

        timestamp = datetime.now(timezone.utc).isoformat()
        meta = Meta(sender_id=fin_id, timestamp=timestamp)

        registerMessage = Register(
            fin_id=fin_id,
            protocol_version=protocol_version,
            security=securityMessage,
            capabilities=[capabilityStructure],
            meta=meta,
            message_id=message_id,
        )

        json_object = {
            "type": "register",
            "message_id": message_id,
            "fin_id": fin_id,
            "protocol_version": protocol_version,
            "security": securityMessage.model_dump(),
            "capabilities": [capabilityStructure.model_dump()],
            "meta": meta.model_dump(),
        }

        json_str = registerMessage.model_dump_json()

        self.assertEqual(json.loads(json_str), json_object)
