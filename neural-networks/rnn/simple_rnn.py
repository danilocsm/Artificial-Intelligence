import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds

dataset, info = tfds.load('imdb_reviews/subwords8k', with_info=True,
                          as_supervised=True)
train_dataset = dataset['train']
test_dataset = dataset['test']
encoder = info.features['text'].encoder

# sample_string = "My name is Danilo"
# encoded_string = encoder.encode(sample_string)
# print(encoded_string)
# original_string = encoder.decode(encoded_string)
# print(original_string)

BATCH_SIZE = 64
BUFFER_SIZE = 10000
train_dataset = train_dataset.shuffle(BUFFER_SIZE)
train_dataset = train_dataset.padded_batch(BATCH_SIZE, padded_shapes=([None,],[]))

test_dataset = test_dataset.padded_batch(BATCH_SIZE, padded_shapes=([None,],[]))

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(encoder.vocab_size, 64),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

# model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
#               optimizer=tf.keras.optimizers.Adam(1e-4),
#               metrics=['accuracy'])
# # history = model.fit(train_dataset, epochs=10,validation_data=test_dataset,validation_steps=30)
# test_loss, test_acc = model.evaluate(test_dataset)
# print("Accuracy: {}".format(test_acc))
#
# def pad_to_size(vec, size):
#     zeros = [0] * (size - len(vec))
#     vec.extend(zeros)
#     return vec
#
# def sample_predict(sample_text, pad):
#     encoded_sample = encoder.encode(sample_text)
#
#     if pad:
#         encoded_sample = pad_to_size(encoded_sample, 64)
#
#     encoded_sample = tf.cast(encoded_sample, tf.float32)
#     predictions = model.predict(tf.expand_dims(encoded_sample, 0))
#     return predictions
#
# sample_text = 'The movie was cool. The animation and the graphics were out of this world. I would recommend this movie.'
# predictions = sample_predict(sample_text, pad=True)
# print(predictions)
# new_sample_text = 'This movie really sucks. Please, dont waste your time with it. Worst movie in the world. '
# print(sample_predict(new_sample_text, pad=True))