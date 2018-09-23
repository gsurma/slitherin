from keras.optimizers import RMSprop
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense


class DeepQNetModel:

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
        self.model.compile(loss="mean_squared_error",
                           optimizer=RMSprop(lr=0.00025,
                                             rho=0.95,
                                             epsilon=0.01),
                           metrics=["accuracy"])
        #self.model.compile(RMSprop(), 'MSE', metrics=["accuracy"])
        self.model.summary()
        #
        # self.model = Sequential()
        #
        # # Convolutions.
        # self.model.add(Conv2D(
        #     16,
        #     kernel_size=(3, 3),
        #     strides=(1, 1),
        #     data_format='channels_first',
        #     input_shape=(num_last_frames,) + env.observation_shape
        # ))
        # self.model.add(Activation('relu'))
        # model.add(Conv2D(
        #     32,
        #     kernel_size=(3, 3),
        #     strides=(1, 1),
        #     data_format='channels_first'
        # ))
        # model.add(Activation('relu'))
        #
        # # Dense layers.
        # model.add(Flatten())
        # model.add(Dense(256))
        # model.add(Activation('relu'))
        # model.add(Dense(env.num_actions))
        #
        # model.summary()
        # model.compile(RMSprop(), 'MSE')

