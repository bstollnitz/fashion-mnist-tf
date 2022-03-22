"""Training, evaluation, and prediction."""

import os
from typing import Tuple

from PIL import Image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import tensorflow as tf

from neural_network import NeuralNetwork

labels_map = {
    0: 'T-Shirt',
    1: 'Trouser',
    2: 'Pullover',
    3: 'Dress',
    4: 'Coat',
    5: 'Sandal',
    6: 'Shirt',
    7: 'Sneaker',
    8: 'Bag',
    9: 'Ankle Boot',
}

MODEL_DIRPATH = 'fashion-mnist-tf/local-keras/model/weights'
IMAGE_FILEPATH = 'fashion-mnist-tf/local-keras/src/predict-image.png'


def _get_data(batch_size: int) -> Tuple[tf.data.Dataset, tf.data.Dataset]:
    """Downloads Fashion MNIST data, and returns two Dataset objects
    wrapping test and training data."""
    (training_images, training_labels), (
        test_images, test_labels) = tf.keras.datasets.fashion_mnist.load_data()

    train_dataset = tf.data.Dataset.from_tensor_slices(
        (training_images, training_labels))
    test_dataset = tf.data.Dataset.from_tensor_slices(
        (test_images, test_labels))

    train_dataset = train_dataset.map(lambda image, label:
                                      (float(image) / 255.0, label))
    test_dataset = test_dataset.map(lambda image, label:
                                    (float(image) / 255.0, label))

    train_dataset = train_dataset.batch(batch_size).shuffle(500)
    test_dataset = test_dataset.batch(batch_size).shuffle(500)

    return (train_dataset, test_dataset)


def training_phase():
    """Trains the model for a number of epochs, and saves it."""
    learning_rate = 0.1
    batch_size = 64
    epochs = 5

    (train_dataset, test_dataset) = _get_data(batch_size)

    model = NeuralNetwork()

    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    optimizer = tf.keras.optimizers.SGD(learning_rate)
    metrics = ['accuracy']
    model.compile(optimizer, loss_fn, metrics)

    print('\n***Training***')
    model.fit(train_dataset, epochs=epochs)

    print('\n***Evaluating***')
    (test_loss, test_accuracy) = model.evaluate(test_dataset)
    print(f'Test loss: {test_loss:>8f}, ' +
          f'test accuracy: {test_accuracy * 100:>0.1f}%')

    model.save(MODEL_DIRPATH)


def inference_phase():
    """Makes a prediction for a local image."""
    print('\n***Predicting***')

    model = tf.keras.models.load_model(MODEL_DIRPATH)

    with Image.open(IMAGE_FILEPATH) as image:
        x = np.asarray(image).reshape((-1, 28, 28)) / 255.0

    predicted_index = np.argmax(model.predict(x))
    predicted_name = labels_map[predicted_index]

    print(f'Predicted class: {predicted_name}')


def main() -> None:
    training_phase()
    inference_phase()


if __name__ == '__main__':
    main()
