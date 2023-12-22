
### Parsing Integer Answer

The `parse_integer_answer` function is used to parse the answer from the GSM8K dataset and convert it into an integer. It takes a string answer as an argument and returns an integer.

```python
answer = parse_integer_answer("1000")
```

### GSM8K Metric

The `gsm8k_metric` function is used to compare the gold and predicted answers. It takes the gold and predicted answers as arguments and returns a boolean value indicating whether they match.

```python
match = gsm8k_metric(gold_answer, pred_answer)
```

## Usage

The `GSM8K` class is used in the DSPy framework for handling the GSM8K dataset. It provides a flexible and efficient way to load, shuffle, and split the dataset, which is crucial for training and evaluating models.

Here is an example of how to use the `GSM8K` class:

```python
# Initialize the GSM8K class
gsm8k = GSM8K()

# Access the train, dev, and test sets
trainset = gsm8k.train
devset = gsm8k.dev
testset = gsm8k.test
