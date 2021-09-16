Master Thesis

Natural Behaviour Predictor

This repository represents the code support of my Master Thesis.
The developed software is composed of three neural network models trained on a custom pedestrian trajectory prediction dataset created with Carla Simulator.

Techniques employed

1. Social LSTM Original Repository -> https://github.com/quancore/social-lstm
2. Social GAN Original Repository  -> https://github.com/agrimgupta92/sgan 
3. Social GAN with context awareness. This is a techinque based on the Social GAN paper. To increase the context awareness of the model I have fed the trajectory encoder with the embeddings of the scene segmentations in which the pedestrians where found.


The software allows the generation of pedestrains which behave in accord with the predictions of the previous described models. 

To make use of the software
1. Startup Carla
2. Run script.py


To select which technique you want to showcase modify the Controller script to by adding in the action pipeline the behaviours you want.
