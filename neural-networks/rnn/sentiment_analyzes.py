import random
import re
import nltk
import numpy as np
import tensorflow as tf
import os


def clean_text(text):
    contractions = {
        "i'm": "i am",
        "he's": "he is",
        "she's": "she is",
        "that's": "that is",
        "what's": "what is",
        "where's": "where is",
        "didn't": "did not",
        "haven't": "have not",
        "\'ll": " will",
        "\'ve": " have",
        "\'re": " are",
        "\'d": " would",
        "won't": "will not",
        "can't": "can not",
        "it's" : "it is",
        "there's" : "there is",
        "don't" : "do not"
    }
    new_text = text.lower()
    for contracted, uncontracted in contractions.items():
        new_text = re.sub(contracted, uncontracted, new_text)
    new_text = re.sub(r"[-()#@;:<>~+=?.|,\]\[!{}]","",new_text)
    return new_text

# Getting the data (train data)
negative_reviews = []
positive_reviews = []
path = "data/aclImdb/train/"
all_text = ""
for dirpath, dir_names, fnames in os.walk(path):
    for dir_name in dir_names:
        for _, _, files in os.walk(path + dir_name):
            path_to_file = path + dir_name + '/'
            for file in files:
                with open(path_to_file + file, 'r') as f:
                    text = clean_text(f.read())
                    all_text += text
                    tokenized_text = nltk.word_tokenize(text)
                    if dir_name == 'neg':
                        negative_reviews.append(tokenized_text)
                    elif dir_name == 'pos':
                        positive_reviews.append(tokenized_text)
                       
    break

# Creating the vocabulary(Size = 8000 words)
word_counter = nltk.FreqDist(word for word in nltk.word_tokenize(all_text))
most_common_words = word_counter.most_common(8000)
vocab = [word for word, count in most_common_words]

id_val = 0
words_ids = {}
for word in vocab:
    words_ids[word] = id_val
    id_val += 1

ids_words = {}
for key, item in words_ids.items():
    ids_words[item] = key

words_ids['<PAD>'] = id_val
# print(words_ids)

def encode(words):
    return [words_ids[word] for word in words if word in vocab]

def decode(ids):
    return [id_words[word] for id in ids]

words_to_ids_negative_reviews = [encode(words) for words in negative_reviews]
words_to_ids_positive_reviews = [encode(words) for words in positive_reviews]

reviews = [(review,1) for review in words_to_ids_negative_reviews]
reviews.extend([(review,0) for review in words_to_ids_positive_reviews])
random.shuffle(reviews)

SEQUENCE_LEN = max([len(review[0]) for review in reviews])

def padding(sequence):
    return sequence + [words_ids['<PAD>']] * (SEQUENCE_LEN - len(sequence))

inputs = []
outputs = []
for review, label in reviews:
    inputs.append(review)
    outputs.append(label)

inputs = np.array([padding(_input) for _input in inputs])
outputs = np.array(outputs)
# Creating the model

model = tf.keras.Sequential()
model.add(tf.keras.layers.Embedding(len(words_ids), 64, input_length=SEQUENCE_LEN))
model.add(tf.keras.layers.GlobalAveragePooling1D())
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
    optimizer=tf.keras.optimizers.Adam(0.001),
    metrics=['accuracy'])
history = model.fit(inputs,outputs,epochs=10)