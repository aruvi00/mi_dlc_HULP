#AUTOCODE_DLC
# CÓGIGO PARA AUTOMATIZAR DLC
import deeplabcut
import subprocess
import os
import sys
deeplabcut.__version__

#PARAMETERS

name_project ='frames'
name_experimenter = 'ainhoa'
video_folder_path = 'C:\\Users\\ainho\\OneDrive\\Escritorio\\UPM4\\TFG\\mis_pruebas\\estudio'
dirs = os.listdir(video_folder_path)
video = []
for file in dirs:
    file = str(file)
    video.append(video_folder_path+'\\'+file)

working_directory = 'C:\\Users\\ainho\\OneDrive\\Escritorio\\UPM4\\TFG\\mis_pruebas'
#CREATE PROJECT
config_path = deeplabcut.create_new_project(name_project, name_experimenter, video, working_directory, copy_videos=True)
#config_path = 'C:\\Users\\ainho\\OneDrive\\Escritorio\\UPM4\\TFG\\mis_pruebas\\r1-ainhoa-2022-04-26\\config.yaml'
print('Editamos ahora el fichero config.yaml')
##### Leemos el fichero de configuracion #####
cfg = deeplabcut.auxiliaryfunctions.read_config(config_path) 

##### Editamos el fichero de configuración #####
# cfg[parametroa_cambiar] = nueva_variable

cfg["bodyparts"] = ["toe",
                    "mtp",
                    "ankle"]
cfg["numframes2pick"] = 10
cfg["dotsize"] = 4
cfg["batch_size"] = 3
cfg["pcutoff"] = 0.1
cfg["TrainingFraction"] = [0.95]
cfg["skeleton"] = [ ["toe",
                        "mtp"],
                    ["mtp", 
                        "ankle"]
                    ]

##### Actualizamos el fichero de configuración #####
deeplabcut.auxiliaryfunctions.write_config(config_path, cfg)
print ("Configuracion completada")

#EXTRACT FRAMES
deeplabcut.extract_frames(config_path, mode='automatic',userfeedback=False, crop=True)

#LABEL FRAMES
deeplabcut.label_frames(config_path)
#CHECK LABELS
deeplabcut.check_labels(config_path)

###########################

#REFINE LABELS
config_path = 'C:\\Users\\ainho\\OneDrive\\Escritorio\\UPM4\\TFG\\mis_pruebas\\frames-ainhoa-2022-05-31\\config.yaml'
deeplabcut.refine_labels(config_path)
deeplabcut.merge_datasets(config_path)

