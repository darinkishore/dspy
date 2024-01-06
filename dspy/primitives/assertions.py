import inspect
from typing import Any, Callable
import dsp
import dspy
import logging
import uuid

#################### Assertion Helpers ####################


def setup_logger():
    """
    Set up a logger for the module.

    The logger logs messages with the level DEBUG to a file named "assertion.log".

    Returns:
        Logger: The set up logger.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler("assertion.log")
    fileHandler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fileHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)

    return logger


logger = setup_logger()


def _build_error_msg(feedback_msgs):
    """Build an error message from a list of feedback messages."""
    return "\n".join([msg for msg in feedback_msgs])


#################### Assertion Exceptions ####################


class DSPyAssertionError(AssertionError):
    """An exception raised specifically by DSPy when an assertion fails.

    This exception is raised when a condition checked by an `Assert` object is determined to be false and
    bypassing assertions has not been enabled in the DSPy settings.

    Attributes:
        id (str): The unique identifier of the failed assertion.
        msg (str): A message that describes the reason for the assertion failure.
        state (Any): The state of the system at the time of the assertion failure.

    """

    def __init__(self, id: str, msg: str, state: Any = None) -> None:
        """
        Create a new instance of the DSPyAssertionError exception.

        Args:
            id (str): The ID of the failed assertion.
            msg (str): The error message describing the assertion failure.
            state (Any, optional): The state of the system when the assertion failed. Defaults to None.
        """
        super().__init__(msg)
        self.id = id
        self.msg = msg
        self.state = state


class DSPySuggestionError(AssertionError):
    """An exception raised specifically by DSPy when a suggestion outcome is rejected.

    This exception is thrown when a condition checked by a `Suggest` object does not meet the desired criteria and
    the suggestion is not being bypassed in the DSPy settings.

    Attributes:
        id (str): The unique identifier of the failed suggestion.
        msg (str): A message that describes the reason for the suggestion rejection.
        target_module (Any): The module associated with the suggestion.
        state (Any): The state of the system at the time of the suggestion evaluation.

    """

    def __init__(
        self, id: str, msg: str, target_module: Any = None, state: Any = None
    ) -> None:
        """
        Create a new instance of the DSPySuggestionError exception.

        Args:
            id (str): The ID of the rejected suggestion.
            msg (str): The error message describing the cause for the suggestion rejection.
            target_module (Any, optional): The module associated with the suggestion. Defaults to None.
            state (Any, optional): The state of the system at the suggestion evaluation time. Defaults to None.
        """
        super().__init__(msg)
        self.id = id
        self.msg = msg
        self.target_module = target_module
        self.state = state


#################### Assertion Primitives ####################


class Constraint:
    """Represents a constraint that can be asserted or suggested within the DSPy framework.

    A Constraint is a condition that is intended to be checked during the execution of DSPy workflows. It can
    be used to assert conditions (with `Assert`) or make suggestions (with `Suggest`) of how a workflow or
    module should behave.

    Attributes:
        id (str): A unique identifier for the constraint.
        result (bool): The result of evaluating the constraint condition (True or False).
        msg (str, optional): An optional message providing details about the condition being checked. Defaults to an empty string.
        target_module (Any, optional): An optional reference to the module associated with the constraint. Defaults to None.

    """

    def __init__(self, result: bool, msg: str = "", target_module=None):
        """
        Initializes a new Constraint object.

        Args:
            result (bool): The outcome of the constraint check (True if the condition is met, False otherwise).
            msg (str, optional): A descriptive message about the constraint condition. Defaults to an empty string.
            target_module (Any, optional): The module that this constraint is associated with, if applicable. Defaults to None.

        """
        self.id = str(uuid.uuid4())
        self.result = result
        self.msg = msg
        self.target_module = target_module

        self.__call__()


class Assert(Constraint):
    """Implements an assert mechanism within the DSPy framework.

    An `Assert` is a type of `Constraint` used to enforce certain conditions that must be met during the DSPy workflows.
    If the condition is not met and assertions are not being bypassed, this will raise an `DSPyAssertionError`.

    """

    def __call__(self) -> bool:
        """
        Evaluates the assertion and determines if the condition is met.

        If the result of the constraint is True, it means the assertion condition is met. If the result is False, depends on the DSPy settings,
        it may either log an error and return True (if assertions are being bypassed) or raise a `DSPyAssertionError` (if assertions are not bypassed).

        Raises:
            ValueError: If the result of the constraint is not a boolean value.
            DSPyAssertionError: If the result is False and assertions are supposed to be enforced according to the settings.

        Returns:
            bool: True if the assertion condition is met, False if it is not met but assertions are being bypassed.
        """
        if isinstance(self.result, bool):
            if self.result:
                return True
            elif dspy.settings.bypass_assert:
                logger.error(f"AssertionError: {self.msg}")
                return True
            else:
                logger.error(f"AssertionError: {self.msg}")
                raise DSPyAssertionError(
                    id=self.id, msg=self.msg, state=dsp.settings.trace
                )
        else:
            raise ValueError("Assertion function should always return [bool]")


class Suggest(Constraint):
    """Implements a suggestion mechanism within the DSPy framework.

    A `Suggest` is a type of `Constraint` used to propose preferable conditions which are not strictly mandatory within the DSPy workflows.
    If the condition is not met, depending on DSPy settings, it may either log the failure and return True (if suggestions are being bypassed), or
    raise a `DSPySuggestionError` if suggestions are enforced and not followed.

    """

    def __call__(self) -> Any:
        """
        Evaluates the suggestion and determines if the preferable condition is met.

        If the result of the constraint is True, it means the suggestion condition is met. If it is False, depends on the DSPy settings,
        it may either log an error and return True (if suggestions are being bypassed) or raise a `DSPySuggestionError` (if suggestions are intended to be enforced).

        Raises:
            ValueError: If the result of the constraint is not a boolean value.
            DSPySuggestionError: If the result is False and suggestions are not meant to be bypassed.

        Returns:
            Any: True if the suggestion condition is met, False if it is not met but suggestions are being bypassed.
        """
            raise ValueError("Suggestion function should always return [bool]")


#################### Assertion Handlers ####################


def noop_handler(func):
    """Handler to bypass assertions and suggestions.

    Now both assertions and suggestions will become noops.
    """

    def wrapper(*args, **kwargs):
        with dspy.settings.context(bypass_assert=True, bypass_suggest=True):
            return func(*args, **kwargs)

    return wrapper


def bypass_suggest_handler(func):
    """Handler to bypass suggest only.

    If a suggestion fails, it will be logged but not raised.
    And If an assertion fails, it will be raised.
    """

    def wrapper(*args, **kwargs):
        with dspy.settings.context(bypass_suggest=True, bypass_assert=False):
            return func(*args, **kwargs)

    return wrapper


def bypass_assert_handler(func):
    """Handler to bypass assertion only.

    If a assertion fails, it will be logged but not raised.
    And If an assertion fails, it will be raised.
    """

    def wrapper(*args, **kwargs):
        with dspy.settings.context(bypass_assert=True):
            return func(*args, **kwargs)

    return wrapper


def assert_no_except_handler(func):
    """Handler to ignore assertion failure and return None."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DSPyAssertionError as e:
            return None

    return wrapper


