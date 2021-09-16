import tensorflow as tf

from config.config import DATASET_FOLDER
from utils.Logger import logger
from utils.TrajectoryDataset import TrajectoryDataset
from models.generator.encoder import Encoder
from models.generator.poolingmodule import PoolingModule


dataset = TrajectoryDataset(DATASET_FOLDER)


encoder = Encoder()
pool_module= PoolingModule()
logger.info(encoder)
logger.info(pool_module)

for sample in dataset:
    input_data = sample[:,:8,:]
    label_data = sample[:,8:,:]
    ending_positions = input_data[:,-1,:]
    result = encoder(input_data)
    result = pool_module(result, ending_positions)