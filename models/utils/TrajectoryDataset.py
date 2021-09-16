import tensorflow as tf
import numpy as np
from os import listdir,path
from typing import Text
from tensorflow.python.framework.ops import convert_to_tensor


class TrajectoryDataset(tf.data.Dataset):



    def get_total_frames(self,):
        return self.total_frames

    def set_total_frames(self,arg):
        self.total_frames = arg



    def _generator(directoryPath):

        training_data = []
        file_names = listdir(directoryPath)
        read_mode = "r"
        num_prediction_frames = 16

        for file_name in file_names:

            train_file_path = path.join(directoryPath, file_name)

            file = open(train_file_path,read_mode)

            complete_sequence_data = []

            for idx,line in enumerate(file):
                items = line.split()
                items = map(lambda x : float(x),items)
                (frame_id,agent_id,x_coord,y_coord) = items
                items = np.array([frame_id,agent_id,x_coord,y_coord])
                complete_sequence_data.append(items)


            complete_sequence_data = np.array(complete_sequence_data)
            frame_ids = np.unique(complete_sequence_data[:,0])
            frame_list = frame_ids.tolist()
            frame_num = len(frame_ids)

            frame_data = []

            for frame in frame_ids:
                frame_data.append(complete_sequence_data[frame == complete_sequence_data[:, 0], :])

            num_sequences = len(frame_ids) - num_prediction_frames + 1



            for idx in range(0 , num_sequences):


                current_sequence_data = np.concatenate(
                    frame_data[idx:idx + num_prediction_frames], axis = 0
                )


                sequence_data = []

                unique_pedestrians_in_sequence = np.unique(current_sequence_data[:,1])


                for pedestrian_id in unique_pedestrians_in_sequence:


                    current_pedestrian_subsequence = current_sequence_data[current_sequence_data[:,1] == pedestrian_id, :]


                    # Current Pedestrian Sequence is of dimension  nr_appearing_frame x 4 (frame_id,agent_id,xcoord,ycoord): 


                    first_frame_appearence = frame_list.index(current_pedestrian_subsequence[0,0]) - idx
                    last_frame_appearence = frame_list.index(current_pedestrian_subsequence[-1,0]) - idx + 1
                    
                    num_frames_pedestrian_present = last_frame_appearence - first_frame_appearence
                    
                    # Agent appears in all the frames
                    if (num_frames_pedestrian_present == num_prediction_frames):
                        frame_coordinates = current_pedestrian_subsequence[:,2:]
                        sequence_data.append(frame_coordinates)
                    else:                    
                        continue

                sequence_data = np.array(sequence_data)    
                if(sequence_data.shape[0] > 0):
                    training_data.append(sequence_data)


        for item in training_data:
            yield item
       
    def __new__(cls,datasetFolderPath):


        return tf.data.Dataset.from_generator(
            cls._generator,
            output_signature = tf.TensorSpec(shape = (None,16,2), dtype = tf.float64),
            args=(datasetFolderPath,)
        )
