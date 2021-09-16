
import time
import carla
import numpy as np

from libs.Carla import Carla
from libs.WeatherBuilder import WeatherBuilder
from libs.SettingsBuilder import SettingsBuilder
from libs.Controller import buildPipeline, simulateStep, spawnWalkers
from libs.Spawner import DespawnPedestrians
from libs.Inference import runSGANInference


carla_client = Carla('localhost', 2000)

def __main__():

    carla_settings  = SettingsBuilder.get_sync_world_confing()
    carla_client.set_world_settings(carla_settings)

    #weather_config= WeatherBuilder.get_weather_config()
    #carla_client.set_weather(weather_config)

    walkers = None
    num_agents = 75
    step = 1000

    try:

        walkers = spawnWalkers(carla_client,num_agents)
        action_pipeline = buildPipeline()

        while True:
                simulateStep(carla_client, walkers, action_pipeline, step)

    except KeyboardInterrupt:
        pass
    finally:
        carla_settings  = SettingsBuilder.get_async_world_config()
        carla_client.set_world_settings(carla_settings)
        DespawnPedestrians(carla_client,walkers)
        print('Despawned')


if __name__ == "__main__":
    __main__()

