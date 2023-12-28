import unittest

from dspy.signatures.field import InputField, OutputField
from dspy.signatures.signature import Signature


class TestSignature(unittest.TestCase):
    def setUp(self):
        self.signature = Signature(signature="input1, input2 -> output1, output2", instructions="Test instructions.")
        self.signature.prompt_skeleton = "Immutable prompt skeleton"

    def test_prompt_skeleton_creation(self):
        self.assertEqual(self.signature.prompt_skeleton, "Immutable prompt skeleton")

    def test_signature_sampling(self):
        sampled_signatures = self.signature.sample_variations(k=2)
        self.assertEqual(len(sampled_signatures), 2)
        for signature in sampled_signatures:
            self.assertIsInstance(signature, Signature)

    def test_parse_structure(self):
        self.signature.parse_structure()
        expected_fields = {
            "input1": InputField(),
            "input2": InputField(),
            "output1": OutputField(),
            "output2": OutputField()
        }
        self.assertEqual(self.signature.fields, expected_fields)

if __name__ == "__main__":
    unittest.main()
