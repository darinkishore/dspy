import random

from dspy.signatures.signature import Signature


class SignatureSampler:
    def __init__(self):
        pass

    def sample(self, signatures, k):
        if k > len(signatures):
            raise ValueError("Cannot sample more items than exist in the list.")
        return random.sample(signatures, k)
