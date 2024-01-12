# Getting Started with DSPy

Welcome to DSPy, a Python-based framework for advanced tasks with language and retrieval models. This guide will help you get started with installing and using DSPy.

## Installation

To install DSPy, you need to run the following command:

```bash
pip install dspy-ai
```

For optional integrations, you can install them as follows:

```bash
pip install dspy-ai[pinecone]  # or [qdrant] or [chromadb] or [marqo]
```

## Usage Guide

DSPy supports various methods for model loading. Here's an example of how to load a model:

```python
llama = dspy.HFModel(model = 'meta-llama/Llama-2-7b-hf')
```

For more details, please refer to the [full usage guide](../api_reference/language_models/using_local_models.md).

## Examples

Here's an example of how to use DSPy for a simple task:

```python
# Initialize the model
llama = dspy.HFModel(model = 'meta-llama/Llama-2-7b-hf')

# Use the model for a task
result = llama.perform_task("example task")
```

## Additional Resources

For additional help and resources, check out the following:

- [DSPy Community](https://discord.gg/dspy)
- [Associated Projects](https://github.com/stanfordnlp/dspy#associated-projects)
