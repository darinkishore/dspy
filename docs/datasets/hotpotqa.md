# HotPotQA

The `hotpotqa.py` file contains the `HotPotQA` class which is a subclass of the `Dataset` class. The `HotPotQA` class is used for handling the HotPotQA dataset in the DSPy framework. It provides a flexible and efficient way to load, shuffle, and split the dataset, which is crucial for training and evaluating models.

## HotPotQA Class

The `HotPotQA` class is initialized with several parameters including `only_hard_examples`, `keep_details`, `unofficial_dev`, and others. It also inherits from the `Dataset` class and overrides some of its methods.

### Initialization

The `HotPotQA` class is initialized with several parameters. The `only_hard_examples` parameter is a boolean that indicates whether to only use hard examples. The `keep_details` parameter specifies which details to keep. The `unofficial_dev` parameter is a boolean that indicates whether to use an unofficial dev set.

```python
hotpotqa = HotPotQA(only_hard_examples=True, keep_details='dev_titles', unofficial_dev=True)
```

### Accessing Datasets

The `train`, `dev`, and `test` properties return the corresponding datasets.

```python
train_data = hotpotqa.train
dev_data = hotpotqa.dev
test_data = hotpotqa.test
