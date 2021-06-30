# -*- coding: utf-8 -*-
"""Copy of covid_detection_from_symptoms.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZSmefvp5aLm9JJNaFcvFYN7EUBSZ3Hi-
"""

import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers

file_name = 'corona_symtomps_data.csv'
df = pd.read_csv(file_name)

df = df.drop(['test_date'], axis=1)

df = df.reindex(['cough', 'fever', 'sore_throat', 'shortness_of_breath', 'head_ache', 'age_60_and_above', 'gender', 'test_indication', 'corona_result'], axis=1)

df = df.rename(columns={'corona_result': 'target'})

df = df.sample(n=9800)

df.dropna(inplace=True)

df.reset_index(drop=True, inplace=True)

# df['target'].unique()

df = df[~df.target.str.contains("other")]

# df['target'].unique()

# df['age_60_and_above'].unique()
#
# df['test_indication'].unique()


df.target = pd.Categorical(df.target)
df['target'] = df.target.cat.codes

df.age_60_and_above = pd.Categorical(df.age_60_and_above)
df['age_60_and_above'] = df.age_60_and_above.cat.codes

df.gender = pd.Categorical(df.gender)
df['gender'] = df.gender.cat.codes

df.test_indication = pd.Categorical(df.test_indication)
df['test_indication'] = df.test_indication.cat.codes

df['target'].value_counts()

count_class_0, count_class_1 = df['target'].value_counts()

# Commented out IPython magic to ensure Python compatibility.
val_df = df.sample(frac=0.20, random_state=1337)
train_df = df.drop(val_df.index)

print(
    "Using %d samples for training and %d for validation"
)

def dataframe_to_dataset(df):
    df = df.copy()
    labels = df.pop("target")
    ds = tf.data.Dataset.from_tensor_slices((dict(df), labels))
    ds = ds.shuffle(buffer_size=len(df))
    return ds


train_ds = dataframe_to_dataset(train_df)
val_ds = dataframe_to_dataset(val_df)
val_ds_test = val_ds

for x, y in train_ds.take(1):
    print("Input:", x)
    print("Target:", y)

train_ds = train_ds.batch(10)
val_ds = val_ds.batch(10)

from tensorflow.keras.layers.experimental.preprocessing import Normalization
from tensorflow.keras.layers.experimental.preprocessing import CategoryEncoding
from tensorflow.keras.layers.experimental.preprocessing import StringLookup


def encode_numerical_feature(feature, name, dataset):
    # Create a Normalization layer for our feature
    normalizer = Normalization()

    # Prepare a Dataset that only yields our feature
    feature_ds = dataset.map(lambda x, y: x[name])
    feature_ds = feature_ds.map(lambda x: tf.expand_dims(x, -1))

    # Learn the statistics of the data
    normalizer.adapt(feature_ds)

    # Normalize the input feature
    encoded_feature = normalizer(feature)
    return encoded_feature


def encode_string_categorical_feature(feature, name, dataset):
    # Create a StringLookup layer which will turn strings into integer indices
    index = StringLookup()

    # Prepare a Dataset that only yields our feature
    feature_ds = dataset.map(lambda x, y: x[name])
    feature_ds = feature_ds.map(lambda x: tf.expand_dims(x, -1))

    # Learn the set of possible string values and assign them a fixed integer index
    index.adapt(feature_ds)

    # Turn the string input into integer indices
    encoded_feature = index(feature)

    # Create a CategoryEncoding for our integer indices
    encoder = CategoryEncoding(output_mode="binary")

    # Prepare a dataset of indices
    feature_ds = feature_ds.map(index)

    # Learn the space of possible indices
    encoder.adapt(feature_ds)

    # Apply one-hot encoding to our indices
    encoded_feature = encoder(encoded_feature)
    return encoded_feature


def encode_integer_categorical_feature(feature, name, dataset):
    # Create a CategoryEncoding for our integer indices
    encoder = CategoryEncoding(output_mode="binary")

    # Prepare a Dataset that only yields our feature
    feature_ds = dataset.map(lambda x, y: x[name])
    feature_ds = feature_ds.map(lambda x: tf.expand_dims(x, -1))

    # Learn the space of possible indices
    encoder.adapt(feature_ds)

    # Apply one-hot encoding to our indices
    encoded_feature = encoder(feature)
    return encoded_feature

