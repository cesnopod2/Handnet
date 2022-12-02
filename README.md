# Handnet_git

This repository contains code of engineering thesis entiled : 
"Deep Neural Network based Dynamic Hand Gesture Recognition using
RGB-D Data" authored by the repository owner created on the Warsaw Institute of Technology.  

![hello_handnet](https://user-images.githubusercontent.com/62251975/204252981-4c8dde54-667e-4670-8fb5-eeed2fbd9c45.gif)


Uploaded project contains proposed gesture recogniton module based on 
LSTM units. Implementation of the model contains in directory : 
[ add directory ]
Moreover I've proposed hand gesture recognition framework, which enables uploading
different recognition models to check how it behave in real-time situation.
It has dedicated GUI. Graphical user interface's code is also included in this repository. 
It was implemented using the Tkinter library.

## Roadmap
* data
  - paths_stat_stop_label.pkl
- GUI
  - camera_thread.py
  - data_collector.py
  - graph_view.py
  - graphical_user_interface.py
  - graphs.py
- model
  - model info
  - LSTM.ipynb
Readme.md

Files description : 
 - paths_stat_stop_label.pkl - file with dataframe containing inforamtion essential to creating dataset. 
 - camera_thread.py - application is initialized in this file. 
 - data_collector.py - contains classes related to custom dataset creation and hadling it in GUI. 
 - graph_views.py - file containing handling graph real-time updates : joint coordinates graphs & skeletal data graph.
 - graphical_user_interface.py - contains classes used for displaying and handling GUI. 
 -  graphs.py - file contains graph initialization. 


## Solution presentation 




## Authors

- [@cesnopod2](https://github.com/cesnopod2)
