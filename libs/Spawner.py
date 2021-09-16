import glob
import os
import sys
import time
import carla
import argparse
import logging
import random
import numpy as np

from numpy.lib.function_base import select

from libs.Carla import Carla
from libs.Walker import Walker
from libs.Geom import compute_distance


def SpawnPedestrians(carla_client, num_agents):

    walkers = []

    try:

        world = carla_client.get_world()

        percentagePedestriansCrossing = 0.0

        spawn_points = []
        batch_commands = []

        walker_blueprints = carla_client.get_all_walker_blueprints()

        for i in range(num_agents):
            spawn_point = carla.Transform()
            loc = carla_client.get_random_location_from_navigation()
            if(loc!= None):
                spawn_point.location = loc
                walker_blueprint = random.choice(walker_blueprints)
                walker_create_command = carla_client.command_spawn_actor(walker_blueprint, spawn_point)
                batch_commands.append(walker_create_command)

        walker_result = carla_client.apply_commands_sync(batch_commands)

        walker_actor_ids = []

        for i in range(len(walker_result)):
            if walker_result[i].error:
                logging.error(walker_result[i].error)
            else:
                walker_actor_ids.append(walker_result[i].actor_id)

        batch_commands = []

        walker_controller_blueprint = carla_client.get_walker_controller_blueprint()

        for i in range(len(walker_actor_ids)):
            walker_controller_create_command = carla_client.command_spawn_actor(walker_controller_blueprint, carla.Transform(), walker_actor_ids[i])
            batch_commands.append(walker_controller_create_command)

        controller_result = carla_client.apply_commands_sync(batch_commands)

        for i in range(len(controller_result)):
            if(controller_result[i].error):
                logging.error(controller_result[i].error)
            else:
                full_walker = Walker(walker_actor_ids[i], controller_result[i].actor_id)
                walkers.append(full_walker)

        carla_client.tick()

        world.set_pedestrians_cross_factor(percentagePedestriansCrossing)

        for i in range(0, len(walkers)):
            walker = walkers[i]

            actor = carla_client.get_actor(walker.actor_id)
            controller  = carla_client.get_actor(walker.controller_id)
            controller.start()

            #controller.tion(carla_client.get_random_location_from_navigation())

            walker.set_actor(actor)
            walker.set_controller(controller)

    except:
        DespawnPedestrians(carla_client, walkers)

    return walkers

def SpawnPedestriansWithTargets(carla_client, num_agents):

    walkers = []

    try:

        world = carla_client.get_world()

        percentagePedestriansCrossing = 0.0

        spawn_points = []
        batch_commands = []

        walker_blueprints = carla_client.get_all_walker_blueprints()

        for i in range(num_agents):
            spawn_point = carla.Transform()
            loc = carla_client.get_random_location_from_navigation()
            if(loc!= None):
                spawn_point.location = loc
                walker_blueprint = random.choice(walker_blueprints)
                walker_create_command = carla_client.command_spawn_actor(walker_blueprint, spawn_point)
                batch_commands.append(walker_create_command)

        walker_result = carla_client.apply_commands_sync(batch_commands)

        walker_actor_ids = []

        for i in range(len(walker_result)):
            if walker_result[i].error:
                logging.error(walker_result[i].error)
            else:
                walker_actor_ids.append(walker_result[i].actor_id)

        batch_commands = []

        walker_controller_blueprint = carla_client.get_walker_controller_blueprint()

        for i in range(len(walker_actor_ids)):
            walker_controller_create_command = carla_client.command_spawn_actor(walker_controller_blueprint, carla.Transform(), walker_actor_ids[i])
            batch_commands.append(walker_controller_create_command)

        controller_result = carla_client.apply_commands_sync(batch_commands)

        for i in range(len(controller_result)):
            if(controller_result[i].error):
                logging.error(controller_result[i].error)
            else:
                full_walker = Walker(walker_actor_ids[i], controller_result[i].actor_id)
                walkers.append(full_walker)

        carla_client.tick()

        world.set_pedestrians_cross_factor(percentagePedestriansCrossing)

        for i in range(0, len(walkers)):
            walker = walkers[i]

            actor = carla_client.get_actor(walker.actor_id)
            controller  = carla_client.get_actor(walker.controller_id)
            controller.start()

            controller.tion(carla_client.get_random_location_from_navigation())

            walker.set_actor(actor)
            walker.set_controller(controller)

    except:
        DespawnPedestrians(carla_client, walkers)

    return walkers


