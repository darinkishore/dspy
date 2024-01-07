# Dataset

The `dataset.py` file contains the `Dataset` class which is a fundamental part of the DSPy framework. The `Dataset` class provides a flexible and efficient way to handle and manipulate datasets, which is crucial for training and evaluating models.

## Dataset Class

The `Dataset` class is a base class for handling datasets in the DSPy framework. It provides methods for shuffling and sampling data, resetting seeds, and preparing datasets by seed.

### Initialization

The `Dataset` class is initialized with train, dev, and test sizes and seeds. It also sets the `do_shuffle` attribute to `True` and the `name` attribute to the class name.

```python
dataset = Dataset(train_size=100, dev_size=50, test_size=50)
```

### Resetting Seeds

The `reset_seeds` method allows to reset the seeds and sizes of the train, dev, and test datasets. It also deletes the existing datasets if they exist.

```python
dataset.reset_seeds(train_seed=1, dev_seed=2, test_seed=3)
```

### Accessing Datasets

The `train`, `dev`, and `test` properties return the corresponding datasets. If a dataset does not exist, it is created by shuffling and sampling the data.

```python
train_data = dataset.train
dev_data = dataset.dev
test_data = dataset.test
```

### Shuffling and Sampling Data

The `_shuffle_and_sample` method shuffles and samples the data for a given split. It also assigns a unique identifier and the split name to each example in the dataset.

### Preparing Datasets by Seed

The `prepare_by_seed` class method prepares the datasets by seed. It creates a `Dataset` object with the given arguments, divides the dev dataset into subsets according to the given train seeds, and resets the seeds and sizes of the datasets for each train seed.

```python
train_seeds = [1, 2, 3, 4, 5]
train_size = 16
dev_size = 1000
eval_seed = 2023
datasets = Dataset.prepare_by_seed(train_seeds=train_seeds, train_size=train_size, dev_size=dev_size, eval_seed=eval_seed)
