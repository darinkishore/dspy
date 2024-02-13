import re

from dspy.modules.prompt_compression import PromptCompression
from dspy.utils import ModelTokenLimits


class Compiler:
    def __init__(self, enable_compression=False, model_name='GPT-3.5'):
        self.enable_compression = enable_compression
        self.model_name = model_name
        self.prompt_compressor = PromptCompression() if enable_compression else None
        self.model_token_limit = ModelTokenLimits.get_limit(model_name)

    def compile(self, program):
        if self._exceeds_token_limit(program) and self.enable_compression:
            program = self._compress_program(program)
        program = self._apply_principle_based_learning(program)
        return program

    def _exceeds_token_limit(self, program):
        return len(program.split()) > self.model_token_limit

    def _compress_program(self, program):
        return self.prompt_compressor.compress(program)

    def _apply_principle_based_learning(self, program):
        # Simulated logic for extracting key principles
        key_principles = re.findall(r'\b(key principles|strategies)\b', program, re.IGNORECASE)
        return ' '.join(key_principles)

class ModelTokenLimits:
    @staticmethod
    def get_limit(model_name):
        limits = {
            'GPT-3.5': 4097,
            'GPT-4': 8192,
            'Mistral': 8000
        }
        return limits.get(model_name, 4097)
