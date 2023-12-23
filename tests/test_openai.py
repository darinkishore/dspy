import unittest

import dsp.modules.gpt3 as gpt3
import dsp.primitives.compiler as compiler
import dspy.retrieve.pinecone_rm as pinecone_rm
import openai
from dspy import dspy


class TestOpenAI(unittest.TestCase):
    def test_gpt3_init(self):
        model = gpt3.GPT3("gpt-3.5-turbo-instruct")
        self.assertIsInstance(model, gpt3.GPT3)

    def test_gpt3_call(self):
        model = gpt3.GPT3("gpt-3.5-turbo-instruct")
        result = model("Hello, world!")
        self.assertIsInstance(result, list)

    def test_gpt3_request(self):
        model = gpt3.GPT3("gpt-3.5-turbo-instruct")
        result = model.request("Hello, world!")
        self.assertIsInstance(result, openai.openai_object.OpenAIObject)

    def test_gpt3_basic_request(self):
        model = gpt3.GPT3("gpt-3.5-turbo-instruct")
        result = model.basic_request("Hello, world!")
        self.assertIsInstance(result, openai.openai_object.OpenAIObject)

    def test_compiler_compile(self):
        def program(x):
            return x * 2
        examples = [1, 2, 3, 4, 5]
        compiled_program = compiler.compile(program, examples)
        self.assertEqual(compiled_program(6), 12)

    def test_pinecone_rm_init(self):
        model = pinecone_rm.PineconeRM("index_name")
        self.assertIsInstance(model, pinecone_rm.PineconeRM)

    def test_pinecone_rm_forward(self):
        model = pinecone_rm.PineconeRM("index_name")
        result = model.forward("Hello, world!")
        self.assertIsInstance(result, dspy.Prediction)

if __name__ == "__main__":
    unittest.main()
