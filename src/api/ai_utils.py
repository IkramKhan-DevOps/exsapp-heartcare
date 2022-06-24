from tensorflow.keras.models import load_model
import numpy as np
from core import settings


def load_image_file():
    # # Save the model
    filepath = f'{settings.BASE_DIR}\\saved_model'
    NN_model = load_model(filepath, compile=True)
    return NN_model


# load an image and predict the class
def run(inp):
    print('------------------INPUT--------------------------------------------------------')
    print(inp)
    print('--------------------------------------------------------------------------------')

    input_np = np.asarray(inp)
    inp = input_np.reshape(1, -1)
    model = load_image_file()
    print('------------------MODEL TYPE-----------------------------------------------------------')
    print(type(model))
    print('------------------------------------------------------------------------------------')
    prediction = model.predict(inp)
    print('------------------OUTPUT-----------------------------------------------------------')
    print(prediction)
    print('------------------------------------------------------------------------------------')
    model.save_weights('fer.h5')
    return prediction
