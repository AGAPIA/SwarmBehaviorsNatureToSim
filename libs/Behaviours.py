
import abc
import carla
import numpy as np

from typing import List
from libs.Walker import Walker


from libs.Preprocessors import MergeSocialLSTMInput, SocialLSTMInput, SGANInput
from libs.Inference import runSGANInference, runSocialLSTMInference


class BaseBehaviour():
    @abc.abstractmethod
    def act(self, walkers, frame_id):
        pass


class LSTMBehavior(BaseBehaviour):

    def __init__(self) -> None:
        self.last_run = 0
        self.started = False
        super().__init__()


    def act(self, walkers : List[Walker], frame_id):

        has_enough_trace = False

        lstm_input = None

        tick_diff = 100

        for i in range(len(walkers)):
            walker = walkers[i]
            controller = walker.controller

            actor_transform = controller.get_transform()
            actor_location = actor_transform.location
            actor_x = actor_location.x
            actor_y = actor_location.y

            walker.add_to_trace(frame_id, actor_x, actor_y)

            if(walker.get_trace_length() == 8):
                walker_lstm_input = SocialLSTMInput(walker)
                if(lstm_input is None):
                    lstm_input = walker_lstm_input
                else:
                    lstm_input = MergeSocialLSTMInput(lstm_input, walker_lstm_input)

                has_enough_trace = True


        if(has_enough_trace == True and (frame_id - self.last_run) > tick_diff):

            self.last_run = frame_id

            inference_result = runSocialLSTMInference(lstm_input)
            for i in range(len(walkers)):

                walker = walkers[i]

                walker_prediction = inference_result[0][i]
                future_positions = walker_prediction[-12:]

                actor_transform = walker.controller.get_transform()
                actor_location = actor_transform.location

                x_target = float(future_positions[11][0][1])
                y_target = float(future_positions[11][0][0])
                z_target = float(actor_location.z)

                new_target = carla.Location(x_target, y_target, z_target)

                if(i == 0):
                    print(walker.trace)
                    print('========== Agent {} ========'.format(walker.instance_id))
                    print("Current Location")
                    print(walker.actor.get_location())
                    print("Target Location")
                    print(new_target)
                    print('============================'.format(walker.instance_id))

                walkers[i].set_destination(new_target)


class SGANBehaviour(BaseBehaviour):

    def __init__(self) -> None:
        self.last_run = 0
        self.started = False
        super().__init__()

    def act(self, walkers : List[Walker], frame_id):

        has_enough_trace = False

        lstm_output = None

        tick_diff = 100

        sgan_input = []

        for i in range(len(walkers)):
            walker = walkers[i]
            controller = walker.controller

            actor_transform = controller.get_transform()
            actor_location = actor_transform.location
            actor_x = actor_location.x
            actor_y = actor_location.y

            walker.add_to_trace(frame_id, actor_x, actor_y)

            if(walker.get_trace_length() == 8):
                walker_sgan_input = SGANInput(walker)
                sgan_input += walker_sgan_input
                has_enough_trace = True


        if(has_enough_trace == True and (frame_id - self.last_run) > tick_diff):

            self.last_run = frame_id

            sgan_input = np.array(sgan_input)
            inference_result = runSGANInference(sgan_input)[0]

            for i in range(len(walkers)):

                walker = walkers[i]

                future_positions = inference_result[i]

                actor_transform = walker.controller.get_transform()
                actor_location = actor_transform.location

                x_target = float(future_positions[0])
                y_target = float(future_positions[1])
                z_target = float(actor_location.z)

                new_target = carla.Location(x_target, y_target, z_target)

                if(i == 0):
                    print('========== Agent {} ========'.format(walker.instance_id))
                    print("Current Location")
                    print(walker.actor.get_location())
                    print("Target Location")
                    print(new_target)
                    print('============================'.format(walker.instance_id))

                walkers[i].set_destination(new_target)