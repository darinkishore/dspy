from random import sample

from dspy.teleprompt.signature_opt import Signature


class SignatureSampler:
    def sample(self, signatures, k):
        return sample(signatures, k)
