import unittest
import json
from uuid import uuid1


from soarca_fin_python_library.models.external_reference import ExternalReference


class TestExternalReferenceMessage(unittest.TestCase):

    def test_external_reference_message_generator_explicit(self):
        name = "test"
        description = "test description"
        url = "https://www.testurl.com"
        source = "testsource"
        external_id = str(uuid1())
        reference_id = str(uuid1())

        externalReference = ExternalReference(
            name=name, description=description, source=source, url=url, external_id=external_id, reference_id=reference_id)

        self.assertEqual(externalReference.name, name,
                         "Names should match")
        self.assertEqual(externalReference.description, description,
                         "Descriptions should match")

        self.assertEqual(externalReference.url, url,
                         "URLs should match")
        self.assertEqual(externalReference.external_id,
                         external_id, "External ids should match")
        self.assertEqual(externalReference.reference_id,
                         reference_id, "Reference ids should match")

    def test_external_reference_message_generator_implicit(self):
        name = "test"

        externalReference = ExternalReference(name=name)

        self.assertEqual(externalReference.name, name,
                         "Names should match")
        self.assertEqual(externalReference.description, None,
                         "Descriptions should be none")

        self.assertEqual(externalReference.url, None,
                         "URLs should be none")
        self.assertEqual(externalReference.external_id,
                         None, "External ids should be none")
        self.assertEqual(externalReference.reference_id,
                         None, "Reference ids should be none")

    def test_json_to_agent_structure_explicit(self):

        name = "test"
        description = "test description"
        url = "https://www.testurl.com"
        source = "testsource"
        external_id = str(uuid1())
        reference_id = str(uuid1())
        json_obj = {
            "name": name,
            "description": description,
            "source": source,
            "url": url,
            "external_id": external_id,
            "reference_id": reference_id,
        }

        externalReference = ExternalReference(**json_obj)
        self.assertEqual(externalReference.name, name,
                         "Names should match")
        self.assertEqual(externalReference.description, description,
                         "Descriptions should match")

        self.assertEqual(externalReference.url, url,
                         "URLs should match")
        self.assertEqual(externalReference.external_id,
                         external_id, "External ids should match")
        self.assertEqual(externalReference.reference_id,
                         reference_id, "Reference ids should match")

    def test_json_to_agent_structure_implicit(self):

        name = "test"
        json_obj = {
            "name": name,
            "description": None,
            "url": None,
            "source": None,
            "external_id": None,
            "reference_id": None,
        }

        externalReference = ExternalReference(**json_obj)

        self.assertEqual(externalReference.name, name,
                         "Names should match")
        self.assertEqual(externalReference.description, None,
                         "Descriptions should be none")

        self.assertEqual(externalReference.url, None,
                         "URLs should be none")
        self.assertEqual(externalReference.external_id,
                         None, "External ids should be none")
        self.assertEqual(externalReference.reference_id,
                         None, "Reference ids should be none")

    def test_agent_structure_to_json_explicit(self):
        name = "test"
        description = "test description"
        url = "https://www.testurl.com"
        source = "testsource"
        external_id = str(uuid1())
        reference_id = str(uuid1())

        externalReference = ExternalReference(
            name=name, description=description, source=source, url=url, external_id=external_id, reference_id=reference_id)

        json_str = externalReference.model_dump_json()

        json_obj = {
            "name": name,
            "description": description,
            "url": url,
            "source": source,
            "external_id": external_id,
            "reference_id": reference_id,
        }

        self.assertEqual(json.loads(json_str), json_obj,
                         "Json objects should match")

    def test_agent_structure_to_json_implicit(self):
        name = "test"

        externalReference = ExternalReference(name=name)

        json_str = externalReference.model_dump_json()

        json_obj = {
            "name": name,
            "description": None,
            "url": None,
            "source": None,
            "external_id": None,
            "reference_id": None,
        }

        self.assertEqual(json.loads(json_str), json_obj,
                         "Json objects should match")
