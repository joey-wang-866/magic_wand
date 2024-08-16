# magic_wand
## Install conda using installer

1. First, go to the Anaconda website at https://www.anaconda.com/products/individual and download the installer for your operating system.

1. Run the installer and follow the instructions to complete the installation. During the installation process, you can choose to add Anaconda to your system path, which will make it easier to access from the command line.

1. Once Anaconda is installed, open a terminal or command prompt and type `conda --version` to verify that it is installed correctly.


## Setting up conda virtual environment

1.  To create a new virtual environment, you can use the conda create command followed by the name of the environment and any packages you want to install. For example, to create a new environment called `magic_wand` with Python 3.12, you can use the following command:

        conda create --name magic_wand python=3.12

    This will create a new virtual environment called magic_wand with Python 3.12 installed

1.  Initialize bash

        conda init bash

1.  To activate the virtual environment, you can use the following command:

        conda activate magic_wand

## Install required packages
1.  Run this command

        pip install -r requirements.txt

## Train YOLOv10
    cd yolov10
    yolo detect train data=D:\pycharm\magic_wand\datasets\data.yaml model=yolov10x.yaml epochs=30 batch=4 imgsz=640 device=0


