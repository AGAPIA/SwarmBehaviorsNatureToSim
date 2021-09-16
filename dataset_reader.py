import pickle
import json

filePath = '/home/eduard/Private/carla/PythonAPI/Dizertatie/customdata/people/people.p'
input_file = open(filePath,'rb')
pedestrians_dict = pickle.load(input_file)

#print(pedestrians_dict.__keys__())
#print(pedestrians_dict.keys())
#print(pedestrians_dict[0][542])
