#codigo para entrenar y analizar de manera automatizada
import deeplabcut
import os
import sys
deeplabcut.__version__

#PARAMETERS
name_project = 'r3-ainhoa-2022-05-10'
path_config_file = '/home/ainhoar/my_dlc/r3-ainhoa-2022-05-10/config.yaml'

#CREATE TRAINING DATASET
deeplabcut.create_training_dataset(path_config_file, net_type='resnet_50', augmenter_type='imgaug', num_shuffles=1, windows2linux=True)

#TRAIN NETWORK
path_pose = ''
cfg = deeplabcut.auxiliaryfunctions.read_config(path_pose) 

##### Editamos el fichero de configuración #####
# cfg[parametroa_cambiar] = nueva_variable

cfg["global_scale"] = 0.3
cfg["max_input_size"] = 2500
cfg["batch_size"] = 3

deeplabcut.train_network(path_config_file, gputouse=0, displayiters=10, maxiters=900000, saveiters=50000, allow_growth=True)

#EVALUATE NETWORK
deeplabcut.evaluate_network(path_config_file,gputouse=0,plotting=True)

#VIDEO ANAYSIS
path_config_file = '/home/ainhoar/my_dlc/r3-ainhoa-2022-05-10/config.yaml'
videos=['/home/ainhoar/my_dlc/r3-ainhoa-2022-05-10/estudio']
    #crearme una carpeta train de videos a entrenar
deeplabcut.analyze_videos(path_config_file,videos, videotype="MP4", gputouse=0, save_as_csv=True)

#PLOTEAR TRAYECTORIAS
deeplabcut.create_labeled_video(path_config_file,videos,videotype="MP4")
deeplabcut.plot_trajectories(path_config_file,videos,videotype="mp4")

#EXTRACT OUTLIER FRAMES
deeplabcut.extract_outlier_frames(path_config_file,videos,videotype="MP4")

#VOLVEMOS A LOCAL!!