# Wilde
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
                                  Minimal duration music has t be when
                                  exporting

  -jd, --join_distance INTEGER    The maximum time between joined segments
  --help                          Show this message and exit.
```
## Installation
Download the latest release. 
Make sure you have python 3 installed.

Unpack the release into a directory and run the following command:
```
python setup.py install
```
Installation might take a while, since it has to install multiple large machine learning libraries.

If you are missing `tensorflow` upon install, go to [tensorflow.org](https://www.tensorflow.org/install/pip#package-location) and get the link for your wheel package.

Then run the following command, replacing the link with your new link:
```
python -m pip install --upgrade https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-2.3.0-cp38-cp38-manylinux2010_x86_64.whl
```


## Using your GPU
By default Wilde will not use your GPU. If you want to speed up Wilde, you have to enable GPU support for tensorflow. This can be done by following these instructions:
[Windows Tutorial](https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781)
[Ubuntu Tutorial](https://towardsdatascience.com/installing-tensorflow-gpu-in-ubuntu-20-04-4ee3ca4cb75d)
