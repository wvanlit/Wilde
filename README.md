# Wilde
Wilde is a command line tool to find and extract music from podcasts

```
Usage: main.py [OPTIONS] PATH

Options:
  -t, --file_type [mp3|wav]  The file format. Defaults to mp3.
  -s, --size INTEGER         Segmentation size in seconds. Defaults to 600.
  -o, --output PATH          Path for the output files.
  -v, --verbose TEXT         Output verbose logging information.
  --help                     Show this message and exit.
```
## Using your GPU
By default Wilde will not use your GPU. If you want to speed up Wilde, you have to enable GPU support for tensorflow. This can be done by following these instructions:
[Windows Tutorial](https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781)
[Ubuntu Tutorial](https://towardsdatascience.com/installing-tensorflow-gpu-in-ubuntu-20-04-4ee3ca4cb75d)
