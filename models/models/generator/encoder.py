import numpy as np
import tensorflow as tf

class Encoder(tf.Module):

    def __init__(self,embedding_dim=64, encoding_dimension=1024, hidden_size=64, name="Encoder"):
        super(Encoder, self).__init__(name=name)

        self.mlp_layer = tf.keras.layers.Dense(encoding_dimension, activation='relu')
        self.encoder = tf.keras.layers.LSTM(hidden_size)

    def __call__(self, input_data):
        x = self.mlp_layer(input_data)
        x = self.encoder(x)
        return x