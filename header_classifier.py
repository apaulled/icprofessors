# Data Processing
import math
import random

import pandas as pd
import numpy as np

import tensorflow as tf
from keras import Sequential
from keras.src.legacy.preprocessing.text import Tokenizer
from keras.src.utils import pad_sequences
from sklearn.metrics import confusion_matrix
from tensorflow.python.keras.losses import BinaryCrossentropy

import json

from keras.src.layers import Embedding, LSTM, Dense


class HeaderClassifier:

    def __init__(self):
        with open('resources/data.json') as f:
            data = json.loads(f.read())

        x = data['headers'] + data['paragraphs']

        # print(data['headers'])

        y = [1 if x_i in data['headers'] else 0 for x_i in x]

        frame = [[x[i], y[i]] for i in range(len(x))]
        random.shuffle(frame)

        # print(frame)

        x = [thing[0] for thing in frame]
        y = [thing[1] for thing in frame]

        self.tokenizer = Tokenizer(num_words=1000)
        self.tokenizer.fit_on_texts(x)

        sequences = self.tokenizer.texts_to_sequences(x)
        data = pad_sequences(sequences, maxlen=50)

        split_index = math.floor(len(data) * 0.7)
        x_train, x_test = data[:split_index], data[split_index:]
        y_train, y_test = np.array(y[:split_index]), np.array(y[split_index:])

        self.model = Sequential([
            Embedding(input_dim=1000, output_dim=64),
            LSTM(32),
            Dense(units=1, activation='sigmoid')
        ])
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        self.model.fit(x_train, y_train, epochs=20)

        y_pred = np.round([p[0] for p in self.model.predict(x_test)])
        confuse = confusion_matrix(y_test, y_pred, normalize='pred')
        print(confuse)

    def is_header(self, text):
        x = [text]
        self.tokenizer.fit_on_texts(x)
        sequences = self.tokenizer.texts_to_sequences(x)
        data = pad_sequences(sequences, maxlen=10)
        pred = self.model.predict(data, verbose=0)
        if round(pred[0][0]) == 1:
            return True
        else:
            return False
