import random

from .signature import Signature


class SignatureSampler:
    def __init__(self):
        pass

    def sample(self, signatures: list[Signature], k: int) -> list[Signature]:
        return random.sample(signatures, k)