def SpawnPedestriansAtLocations(carla_client :Carla, walker_spawn_locations, num_agents):

    walkers = []

    try:
        batch_commands = []

        walker_blueprints = carla_client.get_all_walker_blueprints()

        for i in range(num_agents):
            spawn_point = walker_spawn_locations[i]
            walker_blueprint = random.choice(walker_blueprints)
            walker_create_command = carla_client.command_spawn_actor(walker_blueprint, spawn_point)
            batch_commands.append(walker_create_command)
    
        walker_result = carla_client.apply_commands_sync(batch_commands)

        walker_actor_ids = []

        for i in range(len(walker_result)):
            if walker_result[i].error:
                logging.error(walker_result[i].error)
            else:
                walker_actor_ids.append(walker_result[i].actor_id)

        batch_commands = []

        walker_controller_blueprint = carla_client.get_walker_controller_blueprint()

        for i in range(len(walker_actor_ids)):
            walker_controller_create_command = carla_client.command_spawn_actor(walker_controller_blueprint, carla.Transform(), walker_actor_ids[i])
            batch_commands.append(walker_controller_create_command)

        controller_result = carla_client.apply_commands_sync(batch_commands)

        for i in range(len(controller_result)):
            if(controller_result[i].error):
                logging.error(controller_result[i].error)
            else:
                full_walker = Walker(walker_actor_ids[i], controller_result[i].actor_id)
                walkers.append(full_walker)

        carla_client.tick()

        for i in range(0, len(walkers)):
            walker = walkers[i]

            actor = carla_client.get_actor(walker.actor_id)
            controller  = carla_client.get_actor(walker.controller_id)
            controller.start()

            walker.set_actor(actor)
            walker.set_controller(controller)

    except:
        DespawnPedestrians(carla_client, walkers)

    return walkers


def GetSpawnPointsNearLocation(carla_client : Carla, location, num_spawnpoints):

    PedestriansSpawnPointsFactor = 50

    numSpawnPointsToGenerate = PedestriansSpawnPointsFactor * num_spawnpoints

    spawn_points_and_distances = []
    for i in range(numSpawnPointsToGenerate):
        random_location = carla_client.get_random_location_from_navigation()
        spawn_point = carla.Transform()
        spawn_point.location = random_location
        distance = compute_distance(spawn_point.location, location)
        spawn_points_and_distances.append((spawn_point, distance))

    spawn_points_and_distances_sorted = sorted(spawn_points_and_distances, key = lambda SpawnAndDistance : SpawnAndDistance[1])

    shortestDist = 1.5

    spawn_points = []
    unselected_spawn_points = []

    for pIndex in range(1, len(spawn_points_and_distances_sorted)):
        potential_point = spawn_points_and_distances_sorted[pIndex]
        current_lowest_dist = np.inf

        for selectedPoint, _distanceToObserver in spawn_points:
            distToThisPoint = compute_distance(potential_point[0].location, selectedPoint.location)

            if(distToThisPoint < current_lowest_dist):
                current_lowest_dist = distToThisPoint


        if current_lowest_dist > shortestDist:
            spawn_points.append(potential_point)
        else:
            unselected_spawn_points.append(potential_point)

        if(len(spawn_points) == num_spawnpoints):
            break

    if(len(spawn_points) < num_spawnpoints):
        num_additional_spawn_points = num_spawnpoints - len(spawn_points)

        spawn_points.extend(unselected_spawn_points[:num_additional_spawn_points])

    return [SpawnPointAndDist[0] for SpawnPointAndDist in spawn_points]
    

def DespawnPedestrians(carla_client, walkers):

    batch_commands = []

    for i in range(len(walkers)):
        walker_actor =  carla_client.get_actor(walkers[i].actor_id)
        controller_actor = carla_client.get_actor(walkers[i].controller_id)
      
        delete_walker_command = carla_client.command_delete_actor(walker_actor)
        delete_controller_command = carla_client.command_delete_actor(controller_actor)
      
        batch_commands.append(delete_walker_command)
        batch_commands.append(delete_controller_command)
    
    carla_client.apply_commands_sync(batch_commands)

