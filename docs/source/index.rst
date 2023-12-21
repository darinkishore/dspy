===========

.. image:: docs/images/DSPy8.png
   :align: center
   :width: 460px

DSPy: *Programming*—not prompting—Foundation Models
----------------------------------------------------

(links to paper and iamges from readme)

**DSPy** is the framework for solving advanced tasks with language models (LMs) and retrieval models (RMs). **DSPy** unifies techniques for **prompting** and **fine-tuning** LMs — and approaches for **reasoning**, **self-improvement**, and **augmentation with retrieval and tools**. All of these are expressed through modules that compose and learn.
=======
.. _index:

.. image:: docs/images/DSPy8.png
   :align: center
   :width: 460px



**DSPy** is the framework for solving advanced tasks with language models (LMs) and retrieval models (RMs). **DSPy** unifies techniques for **prompting** and **fine-tuning** LMs — and approaches for **reasoning**, **self-improvement**, and **augmentation with retrieval and tools**. All of these are expressed through modules that compose and learn.
Language Model Clients
----------------------

Language Model Clients are interfaces for interacting with various language models. They provide a unified API for different language models, allowing you to switch between different models with minimal code changes.

For more details, see :doc:`language_models_client`.

Retrieval Model Clients
-----------------------

Retrieval Model Clients are interfaces for interacting with various retrieval models. They provide a unified API for different retrieval models, allowing you to switch between different models with minimal code changes.

For more details, see :doc:`retrieval_models_client`.

Using Local Models
------------------

DSPy supports various methods for loading local models. This includes built-in wrappers, server integration, and external package integration.

For more details, see :doc:`using_local_models`.

Modules
-------

Modules in DSPy are composable and declarative components that encapsulate specific functionality. They can be combined to create complex programs.

For more details, see :doc:`modules`.

Teleprompters
-------------

Teleprompters in DSPy are powerful optimizers that can learn to bootstrap and select effective prompts for the modules of any program.

For more details, see :doc:`teleprompters`.

In its latest version, **DSPy** introduces new capabilities and changes that further enhance its functionality and usability. This includes the introduction of the `Box` class for handling predictions, the ability to use local models within DSPy, and improvements to the documentation. These updates are aimed at providing clear, comprehensive, and up-to-date information for all users of the project.
==================

.. image:: docs/images/DSPy8.png
   :align: center
   :width: 460px

DSPy: *Programming*—not prompting—Foundation Models
----------------------------------------------------

(links to paper and iamges from readme)

**DSPy** is the framework for solving advanced tasks with language models (LMs) and retrieval models (RMs). **DSPy** unifies techniques for **prompting** and **fine-tuning** LMs — and approaches for **reasoning**, **self-improvement**, and **augmentation with retrieval and tools**. All of these are expressed through modules that compose and learn.
To make this possible:

- **DSPy** provides **composable and declarative modules** for instruct
New Capabilities and Changes
----------------------------

1. **Introduction of the `Box` Class**: The `Box` class has been introduced to handle predictions. It allows for the storage of a value and its "alternatives", and potentially tracks the "source" of the value. This class is designed to seamlessly integrate with the existing DSPy framework and provides a more efficient and intuitive way to handle predictions.

2. **Support for Local Models**: DSPy now supports the use of local models within the framework. This includes built-in wrappers, server integration, and external package integration for model loading. This feature allows users to leverage the power of local models in their DSPy programs, providing greater flexibility and control over their tasks.

3. **Improved Documentation**: The documentation has been significantly updated to reflect the current state of the project. This includes comprehensive information on the new capabilities and changes, as well as detailed instructions on how to use DSPy. The goal is to provide clear, comprehensive, and up-to-date documentation for all users of the project.

For more detailed information on these new capabilities and changes, please refer to the respective sections in this documentation.