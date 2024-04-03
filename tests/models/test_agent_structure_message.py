import unittest
import json
from uuid import uuid1
from soarca_fin_python_library.models.agent_structure import AgentStructure


class TestAgentStructureMessage(unittest.TestCase):

    def test_agent_structure_message_generator(self):
        name = "somestringhere"
        agentStructure = AgentStructure(name=name)

        self.assertEqual(agentStructure.type, "soarca-fin",
                         "Type should be an soarca-fin")
        self.assertEqual(agentStructure.name, name)

    def test_json_to_agent_structure(self):

        name = "test"
        agent_id = str(uuid1())
        json_obj = {
            "type": "soarca-fin",
            "name": f"soarca-fin--{name}-{agent_id}"
        }

        agent = AgentStructure(**json_obj)

        self.assertEqual(agent.type, "soarca-fin",
                         "Type should be an soarca-fin")
        self.assertEqual(agent.name, f"soarca-fin--{name}-{agent_id}",
                         "Names should match")

    def test_agent_structure_to_json(self):
        name = "soarca-fin--test-6f00849a-f0d6-11ee-9487-d6ff9f4e6dd2"
        agentStructure = AgentStructure(name=name)

        json_str = agentStructure.model_dump_json()

        json_obj = {
            "type": "soarca-fin",
            "name": "soarca-fin--test-6f00849a-f0d6-11ee-9487-d6ff9f4e6dd2",
        }

        self.assertEqual(json.loads(json_str), json_obj,
                         "Json objects should match")
