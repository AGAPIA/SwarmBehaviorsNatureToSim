import numpy as np
import tensorflow as tf

class PoolingModule(tf.Module):


    def mlp(self, layer_sizes, batch_norm = True, activation = 'relu', dropout = 0.0):

        mlp_model = tf.keras.Sequential()

        layers = []
        for input_dim, output_dim in zip(layer_sizes[:-1], layer_sizes[1:]):

            linear_layer = tf.keras.layers.Dense(output_dim, activation=activation)
            mlp_model.add(linear_layer)
            if(batch_norm):
                batch_norm_layer = tf.keras.layers.BatchNormalization()
                mlp_model.add(batch_norm_layer)
            if(dropout > 0.0):
                dropout_layer = tf.keras.layers.Dropout(dropout)
                mlp_model.add(dropout_layer)
        
        return mlp_model




    def __init__(self, embedding_dim=64, hidden_state_dim=64, output_dim = 1024, name="Pooling_Module"):

        super(PoolingModule, self).__init__(name=name)


        self.embedding_dim = embedding_dim
        self.hidden_state_dim = hidden_state_dim
        self.mlp_input_dim = embedding_dim + hidden_state_dim
        self.output_dim = output_dim
        mlp_layer_sizes = [self.mlp_input_dim, 512, self.output_dim]

        self.spatial_embedding = tf.keras.layers.Dense(embedding_dim, activation=None)
        self.coordinate_embedding = self.mlp(mlp_layer_sizes,batch_norm=True, activation='relu', dropout=0)


    def __call__(self,  hidden_states, ending_positions):
        

        pooled_hidden = []

        for idx, hidden_state in enumerate(hidden_states):
            ped_rel_pos = ending_positions - ending_positions[idx]
            current_relative = ending_positions
            current_relative = self.spatial_embedding(current_relative)
            hidden_mlp_input = tf.concat([current_relative,hidden_states],axis=1)
            coord_embeds = self.coordinate_embedding(hidden_mlp_input)
            pooled_result = tf.math.reduce_max(coord_embeds,axis=0)
            pooled_hidden.append(pooled_result)

        return pooled_hidden