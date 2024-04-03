import unittest
import json
from uuid import uuid1
from soarca_fin_python_library.message_factory import generateAgentStructureMessage
from soarca_fin_python_library.models.agent_structure import AgentStructure


class TestAgentStructureMessage(unittest.TestCase):
    def test_agent_structure_message_generator(self):
        name = "test"
        id = str(uuid1())
        agentStructure = generateAgentStructureMessage(name, id)

        self.assertEqual(
            agentStructure.type, "soarca-fin", "Type should be an soarca-fin"
        )
        self.assertEqual(
            agentStructure.name, f"soarca-fin--{name}-{id}", "Names should match"
        )

    def test_json_to_agent_structure(self):
        name = "test"
        id = str(uuid1())
        json_obj = {"type": "soarca-fin", "name": f"soarca-fin--{name}-{id}"}

        agent = AgentStructure(**json_obj)

        self.assertEqual(agent.type, "soarca-fin", "Type should be an soarca-fin")
        self.assertEqual(agent.name, f"soarca-fin--{name}-{id}", "Names should match")

    def test_agent_structure_to_json(self):
        name = "test"
        id = str(uuid1())
        agent = generateAgentStructureMessage(name, id)

        json_str = agent.model_dump_json()

        json_obj = {
            "type": "soarca-fin",
            "name": f"soarca-fin--{name}-{id}",
        }

        self.assertEqual(json.loads(json_str), json_obj, "Json objects should match")
