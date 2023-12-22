# Teleprompters

Teleprompters are powerful optimizers (included in DSPy) that can learn to bootstrap and select effective prompts for the modules of any program. (The "tele-" in the name means "at a distance", i.e., automatic prompting at a distance.)

This documentation provides an overview of the DSPy Teleprompters.

## Teleprompters

| Module | Jump To |
| --- | --- |
| LabeledFewShot | [LabeledFewShot Section](#telepromptlabeledfewshot) |
| BootstrapFewShot | [BootstrapFewShot Section](#telepromptbootstrapfewshot) |
| Ensemble | [Ensemble Section](#telepromptensemble) |
| BootstrapFewShotWithRandomSearch | [BootstrapFewShotWithRandomSearch Section](#telepromptbootstrapfewshotwithrandomsearch) |
| BootstrapFinetune | [BootstrapFinetune Section](#telepromptbootstrapfinetune) |

## teleprompt.LabeledFewShot

### Constructor

The constructor initializes the `LabeledFewShot` class and sets up its attributes, particularly defining `k` number of samples to be used by the predictor.

```python
class LabeledFewShot(Teleprompter):
    def __init__(self, k=16):
        self.k = k
```

**Parameters:**
- `k` (_int_): Number of samples to be used for each predictor. Defaults to 16.

### Method

#### `compile(self, student, *, trainset)`

This method compiles the `LabeledFewShot` instance by configuring the `student` predictor. It assigns subsets of the `trainset` in each student's predictor's `demos` attribute. If the `trainset` is empty, the method returns the original `student`.

**Parameters:**
- `student` (_Teleprompter_): Student predictor to be compiled.
- `trainset` (_list_): Training dataset for compiling with student predictor.

**Returns:**
- The compiled `student` predictor with assigned training samples for each predictor or the original `student` if the `trainset` is empty.

### Example

```python
import dspy

#Assume defined trainset
class RAG(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()

        #declare retrieval and predictor modules
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)
    
    #flow for answering questions using predictor and retrieval modules
    def forward(self, question):
        context = self.retrieve(question).passages
        prediction = self.generate_answer(context=context, question=question)
        return dspy.Prediction(context=context, answer=prediction.answer)

#Define teleprompter
teleprompter = LabeledFewShot()

# Compile!
compiled_rag = teleprompter.compile(student=RAG(), trainset=trainset)
```

## teleprompt.BootstrapFewShot

### Constructor

The constructor initializes the `BootstrapFewShot` class and sets up parameters for bootstrapping.

```python
class BootstrapFewShot(Teleprompter):
    def __init__(self, metric=None, teacher_settings={}, max_bootstrapped_demos=4, max_labeled_demos=16, max_rounds=1):
        self.metric = metric
        self.teacher_settings = teacher_settings

        self.max_bootstrapped_demos = max_bootstrapped_demos
        self.max_labeled_demos = max_labeled_demos
        self.max_rounds = max_rounds
```

**Parameters:**
- `metric` (_callable_, _optional_): Metric function to evaluate examples during bootstrapping. Defaults to `None`.
- `teacher_settings` (_dict_, _optional_): Settings for teacher predictor. Defaults to empty dictionary.
- `max_bootstrapped_demos` (_int_, _optional_): Maximum number of bootstrapped demonstrations per predictor. Defaults to 4.
- `max_labeled_demos` (_int_, _optional_): Maximum number of labeled demonstrations per predictor. Defaults to 16.
- `max_rounds` (_int_, _optional_): Maximum number of bootstrapping rounds. Defaults to 1.

### Method

#### `compile(self, student, *, teacher=None, trainset, valset=None)`

This method compiles the BootstrapFewShot instance by performing bootstrapping to refine the student predictor.

This process includes preparing the student and teacher predictors, which involves creating predictor copies, verifying the student predictor is uncompiled, and compiling the teacher predictor with labeled demonstrations via LabeledFewShot if the teacher predictor hasn't been compiled.

The next stage involves preparing predictor mappings by validating that both the student and teacher predictors have the same program structure and the same signatures but are different objects.

The final stage is performing the bootstrapping iterations.

**Parameters:**
- `student` (_Teleprompter_): Student predictor to be compiled.
- `teacher` (_Teleprompter_, _optional_): Teacher predictor used for bootstrapping. Defaults to `None`.
- `trainset` (_list_): Training dataset used in bootstrapping.
- `valset` (_list_, _optional_): Validation dataset used in compilation. Defaults to `None`.

**Returns:**
- The compiled `student` predictor after bootstrapping with refined demonstrations.

### Example

```python
#Assume defined trainset
#Assume defined RAG class
...

#Define teleprompter and include teacher
teacher = dspy.OpenAI(model='gpt-3.5-turbo', api_key = openai.api_key, api_provider = "openai", model_type = "chat")
teleprompter = BootstrapFewShot(teacher_settings=dict({'lm': teacher}))

# Compile!
compiled_rag = teleprompter.compile(student=RAG(), trainset=trainset)
```

## teleprompt.Ensemble

### Constructor

### `__init__(self, *, reduce_fn=None, size=None, deterministic=False)`

The `Ensemble` constructor initializes an `Ensemble` teleprompter instance. It is designed to create ensembled versions of multiple programs. This means the final program uses multiple component programs' outputs to form a singular output, often leading to robust predictions.

**Parameters:**
- `reduce_fn` (_callable_, _optional_): Function that reduces outputs from different programs. A common reduce function is `dspy.majority`. Defaults to `None`.
- `size` (_int_, _optional_): The subset size of programs to use when not using all for the ensemble. Defaults to `None`, which means all programs are used.
- `deterministic` (_bool_, _optional_): Currently not implemented; if set to `True`, raises a `NotImplementedError`. It is intended for deterministic sampling of programs for the ensemble. Defaults to `False`.

```python
class Ensemble(Teleprompter):
    def __init__(self, *, reduce_fn=None, size=None, deterministic=False):
```

**Parameters:**
- `reduce_fn` (_callable_, _optional_): Function used to reduce multiple outputs from different programs into a single output. A common choice is `dspy.majority`. Defaults to `None`.
- `size` (_int_, _optional_): Number of programs to randomly select for ensembling. If not specified, all programs will be used. Defaults to `None`.
- `deterministic` (_bool_, _optional_): Specifies whether ensemble should operate deterministically. Currently, setting this to `True` will raise an error as this feature is pending implementation. Defaults to `False`.

### Method

#### `compile(self, programs)`

#### `compile(self, programs)`

Compile an ensemble of programs into a single `EnsembledProgram` which, when executed, can sample a subset of the programs or use all of them to produce outputs. These outputs are then combined using a specified `reduce_fn`.

**Parameters:**
- `programs` (_list_): List of `dspy.Module` instances to be ensembled.

**Returns:**
- An instance of `EnsembledProgram`, which can be used just like any other `dspy.Module`. The ensembled program runs the forward method on the individual programs selected, collects their outputs, and uses the `reduce_fn` to produce a final output. If `reduce_fn` is None, it returns the list of outputs directly.

**Parameters:**
- `programs` (_list_): List of programs to be ensembled.

**Returns:**
- `EnsembledProgram` (_Module_): An ensembled version of the input programs.

### Example

```python
import dspy
from dspy.teleprompt import Ensemble

# Assume a list of programs
programs = [program1, program2, program3, ...]

# Define Ensemble teleprompter
teleprompter = Ensemble(reduce_fn=dspy.majority, size=2)

# Compile to get the EnsembledProgram
ensembled_program = teleprompter.compile(programs)
```

## teleprompt.BootstrapFewShotWithRandomSearch

### Constructor

The constructor initializes the `BootstrapFewShotWithRandomSearch` class and sets up its attributes. It inherits from the `BootstrapFewShot` class and introduces additional attributes for the random search process.

```python
class BootstrapFewShotWithRandomSearch(BootstrapFewShot):
    def __init__(self, metric, teacher_settings={}, max_bootstrapped_demos=4, max_labeled_demos=16, max_rounds=1, num_candidate_programs=16, num_threads=6):
        self.metric = metric
        self.teacher_settings = teacher_settings
        self.max_rounds = max_rounds

        self.num_threads = num_threads

        self.min_num_samples = 1
        self.max_num_samples = max_bootstrapped_demos
        self.num_candidate_sets = num_candidate_programs
        self.max_num_traces = 1 + int(max_bootstrapped_demos / 2.0 * self.num_candidate_sets)

        self.max_bootstrapped_demos = self.max_num_traces
        self.max_labeled_demos = max_labeled_demos

        print("Going to sample between", self.min_num_samples, "and", self.max_num_samples, "traces per predictor.")
        print("Going to sample", self.max_num_traces, "traces in total.")
        print("Will attempt to train", self.num_candidate_sets, "candidate sets.")
```

**Parameters:**
- `metric` (_callable_, _optional_): Metric function to evaluate examples during bootstrapping. Defaults to `None`.
- `teacher_settings` (_dict_, _optional_): Settings for teacher predictor. Defaults to empty dictionary.
- `max_bootstrapped_demos` (_int_, _optional_): Maximum number of bootstrapped demonstrations per predictor. Defaults to 4.
- `max_labeled_demos` (_int_, _optional_): Maximum number of labeled demonstrations per predictor. Defaults to 16.
- `max_rounds` (_int_, _optional_): Maximum number of bootstrapping rounds. Defaults to 1.
- `num_candidate_programs` (_int_): Number of candidate programs to generate during random search.
- `num_threads` (_int_): Number of threads used for evaluation during random search.

### Method

Refer to [teleprompt.BootstrapFewShot](#telepromptbootstrapfewshot) documentation.

## Example

```python
#Assume defined trainset
#Assume defined RAG class
...

#Define teleprompter and include teacher
teacher = dspy.OpenAI(model='gpt-3.5-turbo', api_key = openai.api_key, api_provider = "openai", model_type = "chat")
teleprompter = BootstrapFewShotWithRandomSearch(teacher_settings=dict({'lm': teacher}))

# Compile!
compiled_rag = teleprompter.compile(student=RAG(), trainset=trainset)
```

## teleprompt.BootstrapFinetune

### Constructor

### `__init__(self, metric=None, teacher_settings={}, multitask=True)`

### `__init__(self, metric=None, teacher_settings={}, multitask=True)`

The `BootstrapFinetune` constructor initializes an instance of `BootstrapFinetune`. It adapts the `BootstrapFewShot` teleprompter concept specifically for a fine-tuning compilation process.

```python
class BootstrapFinetune(Teleprompter):
    def __init__(self, metric=None, teacher_settings={}, multitask=True):
```

**Parameters:**
- `metric` (_callable_, _optional_): A function used to compute the match between a model's predictions and the gold answers. It informs the bootstrapping process during fine-tuning. Defaults to `None`.
- `teacher_settings` (_dict_, _optional_): Configuration for the teacher model used in fine-tuning. Defaults to an empty dictionary.
- `multitask` (_bool_, _optional_): When `True`, fine-tuning treats tasks as related and attempts to learn across tasks. Defaults to `True`.

```python
class BootstrapFinetune(Teleprompter):
    def __init__(self, metric=None, teacher_settings={}, multitask=True):
```

**Parameters:**
- `metric` (_callable_, _optional_): Metric function to evaluate examples during bootstrapping. Defaults to `None`.
- `teacher_settings` (_dict_, _optional_): Settings for teacher predictor. Defaults to empty dictionary.
- `multitask` (_bool_, _optional_): Enable multitask fine-tuning. Defaults to `True`.

#### `compile(self, student, *, teacher=None, trainset, valset=None, target='t5-large', bsize=12, accumsteps=1, lr=5e-5, epochs=1, bf16=False, int8=False, peft=False, path_prefix=None)`

This method is responsible for compiling a `BootstrapFinetune` instance. It heavily involves preparing the finetuning dataset, performing the finetune, and putting together the compiled package with new fine-tuned language models.

**Parameters:**
- `student` (_dspy.Module_): The student model to be fine-tuned.
- `teacher` (_dspy.Module_ or _list_ of _dspy.Module_, _optional_): The teacher model(s) used to guide fine-tuning. Defaults to `None`.
- `trainset` (_iterable_): A collection of examples used for training.
- `valset` (_iterable_, _optional_): A collection of examples used for validation. Defaults to `None`.
- `target` (_str_, _optional_): The identifier for the Hugging Face model to be fine-tuned. Defaults to `'t5-large'`.
- `bsize` (_int_, _optional_): The batch size used during fine-tuning. Defaults to `12`.
- `accumsteps` (_int_, _optional_): The number of gradient accumulation steps. Defaults to `1`.
- `lr` (_float_, _optional_): The learning rate. Defaults to `5e-5`.
- `epochs` (_int_, _optional_): The number of epochs to train for. Defaults to `1`.
- `bf16` (_bool_, _optional_): Whether to use Brain Floating Point 16-bit precision. Defaults to `False`.
- `int8` (_bool_, _optional_): Whether to use 8-bit integer precision. Defaults to `False`.
- `peft` (_bool_, _optional_): Whether to use Pre-trained Encoder Fine-Tuning (PEFT). Defaults to `False`.
- `path_prefix` (_str_, _optional_): Path prefix for saving training artifacts. Defaults to `None`.

**Returns:**
- A newly compiled instance of `dspy.Module` incorporating the fine-tuned language model(s).

**Example Usage:**

```python
# Assume defined `trainset`
# Assume defined `student_model` instance of `dspy.Module`

bootstrap_finetuner = BootstrapFinetune()
compiled_model = bootstrap_finetuner.compile(student_model, trainset=trainset)
```

**Parameters:**
- `student` (_Predict_): Student predictor to be fine-tuned.
- `teacher` (_Predict_, _optional_): Teacher predictor to help with fine-tuning. Defaults to `None`.
- `trainset` (_list_): Training dataset for fine-tuning.
- `valset` (_list_, _optional_): Validation dataset for fine-tuning. Defaults to `None`.
- `target` (_str_, _optional_): Target model for fine-tuning. Defaults to `'t5-large'`.
- `bsize` (_int_, _optional_): Batch size for training. Defaults to `12`.
- `accumsteps` (_int_, _optional_): Gradient accumulation steps. Defaults to `1`.
- `lr` (_float_, _optional_): Learning rate for fine-tuning. Defaults to `5e-5`.
- `epochs` (_int_, _optional_): Number of training epochs. Defaults to `1`.
- `bf16` (_bool_, _optional_): Enable mixed-precision training with BF16. Defaults to `False`.

**Returns:**
- `compiled2` (_Predict_): A compiled and fine-tuned `Predict` instance.

### Example

```python
#Assume defined trainset
#Assume defined RAG class
...

#Define teleprompter
teleprompter = BootstrapFinetune(teacher_settings=dict({'lm': teacher}))

# Compile!
compiled_rag = teleprompter.compile(student=RAG(), trainset=trainset, target='google/flan-t5-base')
```