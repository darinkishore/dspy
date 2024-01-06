import dspy
import dsp

from .predict import Predict


class Retry(Predict):
    """A Predict module wrapper enabling retry logic for handling exceptions.

    The Retry class is designed to augment the behavior of an existing module with retry logic. When an error is
    encountered during the execution of the original module's forward method, this wrapper allows for
    re-attempting execution with potentially modified inputs based on past failures.

    Attributes:
        module (Predict): The original module that the Retry class wraps.
        original_signature (Signature): The signature of the original module.
        original_forward (Callable): The original forward callable.
        new_signature (Signature): The generated signature with additional fields to handle past outputs and feedback.

    Methods:
        - __init__: Initializes the Retry class.
        - _create_new_signature: Filters and extends the signature for retry purposes.
        - forward: Overridden forward method that handles retry logic.
        - __call__: Callable method that delegates to the original or overridden forward method.
    """
    def __init__(self, module):
        super().__init__(module.signature)
        self.module = module
        self.original_signature = module.signature.signature
        self.original_forward = module.forward
        self.new_signature = self._create_new_signature(self.original_signature)

    def _create_new_signature(self, original_signature):
        """Generates a new signature by augmenting the original with fields for retry logic.

        This method extends the original module's signature by adding new input fields corresponding to past outputs and feedback. It effectively creates a new 'extended' signature for the Retry module.

        Args:
            original_signature (Signature): The original signature from the Predict module.

        Returns:
            Dict[str, Any]: The 'extended' signature dictionary with added fields for past outputs and feedback.
        """
        extended_signature = {}
        input_fields = original_signature.input_fields()
        output_fields = original_signature.output_fields()
        modified_output_fields = {}

        for key, value in output_fields.items():
            modified_output_fields[f"past_{key}"] = dspy.InputField(
                prefix="Past " + value.prefix,
                desc="past output with errors",
                format=value.format,
            )

        extended_signature.update(input_fields)
        extended_signature.update(modified_output_fields)

        extended_signature["feedback"] = dspy.InputField(
            prefix="Instructions:",
            desc="Some instructions you must satisfy",
            format=str,
        )
        extended_signature.update(output_fields)

        return extended_signature

    def forward(self, *args, **kwargs):
        """Executes the module's forward method incorporating retry logic with past outputs and feedback.

        Adjusts the inputs based on past outputs to retry the computation in case of previous errors.
        It modifies the forward call to include these additional inputs for a new computation attempt.

        Args:
            *args: Positional arguments for the forward method.
            **kwargs: Keyword arguments for the forward method, including past outputs and feedback.

        Returns:
            Any: The result of the forward computation possibly using modified inputs.
        """
        for key, value in kwargs["past_outputs"].items():
            past_key = f"past_{key}"
            if past_key in self.new_signature:
                kwargs[past_key] = value
        del kwargs["past_outputs"]
        kwargs["signature"] = self.new_signature
        demos = kwargs.pop("demos", self.demos if self.demos is not None else [])
        return self.original_forward(demos=demos, **kwargs)
    
    def __call__(self, **kwargs):
        """Invokes the module's call method or the forward method with retry adjustments.

        This method determines whether to execute the module's original call method or to invoke the forward method with retry logic. If DSPy settings specify to backtrack, it uses the previously failed args; otherwise, it proceeds with a normal call or a retry.

        Args:
            **kwargs: Keyword arguments for the call, including any args from backtrack settings.

        Returns:
            Any: The result of the original call or the forward method with retry adjustments.
        """
        if dspy.settings.backtrack_to == self.module:
            for key, value in dspy.settings.backtrack_to_args.items():
                kwargs.setdefault(key, value)
            return self.forward(**kwargs)
        else:
            # seems like a hack, but it works for now
            demos = kwargs.pop("demos", self.demos if self.demos is not None else [])
            return self.module(demos=demos, **kwargs)
