from openai import InvalidRequestError
from openai.error import APIError

import dsp
import tqdm
import pandas as pd

from IPython.display import display
from dsp.utils import EM, F1, HotPotF1


def evaluateRetrieval(fn, openai_predict_fn, dev, metric=None):
    data = []

    for example in tqdm.tqdm(dev):
        question = example.question
        prediction = openai_predict_fn(question)

        d = dict(example)

        # d['prediction'] = prediction.answer
        d['correct'] =  dsp.passage_match(prediction.context, example.answer)
        data.append(d)

    df = pd.DataFrame(data)

    percentage = round(100.0 * df['correct'].sum() / len(dev), 1)
    print(f"Answered {df['correct'].sum()} / {len(dev)} ({percentage}%) correctly.")
    df['correct'] = df['correct'].apply(lambda x: '✔️' if x else '❌')

    pd.options.display.max_colwidth = None
    display(df.style.set_table_styles([{'selector': 'th', 'props': [('text-align', 'left')]}, {'selector': 'td', 'props': [('text-align', 'left')]}]))


def evaluateAnswer(fn, openai_predict_fn, dev, metric=EM):
    data = []

    for example in tqdm.tqdm(dev):
        question = example.question
        prediction = openai_predict_fn(question)

        d = dict(example)

        pred = prediction.answer

        d['prediction'] = pred
        d['correct'] = metric(pred, example.answer)
        data.append(d)

    df = pd.DataFrame(data)

    percentage = round(100.0 * df['correct'].sum() / len(dev), 1)
    print(f"Answered {df['correct'].sum()} / {len(dev)} ({percentage}%) correctly.")
    df['correct'] = df['correct'].apply(lambda x: '✔️' if x else '❌')

    pd.options.display.max_colwidth = None
    display(df.style.set_table_styles([{'selector': 'th', 'props': [('text-align', 'left')]}, {'selector': 'td', 'props': [('text-align', 'left')]}]))



def evaluate(fn, openai_predict_fn, dev, metric=EM):
    data = []

    for example in tqdm.tqdm(dev):
        question = example.question
        prediction = openai_predict_fn(question)

        d = dict(example)

        pred = prediction#.answer

        d['prediction'] = pred
        d['correct'] = metric(pred, example.answer)
        data.append(d)

    df = pd.DataFrame(data)

    percentage = round(100.0 * df['correct'].sum() / len(dev), 1)
    print(f"Answered {df['correct'].sum()} / {len(dev)} ({percentage}%) correctly.")
    df['correct'] = df['correct'].apply(lambda x: '✔️' if x else '❌')

    pd.options.display.max_colwidth = None
    display(df.style.set_table_styles([{'selector': 'th', 'props': [('text-align', 'left')]}, {'selector': 'td', 'props': [('text-align', 'left')]}]))

    return percentage

# Check OpenAI library version and import syntax functions accordingly
import openai
if openai.__version__ == '0.28':
    from .syntax_v028 import *
elif openai.__version__ == '1.0':
    from .syntax_v1 import *


