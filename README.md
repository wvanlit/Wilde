# Wilde
[![Build Status](https://dev.azure.com/wilde-cli/Wilde/_apis/build/status/wvanlit.Wilde?branchName=main)](https://dev.azure.com/wilde-cli/Wilde/_build/latest?definitionId=1&branchName=main)

Wilde is a command line tool to find and extract music from podcasts

```
Usage: wilde [OPTIONS] PATH

Options:
  -t, --file_type [mp3|wav]       The file format. Defaults to mp3.
  -s, --size INTEGER              Segmentation size in seconds. Defaults to
                                  600.

  -o, --output PATH               Path for the output files.
  -v, --verbose                   Output verbose logging information.
  -md, --minimal_duration INTEGER
                                  Minimal duration music has to be when
                                  exporting

  -jd, --join_distance INTEGER    The maximum time between joined segments
  --help                          Show this message and exit.
```
## Installation
Download the latest release. Make sure you have python 3 installed.

### Ubuntu
Unpack the release into a directory and run the following commands:
```
python -m pip install --upgrade pip setuptools wheel
python setup.py install
```

### Windows
```
python -m pip install --upgrade pip setuptools wheel
pip install torch==1.4 torchvision==0.5 -f https://download.pytorch.org/whl/torch_stable.html
python setup.py install
```
Installation might take a while, since it has to install multiple large machine learning libraries.

### Troubleshooting
#### Libsndfile
If you get an error about missing libsndfile do one of the following:

* Install from the official website [here](http://www.mega-nerd.com/libsndfile/#Download) on both Linux and Windows

* Run `sudo apt-get install libsndfile` on Ubuntu

* If you are using `conda` then you can get the package from `conda-forge` by running:
```
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install --yes --quiet libsndfile  
```
#### Tensorflow
If you are missing `tensorflow` upon install, go to [tensorflow.org](https://www.tensorflow.org/install/pip#package-location) and get the link for your wheel package.
Then run the following command, replacing the link with your new link:
```
python -m pip install --upgrade https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-2.3.0-cp38-cp38-manylinux2010_x86_64.whl
```
#### PyTorch on Conda
If you get an error regarding `torch` during the setup installation, try running the following command before running the setup again:
```
conda install pytorch
```
## Using your GPU
By default Wilde will not use your GPU. If you want to speed up Wilde, you have to enable GPU support for tensorflow. This can be done by following these instructions:

[Windows Tutorial](https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781)

[Ubuntu Tutorial](https://towardsdatascience.com/installing-tensorflow-gpu-in-ubuntu-20-04-4ee3ca4cb75d)