def suggest_backtrack_handler(func, bypass_suggest=True, max_backtracks=2):
    """Handler for backtracking suggestion.

    Re-run the latest predictor up to `max_backtracks` times,
    with updated signature if a suggestion fails. updated signature adds a new
    input field to the signature, which is the feedback.
    """

    def wrapper(*args, **kwargs):
        error_msg, result = None, None
        dspy.settings.backtrack_to = None

        # Predictor -> List[feedback_msg]
        dspy.settings.predictor_feedbacks = {}

        for i in range(max_backtracks + 1):
            if i > 0 and dspy.settings.backtrack_to is not None:
                # generate values for new fields
                feedback_msg = _build_error_msg(
                    dspy.settings.predictor_feedbacks[dspy.settings.backtrack_to]
                )

                dspy.settings.backtrack_to_args = {
                    "feedback": feedback_msg,
                    "past_outputs": past_outputs,
                }

            # if last backtrack: ignore suggestion errors
            if i == max_backtracks:
                result = bypass_suggest_handler(func)(*args, **kwargs) if bypass_suggest else None
                break

            else:
                try:
                    result = func(*args, **kwargs)
                    break
                except DSPySuggestionError as e:
                    suggest_id, error_msg, suggest_target_module, error_state = (
                        e.id,
                        e.msg,
                        e.target_module,
                        e.state[-1],
                    )

                    if dsp.settings.trace:
                        if suggest_target_module:
                            for i in range(len(dsp.settings.trace) - 1, -1, -1):
                                trace_element = dsp.settings.trace[i]
                                mod = trace_element[0]
                                if mod.signature == suggest_target_module:
                                    dspy.settings.backtrack_to = mod
                                    break
                        else:
                            dspy.settings.backtrack_to = dsp.settings.trace[-1][0]

                        if dspy.settings.backtrack_to is None:
                            logger.error("Specified module not found in trace")

                        # save unique feedback message for predictor
                        if (
                            error_msg
                            not in dspy.settings.predictor_feedbacks.setdefault(
                                dspy.settings.backtrack_to, []
                            )
                        ):
                            dspy.settings.predictor_feedbacks[
                                dspy.settings.backtrack_to
                            ].append(error_msg)

                        output_fields = vars(error_state[0].signature.signature)
                        past_outputs = {}
                        for field_name, field_obj in output_fields.items():
                            if isinstance(field_obj, dspy.OutputField):
                                past_outputs[field_name] = getattr(
                                    error_state[2], field_name, None
                                )

                        # save latest failure trace for predictor per suggestion
                        error_ip = error_state[1]
                        error_op = error_state[2].__dict__["_store"]
                        error_op.pop("_assert_feedback", None)
                        error_op.pop("_assert_traces", None)

                    else:
                        logger.error(
                            f"UNREACHABLE: No trace available, this should not happen. Is this run time?"
                        )

        return result

    return wrapper


def handle_assert_forward(assertion_handler, **handler_args):
    def forward(self, *args, **kwargs):
        args_to_vals = inspect.getcallargs(self._forward, *args, **kwargs)

        # if user has specified a bypass_assert flag, set it
        if "bypass_assert" in args_to_vals:
            dspy.settings.configure(bypass_assert=args_to_vals["bypass_assert"])

        wrapped_forward = assertion_handler(self._forward, **handler_args)
        return wrapped_forward(*args, **kwargs)

    return forward


default_assertion_handler = suggest_backtrack_handler


def assert_transform_module(
    module, assertion_handler=default_assertion_handler, **handler_args
):
    """
    Transform a module to handle assertions.
    """
    if not getattr(module, "forward", False):
        raise ValueError(
            "Module must have a forward method to have assertions handled."
        )
    if getattr(module, "_forward", False):
        logger.info(
            f"Module {module.__class__.__name__} already has a _forward method. Skipping..."
        )
        pass  # TODO warning: might be overwriting a previous _forward method

    module._forward = module.forward
    module.forward = handle_assert_forward(assertion_handler, **handler_args).__get__(
        module
    )

    setattr(module, "_assert_transformed", True)

    return module
