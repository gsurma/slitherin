from keras.optimizers import RMSprop
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense


class DDQNModel:

    def __init__(self, input_shape, action_space):
        self.model = Sequential()
        self.model.add(Conv2D(16,
                              3,
                              strides=(1, 1),
                              padding="valid",
                              activation="relu",
                              input_shape=input_shape,
                              data_format="channels_first"))
        self.model.add(Conv2D(32,
                              3,
                              strides=(1, 1),
                              padding="valid",
                              activation="relu",
                              input_shape=input_shape,
                              data_format="channels_first"))
        self.model.add(Flatten())
        self.model.add(Dense(256, activation="relu"))
        self.model.add(Dense(action_space))
        self.model.compile(RMSprop(), "MSE", metrics=["accuracy"])


