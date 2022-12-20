import tensorflow as tf
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.layers import LSTM, Embedding
from tensorflow.keras.models import Model

dataset = pd.read_csv('./AI/dataset_new.csv')
dataset.dropna(inplace = True)

x = dataset['tweet'].to_numpy()
y = dataset['class'].to_numpy()

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

vectorizer = TextVectorization(
    max_tokens = None, 
    standardize = 'lower_and_strip_punctuation', 
    split = 'whitespace', 
    ngrams = None, 
    output_mode = 'int', 
    output_sequence_length = None)

MAX_VOCAB = 1500
MAX_LENGTH = 15

vectorizer = TextVectorization(max_tokens = MAX_VOCAB, output_mode = 'int', output_sequence_length=MAX_LENGTH)
vectorizer.adapt(x_train)

tf.random.set_seed(42)
embedding = Embedding(embeddings_initializer = 'uniform', output_dim = 128, input_dim = MAX_VOCAB, input_length = MAX_LENGTH, name='embedding')

input = Input(shape=(1,), dtype="string")
x = vectorizer(input)
x = embedding(x)
x = LSTM(100)(x)

output = Dense(1, activation="sigmoid")(x)
model = tf.keras.Model(input, output, name="LSTM")

model.compile(
    loss='binary_crossentropy',
    optimizer='adam', 
    metrics=['accuracy']
)

history = model.fit(
    x_train, 
    y_train, 
    epochs=10, 
    validation_data = (x_test, y_test))

def predict_word(sentence):
  probability = model.predict([sentence])
  return probability[0][0]