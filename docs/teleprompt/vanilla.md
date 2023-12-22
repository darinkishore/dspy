# Vanilla Teleprompter

The `vanilla.py` file in the `teleprompt` module contains the `LabeledFewShot` class, which is a type of teleprompter. This class is used to compile a student model with a given training set.

## LabeledFewShot Class

The `LabeledFewShot` class is a type of teleprompter that compiles a student model with a given training set.

### `__init__(self, k=16)`

This method initializes the `LabeledFewShot` class.

**Parameters:**

- `k` (int, optional): The number of examples to sample from the training set. Defaults to 16.

### `compile(self, student, *, trainset, sample=True)`

This method compiles the student model with the given training set.

**Parameters:**

- `student` (Model): The student model to compile.
- `trainset` (list): The training set to use for compilation.
- `sample` (bool, optional): Whether to sample examples from the training set. Defaults to True.

**Return:**

- `student` (Model): The compiled student model.

## Examples

Here is an example of how to use the `LabeledFewShot` class:

```python
from dspy.teleprompt.vanilla import LabeledFewShot

# Initialize the LabeledFewShot class
teleprompter = LabeledFewShot(k=16)

# Compile the student model
compiled_student = teleprompter.compile(student, trainset=trainset, sample=True)
