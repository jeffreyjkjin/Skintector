import argparse

import keras
import tensorflow as tf
from utils import input_preprocess

# Setting seed to ensure reproducibility
keras.utils.set_random_seed(42)


## Define test set loader
def load_test_set(image_size, batch_size):
    # Loading images from the test set
    test_ds = keras.utils.image_dataset_from_directory(
        "./api/training/sd198/test",
        image_size=image_size,
        batch_size=batch_size,
    )
    # Preprocessing the images
    test_ds = test_ds.map(input_preprocess, num_parallel_calls=tf.data.AUTOTUNE)
    # Prefetching data
    test_ds = test_ds.prefetch(buffer_size=tf.data.AUTOTUNE)

    return test_ds


## Main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", "-m", type=int, required=True, help="Model number (1-6)"
    )
    args = parser.parse_args()

    # Set hyperparameters
    image_dim = 480
    image_size = (image_dim, image_dim)
    batch_size = 16

    ## Load test set of SD-198
    test_ds = load_test_set(
        image_size=image_size,
        batch_size=batch_size,
    )

    ## Load the model
    model = keras.saving.load_model(f"./api/training/models/model_{args.model}.keras")

    ## Evaluate the model
    results = model.evaluate(test_ds, return_dict=True)
    print(results["accuracy"])
    print(results["f1-score"])
