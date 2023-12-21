===========



(links to paper and iamges from readme)

**DSPy** is the framework for solving advanced tasks with language models (LMs) and retrieval models (RMs). **DSPy** unifies techniques for **prompting** and **fine-tuning** LMs — and approaches for **reasoning**, **self-improvement**, and **augmentation with retrieval and tools**. All of these are expressed through modules that compose and learn.
=======
.. _index:

.. include:: readme.rst

.. toctree::

.. image:: docs/images/DSPy8.png
   :align: center
   :width: 460px

DSPy: *Programming*—not prompting—Foundation Models
----------------------------------------------------

(links to paper and iamges from readme)

**DSPy** is the framework for solving advanced tasks with language models (LMs) and retrieval models (RMs). **DSPy** unifies techniques for **prompting** and **fine-tuning** LMs — and approaches for **reasoning**, **self-improvement**, and **augmentation with retrieval and tools**. All of these are expressed through modules that compose and learn.

.. toctree::
   :maxdepth: 2
   :caption: Table of Contents

   language_models
   retrieval_models
   using_local_models
   modules
   teleprompters
==================

.. image:: docs/images/DSPy8.png
   :align: center
   :width: 460px

DSPy: *Programming*—not prompting—Foundation Models
----------------------------------------------------

(links to paper and iamges from readme)

**DSPy** is the framework for solving advanced tasks with language models (LMs) and retrieval models (RMs). **DSPy** unifies techniques for **prompting** and **fine-tuning** LMs — and approaches for **reasoning**, **self-improvement**, and **augmentation with retrieval and tools**. All of these are expressed through modules that compose and learn.
.. include:: language_models.rst
----------------------

Language Model Clients are interfaces for interacting with various language models. They provide a unified API for different language models, allowing you to switch between different models with minimal code changes.

For more details, see :doc:`language_models_client`.

Retrieval Model Clients
-----------------------

.. include:: retrieval_models.rst are interfaces for interacting with various retrieval models. They provide a unified API for different retrieval models, allowing you to switch between different models with minimal code changes.

For more details, see :doc:`retrieval_models_client`.

Using Local Models
------------------

DSPy supports various methods for loading local models. This includes built-in wrappers, server integration, and external package integration.

For more details, see :doc:`using_local_models`.

Modules
-------

Modules in DSPy are composable and declarative components that encapsulate specific functionality. They can be combined to create complex programs.

For more details, see :doc:`modules`.

.. include:: teleprompters.rst
-------------

Teleprompters in DSPy are powerful optimizers that can learn to bootstrap and select effective prompts for the modules of any program.

For more details, see :doc:`teleprompters`.

To make this possible:

- **DSPy** provides **composable and declarative modules** for instruct