# Categorical features encoded as integers
age_60_and_above = keras.Input(shape=(1,), name="age_60_and_above", dtype="int64")
gender = keras.Input(shape=(1,), name="gender", dtype="int64")
test_indication = keras.Input(shape=(1,), name="test_indication", dtype="int64")


# Numerical features
cough = keras.Input(shape=(1,), name="cough")
fever = keras.Input(shape=(1,), name="fever")
sore_throat = keras.Input(shape=(1,), name="sore_throat")
shortness_of_breath = keras.Input(shape=(1,), name="shortness_of_breath")
head_ache = keras.Input(shape=(1,), name="head_ache")

all_inputs = [
    cough,
    fever,
    sore_throat,
    shortness_of_breath,
    head_ache,
    age_60_and_above,
    gender,
    test_indication,
]

# Integer categorical features
age_60_and_above_encoded = encode_integer_categorical_feature(age_60_and_above, "age_60_and_above", train_ds)
gender_encoded = encode_integer_categorical_feature(gender, "gender", train_ds)
test_indication_encoded = encode_integer_categorical_feature(test_indication, "test_indication", train_ds)


# Numerical features
cough_encoded = encode_numerical_feature(cough, "cough", train_ds)
fever_encoded = encode_numerical_feature(fever, "fever", train_ds)
sore_throat_encoded = encode_numerical_feature(sore_throat, "sore_throat", train_ds)
shortness_of_breath_encoded = encode_numerical_feature(shortness_of_breath, "shortness_of_breath", train_ds)
head_ache_encoded = encode_numerical_feature(head_ache, "head_ache", train_ds)

all_features = layers.concatenate(
    [
        cough_encoded,
        fever_encoded,
        sore_throat_encoded,
        shortness_of_breath_encoded,
        head_ache_encoded,
        age_60_and_above_encoded,
       gender_encoded,
       test_indication_encoded,
    ]
    )
x = layers.Dense(8, activation="relu")(all_features)
x = layers.Dropout(0.5)(x)
output1 = layers.Dense(10, activation="relu")(x)
output2 = layers.Dense(10, activation="relu")(output1)
output = layers.Dense(1, activation="sigmoid")(output2)
model = keras.Model(all_inputs, output)
model.compile("adam", "binary_crossentropy", metrics=["accuracy"])

keras.utils.plot_model(model, show_shapes=True, rankdir="LR")

# fit the keras model on the dataset
history = model.fit(train_ds, epochs=50, validation_data=val_ds)
#history = modelh.fit(x_train, y_train, epochs=20, validation_data=(x_test, y_test), batch_size=128)

sample = {
    "cough": 1,
    "fever": 1,
    "sore_throat": 1,
    "shortness_of_breath": 1,
    "head_ache": 1,
    "age_60_and_above": 1,
    "gender": 1,
    "test_indication": 1
}

input_dict = {name: tf.convert_to_tensor([value]) for name, value in sample.items()}
predictions = model.predict(input_dict)

print(
    "This particular patient had a %.1f percent probability "
    "of having a corona disease, as evaluated by our model." % (100 * predictions[0][0],)
)

sample = {
    "cough": 0,
    "fever": 0,
    "sore_throat": 0,
    "shortness_of_breath": 0,
    "head_ache": 0,
    "age_60_and_above": 0,
    "gender": 0,
    "test_indication": 0
}

input_dict = {name: tf.convert_to_tensor([value]) for name, value in sample.items()}
predictions = model.predict(input_dict)

print(
    "This particular patient had a %.1f percent probability "
    "of having a corona disease, as evaluated by our model." % (100 * predictions[0][0],)
)

import keras.backend as kb
kb.eval(model.optimizer)
kb.eval(model.optimizer.learning_rate)

import matplotlib.pyplot as plt
# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

# evaluate the keras model
_, accuracy = model.evaluate(val_ds)
print('Accuracy: %.2f' % (accuracy*100))

predict_values_prob = model.predict(val_ds)


predict_values = [1 if (100 * x[0])> 40 else 0 for x in predict_values_prob]

dataset = val_df.values
y_class_original = list(dataset[:,8])

from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_class_original, predict_values)
print(cm)

import seaborn as sns
#sns.heatmap(cm,annot=True,annot_kws={"size": 16},fmt='1f')# font size
sns.heatmap(cm, annot=True, cmap='twilight_shifted', fmt='g')

from sklearn.metrics import classification_report
print(classification_report(y_class_original, predict_values
))