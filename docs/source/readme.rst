.. _readme:

=====================
DSPy: Programming—not prompting—Foundation Models
=====================

.. image:: ../../images/DSPy8.png
   :align: center
   :width: 460px

**DSPy** is the framework for solving advanced tasks with language models (LMs) and retrieval models (RMs). **DSPy** unifies techniques for **prompting** and **fine-tuning** LMs — and approaches for **reasoning**, **self-improvement**, and **augmentation with retrieval and tools**. All of these are expressed through modules that compose and learn.

To make this possible:

- **DSPy** provides **composable and declarative modules** for instructing LMs in a familiar Pythonic syntax. It upgrades "prompting techniques" like chain-of-thought and self-reflection from hand-adapted *string manipulation tricks* into truly modular *generalized operations that learn to adapt to your task*.

- **DSPy** introduces an **automatic compiler that teaches LMs** how to conduct the declarative steps in your program. Specifically, the **DSPy compiler** will internally *trace* your program and then **craft high-quality prompts for large LMs (or train automatic finetunes for small LMs)** to teach them the steps of your task.

The **DSPy compiler** *bootstraps* prompts and finetunes from minimal data **without needing manual labels for the intermediate steps** in your program. Instead of brittle "prompt engineering" with hacky string manipulation, you can explore a systematic space of modular and trainable pieces.

For complex tasks, **DSPy** can routinely teach powerful models like `GPT-3.5` and local models like `T5-base` or `Llama2-13b` to be much more reliable at tasks. **DSPy** will compile the *same program* into different few-shot prompts and/or finetunes for each LM.

If you want to see **DSPy** in action, `open our intro tutorial notebook <https://colab.research.google.com/github/stanfordnlp/dspy/blob/main/intro.ipynb>`_.

Table of Contents
=================

1. `Installation <#1-installation>`_
2. `Framework Syntax <#2-syntax-youre-in-charge-of-the-workflowits-free-form-python-code>`_
3. `Compiling: Two Powerful Concepts <#3-two-powerful-concepts-signatures--teleprompters>`_
4. `Tutorials & Documentation <#4-documentation--tutorials>`_
5. `FAQ: Is DSPy right for me? <#5-faq-is-dspy-right-for-me>`_
