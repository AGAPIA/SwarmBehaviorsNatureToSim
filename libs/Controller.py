
from typing import List
from libs.Carla import Carla
from libs.Spawner import  SpawnPedestriansAtLocations, GetSpawnPointsNearLocation
from libs.Behaviours import LSTMBehavior, SGANBehaviour
from libs.Walker import Walker

def spawnWalkers(carla_client, num_agents):
    spectator_transform = carla_client.get_spectator_transform()
    spectator_location = spectator_transform.location
    spawn_locations = GetSpawnPointsNearLocation(carla_client,spectator_location,num_agents)
    walkers = SpawnPedestriansAtLocations(carla_client,spawn_locations,num_agents)
    return walkers


def buildPipeline():


    #lstmBehaviour = LSTMBehavior()
    sganBehaviour = SGANBehaviour()

    action_pipeline = [
        sganBehaviour
    ]

    return action_pipeline


def simulateStep(carla_client : Carla, walkers : List[Walker], action_pipeline : List[any], step: int = 10):
    tick = carla_client.tick()
    if(tick % step == 0):
        print('hit at {}'.format(tick))
        for action in action_pipeline:
            action.act(walkers, tick)

